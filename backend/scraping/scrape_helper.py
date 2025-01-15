from typing import List
import time
from threading import Thread
from logging import getLogger

from bs4 import BeautifulSoup
import requests

from ..helper_classes.CustomSearchResult import CustomSearchResult
from app_logging import setup_logging

setup_logging()
logger = getLogger("scraping")


class ContentScraper:
    def __init__(self):
        custom_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        self.scrape_session = requests.Session()
        self.scrape_session.headers.update(custom_headers)

    def __fetch_website_content(self, url: str, result: dict = None) -> str:
        """
        Fetches a website source content as plain html
        """
        logger.debug("Fetching %s", url)
        data = self.scrape_session.get(url)
        raw_content = data.text
        total_html = BeautifulSoup(raw_content, "html.parser")
        required_html = total_html.find("main") or total_html.find("body")
        if required_html is None:
            logger.warning("Unable to fetch content from %s", url)
            return

        content = required_html.get_text()
        result[url] = content

        # TODO: Remove the content, here we are not to return the content but \
        #       add the content to the result `dict`, also at the method annotation
        return content

    def fetch_websites(self, web_urls: List[CustomSearchResult]) -> dict:
        web_contents: dict = {}
        threads: List[Thread] = []

        start = time.time()
        for item in web_urls:
            thread = Thread(
                target=self.__fetch_website_content, args=(item.link, web_contents)
            )
            threads.append(thread)

        # joining the threads
        for thread in threads:
            thread.join()
        end = time.time()

        logger.info("Time taken in fetching the webpages: %f", (end - start))

        return web_contents


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

if __name__ == "__main__":
    website_url = "https://www.nccu.edu/news/nccu-law-and-technology-symposium-and-summit-oct-10-11"
    my_scraper = ContentScraper()
    print(my_scraper.__fetch_website_content(website_url))
