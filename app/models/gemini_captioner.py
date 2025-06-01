from typing import List, Optional
import logging
from google import genai
from app.models.base_captioner import Captioner
from app.example.example import Example, CaptionExample
from app.models.constants import GEMINI_BASE_PROMPT

logger = logging.getLogger(__name__)


class GeminiCaptioner:
    def __init__(self, model_name="gemini-1.5-flash", api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key
        self.accepted_examples = [CaptionExample]

        self.default_prompt = GEMINI_BASE_PROMPT

        # Inizializza il client Gemini
        try:
            self.client = genai.Client(api_key=self.api_key)
            # self.model = genai.GenerativeModel(model_name=self.model_name)
        except Exception as e:
            logger.exception("Failed to initialize Gemini client: %s", e)
            raise

    def __call__(
        self,
        base_caption: str,
        social: str,
        mood: str = "neutral",
        examples: Optional[List[Example]] = None,
        ignore_errors: bool = True
    ) -> str:
        if examples:
            example = examples[0]
            if not isinstance(example, tuple(self.accepted_examples)):
                logger.error(f"Class {example.__class__} is not accepted. Accepted: {self.accepted_examples}")
                if not ignore_errors:
                    raise ValueError(f"Invalid example class: {example.__class__}")

            examples_text = "Here are some example captions:\n" + "\n".join(f"- {str(e)}" for e in examples)
        else:
            examples_text = "No example captions provided."

        prompt = self.default_prompt.format(
            base_caption.strip(),
            social.strip(),
            mood.strip(),
            examples_text
        )

        try:
            print("GeminiCaptioner prompt: %s", prompt)
            response = self.client.models.generate_content(model= self.model_name, contents = prompt)
            print("GeminiCaptioner response: %s", response.text)
            return response.text.strip()
        except Exception as e:
            logger.exception("GeminiCaptioner failed: %s", e)
            if not ignore_errors:
                raise e
            return "Retry"
