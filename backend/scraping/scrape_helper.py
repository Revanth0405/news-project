# import selenium.webdriver as webdriver
# from selenium.webdriver.chrome.service import Service
# import time
# from bs4 import BeautifulSoup
# import scraping.scraping_llm as scraping_llm

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

def fetch_website_content(url: str):
    session = requests.Session()
    session.headers.update(headers)

    data = session.get(url)
    print(data.status_code)

# def scrape_website(website_url):

#     chrome_driver_path = ""
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')  
#     driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

#     try:
#         driver.get(website_url)

#         time.sleep(5)

#         html = driver.page_source
#         soup = BeautifulSoup(html, 'html.parser') 

#         content = soup.get_text()
#         modified_content = scraping_llm.extract_information(content)
#         return modified_content

#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     website_url = "https://www.nccu.edu/news/nccu-law-and-technology-symposium-and-summit-oct-10-11"
#     # content = scrape_website(website_url)
#     # print(content)
#     fetch_website_content(website_url)

