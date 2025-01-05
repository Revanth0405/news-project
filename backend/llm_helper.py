import ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

model_name = "llama3.2"

def extract_meta_info(query):
    # Extract metadata from the query -- related topic, latest or oldest topic, category of news
    prompt = f"""
        I have the user query: {query}
        The user wants to know the metadata of the query.
        Please provide the metadata of the query.
        Dont provide any information that is not metadata.
        The metadata should consist of the following things:
        1. Related topic of news
        2. Latest news / Oldest news
        3. Category of news
    """
    return prompt

def user_query_analysis(query):
    # Get user query
    prompt = extract_meta_info(query)
    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response['message']['content']

if __name__ == "__main__":
    query = ""
    print(user_query_analysis(query))