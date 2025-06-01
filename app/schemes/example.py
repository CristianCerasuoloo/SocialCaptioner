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
