import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()  # creates a session like requests

url = "https://doi.org/10.1002/anie.202415226"
response = scraper.get(url)

soup = BeautifulSoup(response.text, "lxml")
print(soup.text)  # should now show the actual page title