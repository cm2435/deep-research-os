from pydantic import BaseModel
from .report_types import ReportType
from core.common.schemas import ResearchCycle


class ReportRequest(BaseModel):
    user_query: str
    prior_research_cycles: list[ResearchCycle]
    report_type: ReportType | None
