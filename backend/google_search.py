from typing import List
import os

from dotenv import load_dotenv
import requests

from helper_classes.CustomSearchResult import CustomSearchResult


# load env files
load_dotenv()

# API credentials
API_URL = os.getenv("CUSTOM_SEARCH_API_URL")
API_KEY = os.getenv("CUSTOM_SEARCH_API_KEY")
CX = os.getenv("CUSTOM_SEARCH_CX")



def custom_search(query: str) -> List[CustomSearchResult]:
    """
    Searches Google using the Custom Search JSON API for a single query.
    Returns a list of search results (items) for the query.
    """
    all_results: List[CustomSearchResult] = []

    params = {
        "q": f"{query} site:news OR inurl:news OR inurl:article",
        "key": API_KEY,
        "cx": CX,
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        search_response = response.json().get("items", [])
        search_results = [
            CustomSearchResult(
                item.get("title", ""),
                item.get("htmlTitle", ""),
                item.get("link", ""),
                item.get("displayLink", ""),
            )
            for item in search_response
        ]
        all_results.extend(search_results)
    except requests.exceptions.RequestException as e:
        print(f"Error searching for query '{query}': {e}")
    except KeyError:
        print(f"No results found for query '{query}'.")

    return all_results

if __name__ == "__main__":
    # List of queries to search
    query_list = [
        "Recent Kerala floods incident"
    ]

    results = custom_search(query_list)

    # Print the search results
    if results:
        for result in results:
            print(result)
    else:
        print("No search results found.")
