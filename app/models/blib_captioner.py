import logging

from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor

from app.models.constants import BLIP_DEFAULT_MODEL

logger = logging.getLogger(__name__)


class BlipCaptioner:
    def __init__(self, model_name=BLIP_DEFAULT_MODEL):
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)

    def __call__(self, image_path: str) -> str:
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(image, return_tensors="pt")
        out = self.model.generate(**inputs)
        print(out)
        return self.processor.decode(out[0], skip_special_tokens=True)
