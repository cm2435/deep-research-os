from typing import List, Literal, Union
from pydantic import Field, BaseModel
from .common import SourcedValue


class InsightEvidence(BaseModel):
    description: SourcedValue = Field(..., description="Description of the evidence")
    data: SourcedValue | None = Field(None, description="Supporting data or metrics")


class Insight(BaseModel):
    description: SourcedValue = Field(..., description="Statement of the insight")
    evidence: List[InsightEvidence] = Field(..., description="Supporting evidence")
    implications: SourcedValue | None = Field(
        None, description="Implications of this insight"
    )


class ContextSection(BaseModel):
    type: Literal["context"]
    content: SourcedValue = Field(..., description="Background and scope")
    analysis: SourcedValue = Field(..., description="Analysis of context")


class InsightsSection(BaseModel):
    type: Literal["insights"]
    items: List[Insight] = Field(..., description="Main insights and findings")
    analysis: SourcedValue = Field(..., description="Analysis of insights")


class ConclusionSection(BaseModel):
    type: Literal["conclusion"]
    content: SourcedValue = Field(..., description="Overall conclusions")
    implications: SourcedValue = Field(..., description="Strategic implications")
    next_steps: SourcedValue | None = Field(None, description="Recommended next steps")


class FutureConsiderationsSection(BaseModel):
    type: Literal["future_considerations"]
    trends: SourcedValue = Field(..., description="Relevant future trends")
    scenarios: SourcedValue = Field(..., description="Potential future scenarios")
    monitoring_plan: SourcedValue = Field(
        ..., description="Approach for ongoing monitoring"
    )


SectionContent = Union[
    ContextSection, InsightsSection, ConclusionSection, FutureConsiderationsSection
]


class AnalysisSection(BaseModel):
    title: str = Field(..., description="Section title")
    content: SectionContent = Field(..., description="Section content")


class GeneralInformationReport(BaseModel):
    title: str = Field(..., description="Report title")
    date: str = Field(..., description="Report date")
    summary: SourcedValue = Field(..., description="Executive summary with sources")
    sections: List[AnalysisSection] = Field(..., description="Report sections")
