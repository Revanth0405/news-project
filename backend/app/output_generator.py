"""
This module contains methods related to extracting useful information
and data from raw html content
"""

from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate

# from langchain.chains import LLMChain

# Initialize the Ollama LLM
model = OllamaLLM(model="llama3.2")


def extract_information_from_html(content: str, user_prompt: str):
    """
    Analyze the given content, remove unnecessary information, and return the refined content.
    """
    prompt = PromptTemplate(
        input_variables=["content", "user_prompt"],
        template="""You are tasked with extracting specific information from the following text content: {content}
        Please follow these instructions carefully: 

        1. *Extract Information:* Only extract the information that directly matches the provided description: {user_prompt}. 
        2. *No Extra Content:* Do not include any additional text, comments, or explanations in your response. 
        3. *Empty Response:* If no information matches the description, return an empty string ('').
        4. *Direct Data Only:* Your output should contain only the data that is explicitly requested, with no other text.
        """,
    )

    chain = prompt | model

    result = chain.invoke({"content": content, "user_prompt": user_prompt})
    print(result)
    return result


def extract_useful_data_from_website_html(
    content: str, title: str, user_prompt: str
) -> str:
    prompt = PromptTemplate(
        input_variables=["content", "title", "user_prompt"],
        template="""
        Task:
            You are an intelligent assistant tasked with extracting clean, simple, and easy-to-understand English text from the provided HTML content of a news article. Your goal is to focus only on the main content of the article, ignoring any irrelevant elements such as ads, website navigation, or other non-article components. The extracted information should be clear and understandable for any man aged between 10 to 60.
        Input Parameters:
            1. **HTML Content**: The raw HTML content of the website's body, provided as a string.
            2. **Title**: The title of the article or website, which provides context about the topic.
            3. **User Prompt**: A specific request from the user about what information the user want to extract from the article.
        Instructions:
            1. Parse the HTML content and identify the main article text. The content is trimmed to focus on the main content only, but not sure about accuracy, So please ignore any non-article elements such as ads, sidebars, or navigation menus.
            2. Extract the relevant information based on the user's prompt. Ensure the extracted text is concise, clear, and written in simple English.
            3. If the user prompt is specific (e.g., "Summarize the key points" or "Explain the main event"), tailor the output to meet that request.
            4. If the user prompt is general (e.g., "Tell me what this article is about"), provide a summary of the article in simple terms.
            5. Do not include any HTML tags, links, or unnecessary formatting in the final output.
            6. Understand the content and give the response in plain english with simple format.

        Actual Inputs:
        **HTML Content**: {content}
        **Title**: {title}
        **User Prompt**: {user_prompt}
        """,
    )

    chain = prompt | model
    result = chain.invoke(
        {"content": content, "title": title, "user_prompt": user_prompt}
    )

    return result


if __name__ == "__main__":
    with open("output.html", "r") as f:
        content = ""
        for line in f.readlines():
            content += line
        result = extract_useful_data_from_website_html(
            content,
            "California wildfires: What we know about L.A.-area fires, what caused them, who is affected and more",
            "What should I know about the recent LA wildfires?",
        )
