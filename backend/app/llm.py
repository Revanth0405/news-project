"""
This module contains all the LLM-related functionality for analyzing queries and generating responses
"""

import json
import ollama
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from scraping import MyContentScraper
from output_generator import extract_information_from_html
import google_search

MODEL_NAME = "llama3.2"
MAX_RESULTS = 3  # Limit number of results to process
TIMEOUT = 30  # Increased timeout to 30 seconds
THREAD_TIMEOUT = 20  # Timeout for individual thread processing


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

def scrape_website(url: str):
    """
    Scrapes content from a given URL
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            webpage_content = response.text
            return webpage_content
        else:
            return "Failed to retrieve webpage content"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def process_search_result(result, web_contents, query):
    """
    Process a single search result and its content
    """
    try:
        content = web_contents.get(result.link, "")
        if content:
            extracted_info = extract_information_from_html(content, query)
            return {
                "title": result.title,
                "link": result.link,
                "displayLink": result.displayLink,
                "extracted_content": extracted_info
            }
    except Exception as e:
        print(f"Error processing {result.link}: {str(e)}")
    return None

def analyse_user_query(query: str) -> dict:
    """
    Analyze the user query, fetch relevant content, and generate a response
    """
    if not query:
        raise ValueError("Query cannot be empty.")

    # Prepare the prompt
    prompt = construct_user_analysis_prompt(query)
    response = ollama.chat(
        model=MODEL_NAME, messages=[{"role": "user", "content": prompt}]
    )
    metadata = response["message"]["content"]

    try:
        # Convert the response to JSON format
        metadata_json = json.loads(metadata)
        
        # Get limited search results
        search_results = google_search.custom_search(metadata_json["google_search"])[:MAX_RESULTS]
        
        if not search_results:
            print("No search results found.")
            return {"metadata": metadata_json, "search_results": [{"title": "No results", "link": "", "displayLink": "", "extracted_content": "No search results found"}]}

        # Initialize scraper and fetch content with timeout
        scraper = MyContentScraper()
        web_contents = scraper.fetch_websites(search_results)
        
        # Process results concurrently with better error handling
        formatted_results = []
        
        with ThreadPoolExecutor(max_workers=MAX_RESULTS) as executor:
            future_to_result = {
                executor.submit(process_search_result, result, web_contents, query): result 
                for result in search_results
            }
            
            for future in as_completed(future_to_result, timeout=TIMEOUT):
                try:
                    result_data = future.result(timeout=THREAD_TIMEOUT)
                    if result_data:
                        formatted_results.append(result_data)
                except TimeoutError:
                    print(f"Timeout processing a result")
                except Exception as e:
                    print(f"Error processing result: {str(e)}")

        # Return results even if some failed
        if formatted_results:
            return {
                "metadata": metadata_json,
                "search_results": formatted_results
            }
        else:
            return {
                "metadata": metadata_json,
                "search_results": [{"title": "Error", "link": "", "displayLink": "", 
                                  "extracted_content": "Failed to process search results"}]
            }

    except json.JSONDecodeError as e:
        raise ValueError(
            "Failed to parse metadata. Ensure the response is properly formatted JSON."
        ) from e
    except Exception as e:
        raise Exception(f"Error processing query: {str(e)}") from e

if __name__ == "__main__":
    result = analyse_user_query("LA wildfires, what is the cause?")
    print("\nMetadata:")
    print(json.dumps(result["metadata"], indent=2))
    print("\nSearch Results and Content:")
    for idx, item in enumerate(result["search_results"], 1):
        print(f"\n{idx}. {item['title']}")
        print(f"   URL: {item['link']}")
        print(f"   Content Summary:")
        print(f"   {item['extracted_content']}")
        print("-" * 80)
