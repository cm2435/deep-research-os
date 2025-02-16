from typing import Union


from pydantic import BaseModel, Field
from .report_types import ReportType
from .executive_briefing import ExecutiveBriefing
from .market_intelligence import MarketIntelligenceReport
from .strategic_framework_report import StrategicFrameworkReport
from .decision_support import DecisionSupportReport
from .general_information import GeneralInformationReport


class ChoiceOfReportFormat(BaseModel):
    reasoning: str = Field(
        description="The reasoning behind the choice of report format"
    )
    chosen_format: ReportType


class ReportBase(BaseModel):
    reasoning: str = Field(
        description="The reasoning about what information from the research to cycle, and where in the report."
    )


class ExecutiveBriefingResponse(ReportBase):
    report: ExecutiveBriefing


class MarketIntelligenceResponse(ReportBase):
    report: MarketIntelligenceReport


class StrategicBriefingResponse(ReportBase):
    report: StrategicFrameworkReport


class DecisionSupportResponse(ReportBase):
    report: DecisionSupportReport


class GeneralInformationResponse(ReportBase):
    report: GeneralInformationReport


REPORT_TYPE = Union[
    ExecutiveBriefingResponse,
    MarketIntelligenceResponse,
    StrategicBriefingResponse,
    DecisionSupportResponse,
]
