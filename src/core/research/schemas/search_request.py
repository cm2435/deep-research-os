from pydantic import BaseModel
from .question_request import QuestionRequestWithId
from core.common.schemas import ResearchCycle
from core.report_generator.schemas import ReportType


class QuestionRequests(BaseModel):
    user_query: str
    prior_research_cycles: list[ResearchCycle]
    questions: list[QuestionRequestWithId]
    max_research_cycles: int
    report_type: ReportType | None
