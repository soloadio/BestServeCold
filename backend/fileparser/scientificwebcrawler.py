from serpapi import GoogleSearch
import os
import cloudscraper
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


class ScientificWebCrawler:

    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.page_load_delay = 2  # seconds
        self.section_wait_timeout = 10000  # milliseconds
        self.retry_delay = 2  # seconds
        self.max_retries = 3

    def getSignificantWebsite(self, query: str):
        params = self.returnParams(query)
        search = GoogleSearch(params)
        results = search.get_dict()
        url = results["organic_results"][0]["link"]
        return url

    def returnParams(self, query: str):
        return {
            "engine": "google",
            "q": str(query),
            "num": 1,
            "api_key": os.environ.get("SERPAPI_KEY"),
            "location": "Toronto, Ontario, Canada",
        }

    def getResearchInfo(self, url):
        paper_links = self.getAllRelativeLinks(url)
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
                        if ("https://doi.org/" in link or "pubmed" in link) and "account" not in link
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

    def getConclusionParagraph(self, researchPaperURL):
        final_result = ""
        for attempt in range(self.max_retries):
            try:
                with sync_playwright() as p:
                    browser = p.webkit.launch(headless=True)
                    page = browser.new_page()
                    page.goto(researchPaperURL, timeout=15000)  # navigation timeout 15s

                    # Wait for section elements to appear
                    page.wait_for_selector('section', timeout=self.section_wait_timeout)

                    sections = page.query_selector_all('section')
                    for section in sections:
                        header = section.query_selector('h2')
                        if header:
                            header_text = header.inner_text().lower()
                            if "conclusion" in header_text or "discussion" in header_text:
                                paragraphs = section.query_selector_all('p, div')
                                final_result = " ".join([p.inner_text().strip() for p in paragraphs])
                                break

                    browser.close()
                    if final_result:
                        return final_result

            except PlaywrightTimeoutError:
                print(f"Attempt {attempt + 1}: Section wait timeout, retrying...")
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")

            time.sleep(self.retry_delay)

        return final_result



if __name__ == "__main__":
  googleTest = ScientificWebCrawler()

  people = ["Ying Fu Li Lab"]

  # print(googleTest.getAllRelativeLinks("https://taari.mcmaster.ca/labs/kretz-lab/"))
  # for x in googleTest.getAllRelativeLinks("https://taari.mcmaster.ca/labs/kretz-lab/"):
  #   print(x)

  for x in people:
    scientisturl = googleTest.getSignificantWebsite(x)
    researchPaperURL, conclusionparagraph = googleTest.getResearchInfo(scientisturl)
    print(x + ":" , scientisturl, researchPaperURL)
    print("\n")
    print(conclusionparagraph)
    print("\n")

  # paragraphs = googleTest.getConclusionParagraph(researchPaperURL)

  # print(paragraphs)

  # for i, text in enumerate(paragraphs, 1):
  #     print(f"Paragraph {i}: {text}")
  # print(researchPaperURL)