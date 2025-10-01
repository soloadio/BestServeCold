# import os
# import cloudscraper
# from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
# import requests
# from playwright_stealth import Stealth
# from .multitasker import Multitasker

# import time

# class ScientificWebCrawler:
#     def __init__(self):
#         self.scraper = cloudscraper.create_scraper()
#         self.page_load_delay = 2
#         self.retry_delay = 2
#         self.max_retries = 3
#         self.base_url = os.environ.get("GOOGLE_SEARCH_SERVER")
    
#     def get_websites(self, query: str, num_results: int = 1):
#         """
#         Returns the top 'num_results' search result URLs for a query using the Google Custom Search API
#         via the Node.js MCP server.

#         Args:
#             query (str): The string to search in Google
#             num_results (int): The number of results to return
        
#         Returns:
#             list (str): A list of URLs
#         """
#         if not query or not query.strip():
#             raise ValueError("Query must be a non-empty string.")

#         payload = {
#             "query": query,
#             "numResults": num_results
#         }

#         try:
#             response = requests.post(self.base_url, json=payload, timeout=10)

#             # Check for HTTP errors
#             response.raise_for_status()

#             data = response.json()

#             # Extract only the URLs
#             urls = [item['url'] for item in data['results']]

#             return urls

#         except requests.exceptions.RequestException as e:
#             print(f"❌ Error calling search API: {e}")
#             return []

#     def worker(self, url):
#         """
#         Worker function to fetch data from a given URL.
#         """
#         researchdata = {'url': None, 'data': None}
#         print(f"Process (PID {os.getpid()}), starting search for: {url}")
#         try:
#             data = self._get_datafromurl(url)
#             # print("uhhh", data)
#             if data:
#                 researchdata['url'] = url
#                 researchdata['data'] = data
#                 return researchdata
#         except Exception as e:
#             print(f"Failed to get conclusion for {url}: {e}")
#         return researchdata
    
#     def valid_data(self, result):
#         if (result['url'] and result['data']):
#             return True
#         return False


#     def get_researchdata(self, urls: list[str]):
#         """
#         Launches multiple processes to fetch data concurrently.
#         Returns the first valid research data and kills other processes.
#         """
#         multitasker = Multitasker()
#         researchdata = multitasker.run(self.worker, urls, (), self.valid_data, stop_on_first_valid=False)
        
#         # print(researchdata)
#         return researchdata


#     # def get_researchdata(self, urls: list[str]):
#     #     """
#     #     Returns any single valid research data from urls.

#     #     Args:
#     #         urls (list[str]): A list of urls to process research data.
        
#     #     Returns:
#     #         researchdata (dict): A key value pair of data from a research paper. Format:
#     #             "url" : "www.example.com" -> The URL the research data is processed from
#     #             "data" : The research data from url.

#     #             {'url': None, 'data': None} -> Returns none if no research data was found.
#     #     """

#     #     researchdata = {'url': None, 'data': None}

#     #     for url in urls:
#     #         try:
#     #             data = self._get_datafromurl(url)
#     #             if data:
#     #                 researchdata['url'] = url
#     #                 researchdata['data'] = data
#     #         except Exception as e:
#     #             print(f"Failed to get conclusion for {url}: {e}")
#     #     return researchdata


#     def _get_datafromurl(self, url: str, filter: list[str]=["conclu", "discussion"]):
#         final_result = ""
#         with Stealth().use_sync(sync_playwright()) as p:
#             browser = p.chromium.launch(headless=True)
#             page = browser.new_page()
#             page.goto(url, timeout=8000)

            
#             try:
#                 # Wait for section elements to appear
#                 page.wait_for_selector('section', timeout=5000)

#                 time.sleep(5)
                
#                 sections = page.query_selector_all('section')

#                 for section in sections:
#                     header = section.query_selector('h2')
#                     if header:
#                         header_text = header.inner_text().lower()

#                         for word in filter:
#                             if word in header_text:
#                                 paragraphs = section.query_selector_all('p, div')
#                                 final_result = " ".join([p.inner_text().strip() for p in paragraphs])
#                                 print(f"{word} section found!")
#                                 break

#             except PlaywrightTimeoutError:
#                 print(f"Page load timeout, could not load page: {url}")
#             except Exception as e:
#                 print(f"Error retrieving data from: {url}. Error: {e}")
            
#             browser.close()
#         return final_result



#     def get_allrelativelinks(self, url: str, filter: list[str]=["https://doi.org/"], exclude: list[str]=["account"]):
#         """
#         Returns a list of filtered relative urls on a given URL.
        
#         Args:
#             url (str): The url to be processed.
#             filter (list[str]): A list of possible strings to filter for in the URLs.
#             exclude (list[str]): A list of possible strings in URL to be excluded from.

#         Returns:
#             filtered_urls (list[str]): A list of filtered relative urls on a given URL.
#         """
#         try:
#             with sync_playwright() as p:
#                 browser = p.webkit.launch(headless=True)
#                 page = browser.new_page()
#                 page.goto(url, timeout=8000)

#                 urls = page.eval_on_selector_all(
#                     'a[href]',
#                     'elements => elements.map(el => el.href)'
#                 )

#                 browser.close()

#                 filtered_urls = self._filterurls(urls, filter, exclude)
                
#                 if filtered_urls:
#                     return filtered_urls

#         except PlaywrightTimeoutError:
#             print(f"Page load timeout, could not load page: {url}")
#         except Exception as e:
#             print(f"Error retrieving links on: {url}. Error: {e}")

#         return []
    

#     def get_allrelativeurls2(self, query: str, filter: list[str]=[], exclude: list[str]=[]):
#         """
#         Returns a list of a maximum of 10 filtered relative urls based on a Google query
        
#         Args:
#             url (str): The url to be processed.
#             filter (list[str]): A list of possible strings to filter for in the URLs.
#             exclude (list[str]): A list of possible strings in URL to be excluded from.

#         Returns:
#             filtered_urls (list[str]): A list of filtered relative links on a given URL.
#         """
#         urls = self.get_websites(query, 10)

#         filtered_urls = self._filterurls(urls, filter, exclude)

#         return filtered_urls
    

#     def _filterurls(self, urls: list[str], filter: list[str], exclude: list[str]):
#         """
#         Returns a list of filtered urls based on filter and exclude.
        
#         Args:
#             urls (str): The list of urls to be filtered.
#             filter (list[str]): A list of possible strings to filter for in the URLs.
#             exclude (list[str]): A list of possible strings in URL to be excluded from.

#         Returns:
#             filtered_url (list[str]): A filtered list of urls.
#         """
#         filtered_url = []
#         if not filter and not exclude:
#             return urls
        
#         for url in urls:
#             # Filters each of the links, removing any link that contains an exclusion and doesn't contain the filter

#             for exclusion in exclude:
#                 if exclusion in url:
#                     break
#                 else:
#                     for word in filter:
#                         if word in url:

#                             filtered_url.append(word)
        
#         return filtered_url


#     def process(self, query: str):
#         urls = self.get_allrelativeurls2(query)
#         print(f"Found {len(urls)} URLs: {', '.join(urls)}")

#         collection_researchdata = self.get_researchdata(urls)

#         noresult = {'url': None, 'data': None}
#         for researchdata in collection_researchdata:
#             if researchdata['url'] and researchdata['data']:
#                 # print(f"Found data in {researchdata['url']}: {researchdata['data']}")
#                 return researchdata
    
#         return noresult



# if __name__ == "__main__":
#     from dotenv import load_dotenv
#     load_dotenv()
#     googleTest = ScientificWebCrawler()
#     people = ["Ying Fu Li Lab"]


#     for x in people:
#         scientisturl = googleTest.getSignificantWebsites(x)[0]
#         researchPaperURL, conclusionparagraph = googleTest.getResearchInfo(scientisturl)
#         print(x + ":" , scientisturl, researchPaperURL)
#         print("\n")
#         print(conclusionparagraph)
#         print("\n")
import os
import psutil
import cloudscraper
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import requests
from playwright_stealth import Stealth
from .multitasker import Multitasker
import time

class ScientificWebCrawler:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.page_load_delay = 2
        self.retry_delay = 2
        self.max_retries = 3
        self.base_url = os.environ.get("GOOGLE_SEARCH_SERVER")
        print(f"🚀 Base URL set to: {self.base_url}")
        self._log_system_info()

    def _log_system_info(self):
        """Logs basic server stats for debugging."""
        mem = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)
        print(f"💾 Memory Usage: {mem.percent}% ({mem.used / 1e6:.2f}MB used / {mem.total / 1e6:.2f}MB total)")
        print(f"🖥 CPU Usage: {cpu}%")
        print(f"⚙️ Active threads/processes: {len(psutil.pids())}")

    def get_websites(self, query: str, num_results: int = 1):
        if not query or not query.strip():
            raise ValueError("Query must be a non-empty string.")

        payload = {
            "query": query,
            "numResults": num_results
        }

        try:
            print(f"🔍 Sending search request: {payload}")
            response = requests.post(self.base_url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            urls = [item['url'] for item in data.get('results', [])]
            print(f"✅ Received {len(urls)} URLs from search API")
            return urls

        except requests.exceptions.RequestException as e:
            print(f"❌ Error calling search API: {e}")
            self._log_system_info()
            return []

    def worker(self, url):
        researchdata = {'url': None, 'data': None}
        print(f"Process (PID {os.getpid()}), starting search for: {url}")
        try:
            data = self._get_datafromurl(url)
            if data:
                researchdata['url'] = url
                researchdata['data'] = data
                return researchdata
        except Exception as e:
            print(f"❌ Failed to get conclusion for {url}: {e}")
            self._log_system_info()
        return researchdata

    def valid_data(self, result):
        return bool(result.get('url') and result.get('data'))

    def get_researchdata(self, urls: list[str]):
        multitasker = Multitasker()
        researchdata = multitasker.run(self.worker, urls, (), self.valid_data, stop_on_first_valid=False)
        return researchdata

    def _get_datafromurl(self, url: str, filter: list[str]=["conclu", "discussion"]):
        final_result = ""
        try:
            with Stealth().use_sync(sync_playwright()) as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=8000)
                print("heres the content on the page:", page.content())
                try:
                    page.wait_for_selector('section', timeout=5000)
                    time.sleep(5)
                    sections = page.query_selector_all('section')
                    for section in sections:
                        header = section.query_selector('h2')
                        if header:
                            header_text = header.inner_text().lower()
                            for word in filter:
                                if word in header_text:
                                    paragraphs = section.query_selector_all('p, div')
                                    final_result = " ".join([p.inner_text().strip() for p in paragraphs])
                                    snippet = final_result[:300] + ("..." if len(final_result) > 300 else "")
                                    print(f"✅ {word} section found at {url}")
                                    print(f"📄 Snippet: {snippet}\n")
                                    break
                except PlaywrightTimeoutError:
                    print(f"⏱ Page load timeout for URL: {url}")
                except Exception as e:
                    print(f"❌ Error extracting data from URL: {url}, {e}")
                    self._log_system_info()
                browser.close()
        except Exception as e:
            print(f"❌ Playwright error for URL {url}: {e}")
            self._log_system_info()
        return final_result
    def get_allrelativelinks(self, url: str, filter: list[str]=["https://doi.org/"], exclude: list[str]=["account"]):
        try:
            with sync_playwright() as p:
                browser = p.webkit.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=8000)
                urls = page.eval_on_selector_all('a[href]', 'elements => elements.map(el => el.href)')
                browser.close()
                filtered_urls = self._filterurls(urls, filter, exclude)
                print(f"🔗 Found {len(filtered_urls)} filtered links on {url}")
                return filtered_urls
        except Exception as e:
            print(f"❌ Error retrieving links on {url}: {e}")
            self._log_system_info()
            return []

    def get_allrelativeurls2(self, query: str, filter: list[str]=[], exclude: list[str]=[]):
        urls = self.get_websites(query, 10)
        filtered_urls = self._filterurls(urls, filter, exclude)
        print(f"🔗 Query '{query}' yielded {len(filtered_urls)} filtered URLs")
        return filtered_urls

    def _filterurls(self, urls: list[str], filter: list[str], exclude: list[str]):
        filtered_url = []
        for url in urls:
            if exclude and any(excl in url for excl in exclude):
                continue
            if filter and any(f in url for f in filter):
                filtered_url.append(url)
            elif not filter:
                filtered_url.append(url)
        return filtered_url

    def process(self, query: str):
        urls = self.get_allrelativeurls2(query)
        print(f"🔍 Found {len(urls)} URLs for query '{query}'")
        collection_researchdata = self.get_researchdata(urls)
        noresult = {'url': None, 'data': None}
        for researchdata in collection_researchdata:
            if researchdata['url'] and researchdata['data']:
                return researchdata
        return noresult