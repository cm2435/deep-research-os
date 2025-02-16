from pydantic import BaseModel, Field
from core.research.schemas import QuestionRequest
from core.common.schemas import ResearchCycle
from core.report_generator.schemas import ReportType


class SearchPlanRequest(BaseModel):
    user_query: str = Field(
        ..., description="The ultimate user question we are doing research to answer"
    )
    prior_research_cycles: list[ResearchCycle] = Field(
        ..., description="The results of prior research cycles"
    )
    max_research_cycles: int = Field(
        ...,
        description="The maximum number of researchcycles to conduct",
    )
    report_type: ReportType | None
    recommended_focus: str | None


class SearchPlanResponse(BaseModel):
    reasoning_for_subquestions_to_answer: str = Field(
        ...,
        description="Reasoning about what knowledge gaps still exist in the research which need to be addressed to answer the user's query",
    )
    search_requests: list[QuestionRequest] = Field(
        ...,
        description="A list of questions which if answered will move us closer to answering the user's query",
    )
