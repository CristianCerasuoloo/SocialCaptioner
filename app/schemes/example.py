from pydantic import BaseModel, field_validator


class Example(BaseModel):
    """
    Example class for captioning.
    """

    caption: str

    @field_validator("caption")
    def validate_caption(cls, v):
        if not isinstance(v, str):
            raise ValueError("caption must be a non-empty string.")
        v = v.strip()
        if v[-1] != ".":
            v += "."

        return v


class ExampleFromPost(BaseModel):
    """
    Example class for captioning from a post.
    """

    image: str
    base_caption: str  # Base caption generated by BLIP
    user_caption: str  # User caption from the post
