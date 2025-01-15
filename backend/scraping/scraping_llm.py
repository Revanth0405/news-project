from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Initialize the Ollama LLM
model = OllamaLLM(model="llama3.2")

def extract_information(content: str, user_prompt: str):
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
        """
    )

    chain = prompt | model

    return chain.invoke({"content": content, "user_prompt": user_prompt})
