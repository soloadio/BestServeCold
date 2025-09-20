# import cloudscraper
# from bs4 import BeautifulSoup

# scraper = cloudscraper.create_scraper()  # creates a session like requests

# url = "https://doi.org/10.1002/anie.202415226"
# response = scraper.get(url)

# soup = BeautifulSoup(response.text, "lxml")
# print(soup.text)  # should now show the actual page title

from playwright.sync_api import sync_playwright

URL = 'https://taari.mcmaster.ca/labs/kretz-lab/'

with sync_playwright() as p:
    browser = p.webkit.launch(headless=True)
    page = browser.new_page()
    page.goto(URL)

    # Wait until the h1 element is loaded
    page.wait_for_selector('h1')

    # Extract the text
    h1_text = page.eval_on_selector('h1', 'el => el.innerText')

    print(h1_text)
