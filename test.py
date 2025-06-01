import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()


gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. Please ensure you have a .env file with the Gemini API key."
    )
llm = GoogleGenerativeAI(model="models/gemini-1.5-flash", api_key=gemini_api_key)

system_template = "Using this basic caption, rephrase it to be the caption for {social} post with a {mood} mood."

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{base_caption}")]
)

prompt = prompt_template.invoke(
    {
        "social": "instagram",
        "mood": "funny",
        "base_caption": "there is a man sitting with a bottle of water",
    }
)
print(f"Prompt: {prompt}")
response = llm.invoke(prompt)

print(f"Response: {response}")
