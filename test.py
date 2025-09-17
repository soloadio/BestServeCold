from serpapi import GoogleSearch


params = {
  "engine": "google",
  "q": "Yingfu Li Lab",
  "num": 1,
  "api_key": "5be9c096d3e498f405583bc2436daae1eeb3d068896123e14df7b710017f2b36",
  "location": "Toronto, Ontario, Canada",
}


def returnLab(query):

  search = GoogleSearch(params)
  results = search.get_dict()
  url = results["organic_results"][0]["link"]
  import requests
  from bs4 import BeautifulSoup

  r = requests.get(url)
  html_content = r.text
  soup = BeautifulSoup(html_content, 'lxml')  
  links = [a.get('href') for a in soup.find_all('a', href=True)]

  for x in links:
    if "doi" in x:
      print(x)



# from serpapi import GoogleSearch
# import os
# import requests
# from bs4 import BeautifulSoup

# class GoogleSearch:

#   def __init__():
#     pass

#   def getSignificantWebsite(self, query: str):
#     params = self.returnParams(query)

#     search = GoogleSearch(params)
#     results = search.get_dict()
#     url = results["organic_results"][0]["link"]

#     return url

#   def returnParams(self, query:str):
#     return {
#       "engine": "google",
#       "q": query,
#       "num": 1,
#       "api_key": os.environ.get("SERPAPI_KEY"),
#       "location": "Toronto, Ontario, Canada",
#     }
  
#   def getResearchPaper(self, url, query: str="doi"):
#     r = requests.get(url)
#     html_content = r.text
#     soup = BeautifulSoup(html_content, 'lxml')  
#     links = [a.get('href') for a in soup.find_all('a', href=True)]

#     for x in links:
#       if "doi" in x:
#         print(x)


# googleTest = GoogleSearch()

# researchPaper = googleTest.getResearchPaper(googleTest.getSignificantWebsite("https://www.yingfulilab.org"))
