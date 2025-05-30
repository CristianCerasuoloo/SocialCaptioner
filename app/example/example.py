from pathlib import Path
from pydantic import BaseModel


class Example(BaseModel):
    """
    Example class for captioning.
    """

    image: Path | None = None
    text: str | None = None

class CaptionExample(Example):
    """
    Example class for captioning.
    """
    text: str
    image: Path = None
    
    def __str__(self):
        return self.text

class ImageCaptionExample(Example):
    """
    Example class for image captioning.
    """
    text: str
    image: Path
    
    def __str__(self):
        return self.text



    