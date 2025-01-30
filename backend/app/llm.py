"""
This module contains all the LLM-related functionality for analyzing queries and generating responses
"""

import json
import ollama
import google_search
from helpers import CustomSearchResult
from scraping import MyContentScraper
from output_generator_gemini import extract_information_from_website

MODEL_NAME = "llama3.2"
MAX_RESULTS = 10  # Limit number of results to process


def construct_user_analysis_prompt(query: str):
    """
    This constructs a prompt for our model for our query, attaching some extra
    data for better context understanding for the model.
    """
    prompt = f"""
        I have the user query: "{query}".
        The user wants to know the metadata of the query.
        Provide the metadata in JSON format with the following keys:

        1. "related_topic": The primary topic or subject that the query is referring to. Be concise and specific.
        2. "latest_news": A boolean indicating whether the user is asking for the latest news (true) or older information (false). 
        3. "category": A list of one or more related categories from the following: 
           ["India", "World", "Sports", "Business", "Technology", "Entertainment", "Cricket", "Science", "Environment", "Tech", "Education", "Life & Style", "Astrology"].
        4. "google_search": Exactly one highly relevant Google search phrases based on the query that will yield the most accurate results.

        Ensure:
        - The "related_topic" is short and accurate.
        - The "category" field contains only valid categories from the given list, and includes multiple relevant categories if applicable.
        - The "google_search" field contains clear and effective search terms that align with the user's intent.
        
        Respond **only** with a properly formatted JSON object without any additional text.
    """
    return prompt


def analyse_user_query(query: str) -> dict:
    """
    Analyze the user query, fetch relevant content, and generate a response
    """
    if not query:
        raise ValueError("Query cannot be empty.")

    # Prepare the prompt
    prompt = construct_user_analysis_prompt(query)

    # Send the prompt to the model
    response = ollama.chat(
        model=MODEL_NAME, messages=[{"role": "user", "content": prompt}]
    )

    # Extract metadata from the response
    metadata = response["message"]["content"]

    try:
        # Convert the response to JSON format
        metadata_json = json.loads(metadata)

        # Get limited search results
        search_results = google_search.custom_search(metadata_json["google_search"])[:MAX_RESULTS]

        if not search_results:
            print("No search results found.")
            return {"metadata": metadata_json, "search_results": [{"title": "No results", "link": "", "displayLink": "", "extracted_content": "No search results found"}]}

        # Initialize scraper and fetch content
        scraper = MyContentScraper()
        web_contents = scraper.fetch_websites(search_results)

        # Now we need to extract the information from the web_contents

        # Print the content of the web_contents dictionary
        for url, content in web_contents.items():
            print(f"URL: {url}")
            print("Content:")
            print(extract_information_from_website(content, query))
            print("-" * 80)

        # Extract information from the fetched content
        formatted_results = [
            {
                "title": result.title,
                "link": result.link,
                "displayLink": result.displayLink,
                "extracted_content": "extract_information_from_website(web_contents.get(result.link, ""), query)"
            }
            for result in search_results
        ]

        return {
            "metadata": metadata_json,
            "search_results": formatted_results
        }

    except json.JSONDecodeError as e:
        raise ValueError(
            "Failed to parse metadata. Ensure the response is properly formatted JSON."
        ) from e

if __name__ == "__main__":
    result = analyse_user_query("Kerala floods, what is the cause?")
    print("\nMetadata:")
    print(json.dumps(result["metadata"], indent=2))
    print("\nSearch Results and Content:")
    for idx, item in enumerate(result["search_results"], 1):
        print(f"\n{idx}. {item['title']}")
        print(f"   URL: {item['link']}")
        print(f"   Content Summary:")
        print(f"   {item['extracted_content']}")
        print("-" * 80)