from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Initialize the Ollama LLM
model = OllamaLLM(model="llama3.2")

def extract_information(content: str):
    """
    Analyze the given content, remove unnecessary information, and return the refined content.
    """
    prompt = PromptTemplate(
        input_variables=["content"],
        template="""
        Analyze the content provided and remove all unnecessary or redundant information.
        Return the refined content while retaining the original meaning and key details without summarising it.
        {content}
        """
    )

    chain = prompt | model

    return chain.invoke({'content' : content})