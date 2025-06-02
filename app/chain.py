import getpass
import os
from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_google_genai import GoogleGenerativeAI

from app.models.blib_captioner import BlipCaptioner
from app.schemes.example import Example, ExampleFromPost
from app.schemes.expectedoutput import ExpectedOutput
from app.schemes.post import Post


class TemplateBuilder:
    SYSTEM_BASE_PROMPT = (
        "You are a helpful assistant that generates captions for social media posts. "
        "You will be provided with a base caption and an optional additional context, and your task is to rephrase the caption "
        "to fit the a {mood} mood for the {social} social media platform. You can give more options for the caption."
        "{format_instructions}"
    )

    USER_PROMPT_TEMPLATE = "Base caption: {base_caption}\n{optional_context}\n"

    USER_POST_EXAMPLE_PROMPT_TEMPLATE = "Base caption: {base_caption}"

    ASSISTANT_POST_EXAMPLE_PROMPT_TEMPLATE = "{{'captions': '[{user_caption}]'}}"

    def __init__(self):
        self.parser = PydanticOutputParser(pydantic_object=ExpectedOutput)

    def __get_prompt(self, few_shot_prompt=None):
        if few_shot_prompt:
            messages = [
                ("system", self.SYSTEM_BASE_PROMPT),
                few_shot_prompt,
                ("user", self.USER_PROMPT_TEMPLATE),
            ]
        else:
            messages = [
                ("system", self.SYSTEM_BASE_PROMPT),
                ("user", self.USER_PROMPT_TEMPLATE),
            ]

        return ChatPromptTemplate.from_messages(messages).partial(
            format_instructions=self.parser.get_format_instructions()
        )

    def get_basic_prompt(self):
        return self.__get_prompt()

    def get_ig_posts_prompt(self, examples: List[ExampleFromPost]):
        example_prompt = ChatPromptTemplate.from_messages(
            [
                ("user", self.USER_POST_EXAMPLE_PROMPT_TEMPLATE),
                ("ai", self.ASSISTANT_POST_EXAMPLE_PROMPT_TEMPLATE),
            ]
        )
        list_dict_examples = [example.model_dump() for example in examples]
        few_shot_prompt = FewShotChatMessagePromptTemplate(
            examples=list_dict_examples,
            # This is a prompt template used to format each individual example.
            example_prompt=example_prompt,
        )

        return self.__get_prompt(few_shot_prompt)


gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    gemini_api_key = getpass.getpass("Enter API key for Google Gemini: ")


parser = PydanticOutputParser(pydantic_object=ExpectedOutput)

blip = BlipCaptioner()
llm = GoogleGenerativeAI(model="models/gemini-2.0-flash", api_key=gemini_api_key)


# Logging runnable to inspect the prompt
log_prompt_runnable = RunnableLambda(
    lambda prompt: (
        [print(f"{msg.type.upper()}: {msg.content}") for msg in prompt.to_messages()],  # type: ignore
        prompt,  # important: return the prompt unchanged so the chain continues
    )[1]  # [1] ensures we return the prompt, not the list of prints
)


def captioning(
    image_path,
    social,
    mood,
    user_context="",
    examples: List[Example] = [],
    posts: List[Post] = [],
):
    if user_context != "":
        optional_context = f"Optional context: {user_context}\n"
    else:
        optional_context = ""

    # if examples:
    #     example_captions = [example.caption for example in examples]
    #     optional_context += f"Consider the following examples for the rephrasing style: {', '.join(f'{example_captions}\n')}."

    ig_posts = []  # List to hold a dict for each post to process as ExampleFromPost if any
    if posts:
        for post in posts:
            resource_paths = (
                [post.resource_path] if not post.is_carousel else post.resource_path
            )
            for resource_path in resource_paths:
                if isinstance(resource_path, str):
                    ig_posts.append(
                        {
                            "image": resource_path,
                            "user_caption": post.caption,
                            "base_caption": blip(
                                resource_path
                            ),  # Generate base caption using BLIP
                        }
                    )

    if ig_posts:
        prompt_template = TemplateBuilder().get_ig_posts_prompt(
            [ExampleFromPost(**post) for post in ig_posts]
        )
    else:
        prompt_template = TemplateBuilder().get_basic_prompt()

    prompt_params = {
        "social": social,
        "mood": mood,
        "base_caption": blip(image_path),
        "optional_context": optional_context,
    }

    # Step 3 – Prompt e chain finale
    # chain = prompt_template | log_prompt_runnable | llm | parser
    chain = prompt_template | llm | parser

    response = chain.invoke(prompt_params)
    captions = response.captions
    if not captions:
        return []
    return captions
