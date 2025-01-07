from typing import List

import requests

from helper_classes.CustomSearchResult import CustomSearchResult

# API credentials
API_KEY = "AIzaSyA_V85LyvaxhPceZneJ3tzrKRZklqcI-WA"
CX = "a10036247dff048e4"


def custom_search(query_list: List[str]) -> List[CustomSearchResult]:
    """
    Searches Google using the Custom Search JSON API for each query in the list.
    Returns a list of search results (items) for all queries.
    """
    all_results: List[CustomSearchResult] = []

    for query in query_list:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "key": API_KEY,
            "cx": CX,
        }

        try:
            response = requests.get(url, params=params)
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
        "Latest AI technologies in India",
        "Trends in AI development",
        "Emerging AI innovations in 2024",
    ]

    results = custom_search(query_list)

    # Print the search results
    if results:
        for result in results:
            print(result)
    else:
        print("No search results found.")
