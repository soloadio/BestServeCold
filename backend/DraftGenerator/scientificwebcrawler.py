from serpapi import GoogleSearch
import os
import cloudscraper
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import requests
from bs4 import BeautifulSoup

from playwright_stealth import Stealth

class ScientificWebCrawler:

    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.page_load_delay = 2  # seconds
        self.section_wait_timeout = 5000  # milliseconds
        self.retry_delay = 2  # seconds
        self.max_retries = 3
        self.base_url = os.environ.get("GOOGLE_SEARCH_SERVER")

    # def getSignificantWebsite(self, query: str):
    #     params = self.returnParams(query)
    #     search = GoogleSearch(params)
    #     results = search.get_dict()
    #     print(results)
    #     url = results["organic_results"][0]["link"]
    #     return url
    
    def getSignificantWebsites(self, query: str, num_results: int = 1):
        """
        Returns the top N search result URLs for a query using the Google Custom Search API
        via the Node.js MCP server.
        """
        if not query or not query.strip():
            raise ValueError("Query must be a non-empty string.")

        payload = {
            "query": query,
            "numResults": num_results
        }

        try:
            response = requests.post(self.base_url, json=payload, timeout=10)

            # Check for HTTP errors
            response.raise_for_status()

            data = response.json()

            print(data)

            # Extract only the URLs
            urls = [item['url'] for item in data['results']]

            return urls

        except requests.exceptions.RequestException as e:
            print(f"❌ Error calling search API: {e}")
            return []



    def returnParams(self, query: str):
        return {
            "engine": "google",
            "q": str(query),
            "num": 1,
            "api_key": os.environ.get("SERPAPI_KEY"),
            "location": "Toronto, Ontario, Canada",
        }

    def getResearchInfo(self, url):
        # paper_links = self.getAllRelativeLinks(url)
        paper_links = self.getAllRelativeLinks2(url)
        print(f"Found {len(paper_links)} research papers:", paper_links)

        for link in paper_links:
            try:
                conclusion = self.getConclusionParagraph(link)
                if conclusion:
                    return link, conclusion
            except Exception as e:
                print(f"Failed to get conclusion for {link}: {e}")
                continue

        return None, None

    def getAllRelativeLinks(self, url):
        for attempt in range(self.max_retries):
            try:
                with sync_playwright() as p:
                    browser = p.webkit.launch(headless=True)
                    page = browser.new_page()
                    page.goto(url, timeout=15000)  # navigation timeout 15s

                    # Wait for page content to load
                    time.sleep(self.page_load_delay)

                    links = page.eval_on_selector_all(
                        'a[href]',
                        'elements => elements.map(el => el.href)'
                    )

                    filtered_links = [
                        link for link in links
                        if ("https://doi.org/" in link) and "account" not in link
                    ]

                    browser.close()
                    if filtered_links:
                        return filtered_links

            except PlaywrightTimeoutError:
                print(f"Attempt {attempt + 1}: Page load timeout, retrying...")
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")

            time.sleep(self.retry_delay)

        return []
    

    def getAllRelativeLinks2(self, query):
        return self.getSignificantWebsites(query, 10)


    def getConclusionParagraph(self, researchPaperURL):
        final_result = ""
        with Stealth().use_sync(sync_playwright()) as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(researchPaperURL, timeout=10000)

            
            try:
                # Wait for section elements to appear
                page.wait_for_selector('section', timeout=self.section_wait_timeout)

                # Print out the full page HTML each attempt
                html_content = page.content()
                print(html_content[:500])  # print first 2000 chars for readability

                sections = page.query_selector_all('section')
                print(f"Found {len(sections)} sections")

                for section in sections:
                    header = section.query_selector('h2')
                    if header:
                        header_text = header.inner_text().lower()
                        print(f"Checking section header: {header_text}")
                        if "conclu" in header_text or "discussion" in header_text:
                            paragraphs = section.query_selector_all('p, div')
                            final_result = " ".join([p.inner_text().strip() for p in paragraphs])
                            print("Conclusion/Discussion section found!")
                            break

            except PlaywrightTimeoutError:
                print(f"Couldnt find")
            except Exception as e:
                print(f"Couldnt find")

            time.sleep(self.retry_delay)

            browser.close()
        return final_result




if __name__ == "__main__":
    import asyncio
    from playwright.async_api import async_playwright
    from playwright_stealth import Stealth
    from dotenv import load_dotenv
    import random
    import time
    from playwright.sync_api import sync_playwright, TimeoutError
    load_dotenv()
    googleTest = ScientificWebCrawler()
    people = ["Ying Fu Li Lab"]

  # print(googleTest.getAllRelativeLinks("https://taari.mcmaster.ca/labs/kretz-lab/"))
  # for x in googleTest.getAllRelativeLinks("https://taari.mcmaster.ca/labs/kretz-lab/"):
  #   print(x)


    for x in people:
        scientisturl = googleTest.getSignificantWebsites(x)[0]
        researchPaperURL, conclusionparagraph = googleTest.getResearchInfo(scientisturl)
        print(x + ":" , scientisturl, researchPaperURL)
        print("\n")
        print(conclusionparagraph)
        print("\n")
