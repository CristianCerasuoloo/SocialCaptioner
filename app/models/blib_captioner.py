from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class BlipCaptioner:
    def __init__(self, model_name="Salesforce/blip-image-captioning-large"):
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)

    def __call__(self, image_path: str) -> str:
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(image, return_tensors="pt")
        out = self.model.generate(**inputs)
        print(out)
        return self.processor.decode(out[0], skip_special_tokens=True)
