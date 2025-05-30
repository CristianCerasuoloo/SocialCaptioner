from app.example.example import Example
from typing import List, Optional

class Captioner:
    """
    Base class for caption
    """

    def __init__(self):
        """
        Initialize the captioner.
        """
        self.default_conditioner = "A caption for this image is"
        self.accepted_examples = []  # List of accepted example classes

    def __call__(self, image_path: str, examples: Optional[List[Example]] = None) -> str:
        """
        Generate a caption for the given image.

        :param image_path: Path to the image file.
        :param examples: List of examples to personalize the caption.
        :return: Generated caption as a string.
        """
        raise NotImplementedError("Subclasses should implement this method.")