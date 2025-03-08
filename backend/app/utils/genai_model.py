import os
from dotenv import load_dotenv

import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 65536,
    "response_mime_type": "text/plain",
}

genai_model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp", generation_config=generation_config
)

genai_chat_session = genai_model.start_chat(history=[])
