import os
import requests
import re
import curl_cffi
from bs4 import BeautifulSoup

class ScientificWebCrawler:
    def __init__(self):
        self.base_url = os.environ.get("GOOGLE_SEARCH_SERVER")
    
    def get_websites(self, query: str, num_results: int = 1):
        """
        Returns the top 'num_results' search result URLs for a query using the Google Custom Search API
        via the Node.js MCP server.

        Args:
            query (str): The string to search in Google
            num_results (int): The number of results to return
        
        Returns:
            list (str): A list of URLs
        """
        if not query or not query.strip():
            raise ValueError("Query must be a non-empty string.")

        payload = {
            "query": query,
            "numResults": num_results
        }
        print(self.base_url)

        try:
            response = requests.post(self.base_url, json=payload, timeout=10)

            # Check for HTTP errors
            response.raise_for_status()

            data = response.json()

            # Extract only the URLs
            urls = [item['url'] for item in data['results']]

            return urls

        except requests.exceptions.RequestException as e:
            print(f"❌ Error calling search API: {e}")
            return []


    def get_researchdata(self, urls: list[str]):
        """
        Returns any single valid research data from urls.

        Args:
            urls (list[str]): A list of urls to process research data.
        
        Returns:
            researchdata (dict): A key value pair of data from a research paper. Format:
                "url" : "www.example.com" -> The URL the research data is processed from
                "data" : The research data from url.

                {'url': None, 'data': None} -> Returns none if no research data was found.
        """
        if not urls:   # nothing to process
            return {'url': None, 'data': None}

        for url in urls:
            data = self._get_datafromurl(url)
            if data['data']:
                return data
            print(f"Did not find any data in: {data['url']}")

        # if no data found in any URL, return empty
        return {'url': None, 'data': None}


    def _get_datafromurl(self, url: str, filter: list[str]=["conclu", "discussion"]):
        researchdata = {'url': url, 'data': None}

        response = curl_cffi.requests.get(url, impersonate="safari_ios", verify=False)

        soup = BeautifulSoup(response.text, "html.parser")

        target_h2 = soup.find("h2", string=re.compile(r"(conclu|discussion)", re.I))

        if target_h2:
            # get the parent section that contains this h2
            section = target_h2.find_parent("section")
            if section:
                print(section.get_text(strip=True))
                researchdata["data"] = section.get_text(strip=True)
            else:
                print("H2 found but no parent section")
        else:
            print("No matching H2 found")

        return researchdata


    def get_allrelativeurls(self, query: str, filter: list[str]=[], exclude: list[str]=[]):
        """
        Returns a list of a maximum of 10 filtered relative urls based on a Google query
        
        Args:
            url (str): The url to be processed.
            filter (list[str]): A list of possible strings to filter for in the URLs.
            exclude (list[str]): A list of possible strings in URL to be excluded from.

        Returns:
            filtered_urls (list[str]): A list of filtered relative links on a given URL.
        """
        urls = self.get_websites(query, 10)

        filtered_urls = self._filterurls(urls, filter, exclude)

        return filtered_urls
    

    def _filterurls(self, urls: list[str], filter: list[str], exclude: list[str]):
        """
        Returns a list of filtered urls based on filter and exclude.
        
        Args:
            urls (str): The list of urls to be filtered.
            filter (list[str]): A list of possible strings to filter for in the URLs.
            exclude (list[str]): A list of possible strings in URL to be excluded from.

        Returns:
            filtered_url (list[str]): A filtered list of urls.
        """
        filtered_url = []
        if not filter and not exclude:
            return urls
        
        for url in urls:
            # Filters each of the links, removing any link that contains an exclusion and doesn't contain the filter

            for exclusion in exclude:
                if exclusion in url:
                    break
                else:
                    for word in filter:
                        if word in url:

                            filtered_url.append(word)
        
        return filtered_url


    def process(self, query: str):
        urls = self.get_allrelativeurls(query)
        if not urls:
            print("error retrieving urls")
        print(f"Found {len(urls)} URLs: {', '.join(urls)}")

        researchdata = self.get_researchdata(urls)

        return researchdata
        # return 

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    crawl = ScientificWebCrawler()
    crawl.process("Ying Fu Li Research Paper")