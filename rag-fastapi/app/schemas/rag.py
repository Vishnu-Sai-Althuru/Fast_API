from pydantic import BaseModel, Field, field_validator


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)

    @field_validator("question", mode="before")
    @classmethod
    def normalize_question(cls, value):
        if not isinstance(value, str):
            return value

        normalized_value = value.strip()
        if not normalized_value:
            raise ValueError("Question cannot be empty.")

        return normalized_value


class QueryResponse(BaseModel):
    answer: str
