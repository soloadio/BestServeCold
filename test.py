from serpapi import GoogleSearch
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import cloudscraper

load_dotenv()

class GoogleWebsite:

  # def __init__():
  #   pass

  scraper = cloudscraper.create_scraper()

  def getSignificantWebsite(self, query: str):
    params = self.returnParams(query)

    search = GoogleSearch(params)
    results = search.get_dict()
    url = results["organic_results"][0]["link"]

    return url

  def returnParams(self, query:str):
    return {
      "engine": "google",
      "q": query,
      "num": 1,
      "api_key": os.environ.get("SERPAPI_KEY"),
      "location": "Toronto, Ontario, Canada",
    }
  
  def getResearchPaper(self, url):
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content, 'lxml')  
    links = [a.get('href') for a in soup.find_all('a', href=True)]

    for x in links:
      
      if "https://doi.org/" in x:
        return x
    return None
  
  def getConclusionParagraph(self, researchPaperURL):

    response = self.scraper.get(researchPaperURL)
    soup = BeautifulSoup(response.text, "lxml")

    # Step 1: Find all <section> tags
    sections = soup.find_all("section")
    # Step 2: Loop through each section

    paragraphs = []
    for section in sections:
        # Find the <h2> inside the section
        header = section.find("h2")

        
        # Check if the header exists and contains "conclusion" (case-insensitive)
        if header and ("conclusion" in header.get_text(strip=True).lower() or  "discussion" in header.get_text(strip=True).lower()):
            # Get all paragraph texts inside this section
            paragraphs = [p.get_text(strip=True) for p in section.find_all("p")]

    return " ".join(paragraphs)
  


googleTest = GoogleWebsite()

researchPaperURL = googleTest.getResearchPaper(googleTest.getSignificantWebsite("Yingfu Li Lab"))
print(researchPaperURL)
paragraphs = googleTest.getConclusionParagraph(researchPaperURL)

print(paragraphs)

# for i, text in enumerate(paragraphs, 1):
#     print(f"Paragraph {i}: {text}")
# print(researchPaperURL)