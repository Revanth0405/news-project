"""
This module contains all the
"""

import json

import ollama

MODEL_NAME = "llama3.2"


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


def analyse_user_query(query: str) -> str:
    """
    Analyze the user query and understand the domain, related topic and category
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
    except json.JSONDecodeError as e:
        raise ValueError(
            "Failed to parse metadata. Ensure the response is properly formatted JSON."
        ) from e

    # Return pretty-formatted JSON
    return json.dumps(metadata_json, indent=4)

if __name__ == "__main__":
    print(analyse_user_query("LA wildfires, what is the cause?"))
