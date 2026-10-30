from pydantic import BaseModel, Field, field_validator


class Product(BaseModel):
    id: int
    name: str
    price: str
    category: str = Field(min_length=1)

    @field_validator("category", mode="before")
    @classmethod
    def strip_category(cls, value: object) -> object:
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Category is required.")
        return value