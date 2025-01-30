from typing import List
import os

from dotenv import load_dotenv
import requests

from helpers import CustomSearchResult
from utils.logger import get_logger


logger = get_logger(__name__)

# load env files
load_dotenv()

# API credentials
API_URL = os.getenv("CUSTOM_SEARCH_API_URL") or ""
API_KEY = os.getenv("CUSTOM_SEARCH_API_KEY") or ""
CX = os.getenv("CUSTOM_SEARCH_CX") or ""


def custom_search(query: str) -> List[CustomSearchResult]:
    """
    Searches Google using the Custom Search API for a single query.
    Returns a list of search results (items) for the query.
    """
    logger.debug("Fetching results from Google Custom Search API for query: %s", query)
    all_results: List[CustomSearchResult] = []

    params = {
        "q": f"{query} site:news OR inurl:news OR inurl:article",
        "key": API_KEY,
        "cx": CX,
    }

    try:
        response = requests.get(
            API_URL, params=params, timeout=(3, 5)
        )  # timeout (conn_timeout, read_timeout)
        response.raise_for_status()  # Raise an exception for HTTP errors
        search_response = response.json().get("items", [])
        for item in search_response:
            all_results.append(
                CustomSearchResult(
                    item.get("title", ""),
                    item.get("htmlTitle", ""),
                    item.get("link", ""),
                    item.get("displayLink", ""),
                )
            )
    except requests.exceptions.RequestException as e:
        logger.exception("Error searching for query: `%s`, with exception %s", query, e)
    except KeyError as e:
        logger.exception("Failed to search for query `%s` with exception %s", query, e)

    return all_results


if __name__ == "__main__":
    # List of queries to search
    query = "Recent Kerala floods incident"

    results = custom_search(query)
    for result in results:
        print(result)
