from typing import List

from pydantic import BaseModel, model_validator


class Post(BaseModel):
    is_carousel: bool
    resource_path: str | List[str]
    caption: str

    @model_validator(mode="before")
    def check_resource_path(cls, values):
        resource_path = values.get("resource_path")
        is_carousel = values.get("is_carousel", False)

        if isinstance(resource_path, str) and is_carousel:
            raise ValueError(
                "resource_path must be a list of strings if is_carousel is True."
            )
        if isinstance(resource_path, list) and not is_carousel:
            for path in resource_path:
                if not isinstance(path, str):
                    raise ValueError("All items in resource_path must be strings.")
        return values
