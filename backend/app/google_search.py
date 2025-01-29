from typing import List
import os
from logging import getLogger

from dotenv import load_dotenv
import requests

from helpers import CustomSearchResult
from utils.logger import setup_logging


# setup_logging()
# logger = getLogger("search_api")

# Load environment variables from .env file
load_dotenv()

# API credentials
API_URL = os.getenv("CUSTOM_SEARCH_API_URL")
API_KEY = os.getenv("CUSTOM_SEARCH_API_KEY")
CX = os.getenv("CUSTOM_SEARCH_CX")

MAX_RESULTS = 10  # Maximum number of results to fetch

def custom_search(query: str) -> List[CustomSearchResult]:
    """
    Searches Google using the Custom Search API for a single query.
    Returns a list of search results (items) for the query.
    """
    # logger.debug("Fetching results from Google Custom Search API for query: %s", query)
    params = {
        "q": f"{query} site:news OR inurl:news OR inurl:article",
        "key": API_KEY,
        "cx": CX,
        "num": MAX_RESULTS,  # Request up to MAX_RESULTS
        "fields": "items(title,htmlTitle,link,displayLink)"  # Only fetch necessary fields
    }

    try:
        response = requests.get(API_URL, params=params, timeout=(3, 5))
        response.raise_for_status()  # Raise an error for bad responses
        search_response = response.json().get("items", [])
        
        if not search_response:
            print("No items found in search response.")
        
        return [
            CustomSearchResult(
                item.get("title", ""),
                item.get("htmlTitle", ""),
                item.get("link", ""),
                item.get("displayLink", "")
            )
            for item in search_response[:MAX_RESULTS]
        ]
    except requests.RequestException as e:
        print(f"Search error: {str(e)}")
        return []


if __name__ == "__main__":
    # Example query to test the search function
    query = "Recent Kerala floods incident"
    results = custom_search(query)
    for result in results:
        print(result)
