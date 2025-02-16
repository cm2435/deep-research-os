from pydantic import BaseModel, Field
from core.common.schemas import ResearchCycle
from core.report_generator.schemas import ReportType


class CriticRequest(BaseModel):
    user_query: str = Field(
        ..., description="The ultimate user question we are doing research to answer"
    )
    prior_research_cycles: list[ResearchCycle] = Field(
        ..., description="The results of prior research cycles"
    )
    max_research_cycles: int = Field(
        ..., description="The maximum number of research cycles to conduct"
    )
    report_type: ReportType | None


class CriticResponse(BaseModel):
    reasoning: str = Field(
        ...,
        description="Reasoning about if the answered questions are sufficient to generated a comprehensive answer to the user's query",
    )
    is_sufficient: bool = Field(
        ...,
        description="Classification of we should stop doing research and generate the final report to answer the users query",
    )
    recommended_focus: str | None = Field(
        None,
        description="If the research is not sufficient, a list of areas or perspectives to prioritize if another cycle is recommended",
    )
