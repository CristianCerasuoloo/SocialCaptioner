from typing import List

from pydantic import BaseModel, Field, field_validator


# Define your desired data structure.
class ExpectedOutput(BaseModel):
    captions: List[str] = Field(
        description="""List of captions generated from the base caption and modified for the specified social media, mood and exampls (if given)."""
    )

    @field_validator("captions")
    def validate_captions(cls, v):
        if not isinstance(v, list) or not all(isinstance(item, str) for item in v):
            raise ValueError("captions must be a list of strings.")
        return v
