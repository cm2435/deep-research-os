from pydantic import BaseModel, Field
from .question_request import SearchDomain


class SearchResponse(BaseModel):
    content: str
    published_date: str = Field(
        ...,
        description="The date of the search, in ISO 8601 format, e.g. 2025-02-08T09:55:17.235Z",
    )
    author: str
    domain: SearchDomain
