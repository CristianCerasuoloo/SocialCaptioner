from typing import List, Optional
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from app.captioner.base_captioner import Captioner
import torch
import logging

from app.example.example import CaptionExample, Example

logger = logging.getLogger(__name__)

class BlipCaptioner(Captioner):
    def __init__(self, model_name="Salesforce/blip-image-captioning-large"):
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)
        self.defaul_conditioner = "A {} caption for this image using a {} mood. {}."
        self.accepted_examples = [CaptionExample]  # Accept all examples by default 

    def __call__(self, image_path: str, social: str, mood: str = None, examples: Optional[List[Example]] = None, ignore_errors: bool = True) -> str:
        # Assert that the given examples are among the accepted ones
        # Assume that each example of the list belongs to the same class
        if examples:
            example = examples[0]
            if issubclass(example.__class__, self.accepted_examples):
                logger.error(f"Class {example.__class__} is not accepted by this Captioner. Accepted classes: {self.accepted_examples}")
                if not ignore_errors:
                    raise ValueError(f"Class {example.__class__} is not accepted by this Captioner. Accepted classes: {self.accepted_examples}")
        image = Image.open(image_path).convert("RGB")
        if examples:
            example_condition = "Examples:\n"
            for example in examples:
                example_condition += f" {str(example)}\n"
        else:
            example_condition = ""

        if not mood:
            mood = "neutral"
        condition = self.defaul_conditioner.format(social, mood, example_condition)

        inputs = self.processor(image, condition, return_tensors="pt")
        out = self.model.generate(**inputs)
        print(out)
        return self.processor.decode(out[0], skip_special_tokens=True)
