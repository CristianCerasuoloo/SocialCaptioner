import getpass
import os
from typing import List

from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableMap
from langchain_google_genai import GoogleGenerativeAI
from pydantic import BaseModel, Field, field_validator

from app.models.blib_captioner import BlipCaptioner
from app.schemes.example import Example

# Carica le variabili dal file .env
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    gemini_api_key = getpass.getpass("Enter API key for Google Gemini: ")


# Define your desired data structure.
class ExpectedOutput(BaseModel):
    captions: List[str] = Field(
        description="""List of captions generated from the base caption and modified for the specified social media, mood and exampls (if given)."""
    )

    @field_validator("captions")
    def validate_captions(cls, v):
        if not isinstance(v, list) or not all(isinstance(item, str) for item in v):
            raise ValueError("captions must be a list of strings.")
        return v


parser = PydanticOutputParser(pydantic_object=ExpectedOutput)

blip = BlipCaptioner()
llm = GoogleGenerativeAI(model="models/gemini-1.5-flash", api_key=gemini_api_key)


system_template = (
    "Using a provided basic caption, rephrase it to be the caption for {social} post with a {mood} mood.{optional_context}\
    Return only a valid JSON object as specified.\n\n{format_instructions}"
)

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{base_caption}")]
).partial(format_instructions=parser.get_format_instructions())


# Step 1 – Runnable per estrarre la caption dall'immagine
blip_runnable = RunnableLambda(lambda x: {"base_caption": blip(x["image_path"])})

# Step 2 – Unione base_caption + altri parametri in un unico dizionario
merge_inputs = RunnableMap(
    {
        "base_caption": blip_runnable,
        "social": lambda x: x["social"],
        "mood": lambda x: x["mood"],
        "optional_context": lambda x: x["optional_context"],
    }
)

# Step 3 – Prompt e chain finale
chain = merge_inputs | prompt_template | llm | parser


def captioning(image_path, social, mood, user_context="", examples: List[Example] = []):
    optional_context = ""
    if user_context != "":
        optional_context = (
            f" Take into account the context provided by the user: {user_context}."
        )

    if examples:
        example_captions = [example.caption for example in examples]
        optional_context += f" Also consider the following examples: {', '.join(f'{example_captions}\n')}."

    response = chain.invoke(
        {
            "social": social,
            "mood": mood,
            "image_path": image_path,
            "optional_context": optional_context,
        }
    )
    captions = response.captions
    if not captions:
        return []
    return captions
