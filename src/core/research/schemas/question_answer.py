from pydantic import BaseModel, Field


class Citation(BaseModel):
    number: int = Field(
        ...,
        description="The reference number of the inline citation provided in the summary",
    )
    author: str = Field(..., description="The author of the citation")
    source_date: str = Field(
        ...,
        description="The date of the source, in ISO 8601 format, e.g. 2025-02-08T09:55:17.235Z",
    )
    url: str | None = Field(
        None,
        description="The url of the source",
    )


class Answer(BaseModel):
    reasoning: str = Field(
        ...,
        description="Any reasoning needed to generate a synoptic, powerful summary of the search results",
    )
    summary: str = Field(
        ...,
        description="A summary of any information relevant to answering the posed question from the search results",
    )
    citations: list[Citation] = Field(
        ...,
        description="Any citations needed to make it clear where information is sourced from",
    )


class AnswerResponses(BaseModel):
    answers: list[Answer]
