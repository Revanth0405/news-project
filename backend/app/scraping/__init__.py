"""
This module provides the necessary classes and methods for scraping web content
for the backend application. It utilizes multi-threading to fetch content from
multiple websites concurrently, enhancing performance.

Dependencies:
- requests: For making HTTP requests.
- BeautifulSoup (bs4): For parsing and extracting HTML content.
- threading: For managing concurrent scraping operations.
- logging: For logging debug and warning messages.

Helper imports:
- CustomSearchResult: A helper class to represent search results
- setup_logging: A utility function to configure logging
"""

import time
from threading import Thread
from typing import List
import logging

import requests
from bs4 import BeautifulSoup

from helpers import CustomSearchResult
from utils.logger import get_logger

# Configure the logging system
logger = get_logger(__name__)
logger.setLevel(logging.DEBUG)


class MyContentScraper:
    """
    A custom web scraper designed to fetch content from multiple webpages efficiently.
    It uses threading to perform concurrent fetch operations and extracts the
    main or body content of webpages.

    Attributes:
        scrape_session (requests.Session): A session object with predefined
        headers to mimic browser requests.
    """

    def __init__(self):
        """
        Initializes the scraper with custom HTTP headers for the session.
        These headers help disguise automated requests as legitimate browser activity.
        """
        custom_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        # Create a requests session and set custom headers
        self.scrape_session = requests.Session()
        self.scrape_session.headers.update(custom_headers)

    def __fetch_website_content(self, url: str, result: dict):
        """
        Fetches the content of a single webpage and stores it in the result dictionary.
        """
        logger.debug("Fetching content from URL: %s", url)

        try:
            # Make the GET request to fetch webpage content
            response = self.scrape_session.get(url)
            response.raise_for_status()  # Raise an error for non-200 HTTP status codes

            # Parse the HTML content using BeautifulSoup
            raw_content = response.text
            soup = BeautifulSoup(raw_content, "html.parser")

            # Extract text content from the main or body section of the webpage
            if soup.main:
                text_content = soup.main.get_text(separator="\n", strip=True)
            elif soup.body:
                text_content = soup.body.get_text(separator="\n", strip=True)
            else:
                text_content = "No meaningful content found"

            if not text_content.strip():
                logger.warning("Unable to extract meaningful content from URL: %s", url)
                result[url] = "No meaningful content found"
            else:
                result[url] = text_content

        except requests.RequestException as e:
            logger.warning("Failed to fetch content from URL: %s. Error: %s", url, e)
            result[url] = "Failed to fetch content"

    def fetch_websites(self, web_urls: List[CustomSearchResult]) -> dict:
        """
        Fetches the content of multiple websites concurrently using threads.

        Args:
            web_urls (List[CustomSearchResult]): A list of `CustomSearchResult`
            objects containing URLs to scrape.

        Returns:
            dict: A dictionary containing the URLs as keys and their fetched
            HTML content as values.
        """
        web_contents: dict = {}
        threads: List[Thread] = []

        start_time = time.time()  # Record the start time

        # Create and start a thread for each URL
        for item in web_urls:
            thread = Thread(
                target=self.__fetch_website_content, args=(item.link, web_contents)
            )
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        end_time = time.time()  # Record the end time
        logger.info(
            "Time taken to fetch %d webpages: %.2f seconds", len(web_urls), (end_time - start_time)
        )

        return web_contents