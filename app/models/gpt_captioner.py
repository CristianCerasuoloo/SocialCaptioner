from typing import List, Optional

from app.models.constants import OPENAI_BASE_PROMPT
import openai
import logging
from app.example.example import Example, CaptionExample

logger = logging.getLogger(__name__)

class OpenAICaptioner:
    """
    Works with GPT's and DeepSeek's API to generate captions.
    """
    def __init__(self, model_name="deepseek-chat", api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key
        self.accepted_examples = [CaptionExample]
        self.default_prompt = OPENAI_BASE_PROMPT

    def __call__(
        self,
        base_caption: str,
        social: str,
        mood: str = "neutral",
        examples: Optional[List[Example]] = None,
        ignore_errors: bool = True
    ) -> str:

        # Verifica del tipo di esempio
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
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=100,
            )
            caption = response.choices[0].message.content.strip()
            return caption
        except Exception as e:
            logger.exception("GPTCaptioner failed: %s", e)
            if not ignore_errors:
                raise e
            return "Retry"  # fallback
