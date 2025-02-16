from pydantic import BaseModel, Field
from core.report_generator.schemas import ReportType


class UserResearchRequest(BaseModel):
    user_query: str = Field(..., description="The user's query")
    max_research_cycles: int = Field(
        default=2, description="The maximum number of research cycles to conduct"
    )
    report_type: ReportType | None = Field(
        None,
        description="The type of report to generate (eg: executive_briefing, strategic_framework, market_intelligence, decision_support)",
    )
