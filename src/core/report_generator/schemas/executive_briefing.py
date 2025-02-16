from typing import List, Literal, Union
from pydantic import Field, BaseModel
from enum import StrEnum, auto
from .common import SourcedValue


class OpportunityImpact(StrEnum):
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()


class RiskSeverity(StrEnum):
    CRITICAL = auto()
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()


class KeyOpportunity(BaseModel):
    title: str = Field(..., description="Brief title of the opportunity")
    description: str = Field(..., description="Detailed description of the opportunity")
    impact: OpportunityImpact = Field(
        ..., description="Potential impact level of the opportunity"
    )
    timeframe: str = Field(
        ..., description="Expected timeframe to realize this opportunity"
    )
    required_resources: List[str] | None = Field(
        None, description="Key resources needed to pursue this opportunity"
    )


class Risk(BaseModel):
    title: str = Field(..., description="Brief title of the risk")
    description: str = Field(..., description="Detailed description of the risk")
    severity: RiskSeverity = Field(..., description="Severity level of the risk")
    mitigation_strategy: str = Field(
        ..., description="Strategy to mitigate or manage this risk"
    )


class Recommendation(BaseModel):
    title: str = Field(..., description="Brief, actionable title of the recommendation")
    description: str = Field(
        ..., description="Detailed explanation of the recommendation"
    )
    rationale: str = Field(
        ..., description="Supporting reasoning for this recommendation"
    )
    expected_impact: str = Field(
        ..., description="Expected business impact of implementing this recommendation"
    )
    timeline: str = Field(..., description="Estimated timeline for implementation")
    required_resources: List[str] | None = Field(
        None, description="Key resources needed to implement this recommendation"
    )


class AppendixDetails(BaseModel):
    type: Literal["appendix"] = Field(
        ..., description="Type identifier for appendix content"
    )
    section: str = Field(
        ..., description="Section name or category for this appendix item"
    )
    data_key: str = Field(
        ..., description="Specific metric or data point being detailed"
    )
    data_value: str = Field(
        ..., description="Value or detailed explanation of the data point"
    )
    methodology: str | None = Field(
        None, description="Methodology used to obtain or calculate this data"
    )
    assumptions: List[str] | None = Field(
        None, description="Key assumptions made in the analysis"
    )
    limitations: List[str] | None = Field(
        None, description="Known limitations or caveats about this data"
    )


class MarketMetrics(BaseModel):
    type: Literal["market_metrics"] = Field(
        ..., description="Type identifier for market metrics"
    )
    metrics: SourcedValue = Field(..., description="Market metrics with sources")


class Opportunities(BaseModel):
    type: Literal["opportunities"] = Field(
        ..., description="Type identifier for opportunities section"
    )
    items: List[KeyOpportunity] = Field(
        ..., description="List of key business opportunities"
    )
    analysis: SourcedValue = Field(
        ..., description="Analysis of opportunities with sources"
    )


class Risks(BaseModel):
    type: Literal["risks"] = Field(..., description="Type identifier for risks section")
    items: List[Risk] = Field(..., description="List of identified risks")
    analysis: SourcedValue = Field(..., description="Analysis of risks with sources")


class Recommendations(BaseModel):
    type: Literal["recommendations"] = Field(
        ..., description="Type identifier for recommendations section"
    )
    items: List[Recommendation] = Field(
        ..., description="List of specific recommendations"
    )
    analysis: SourcedValue = Field(
        ..., description="Analysis of recommendations with sources"
    )


SectionContent = Union[
    MarketMetrics, Opportunities, Risks, Recommendations, AppendixDetails
]


class BriefingSection(BaseModel):
    title: str = Field(..., description="Title of this section")
    content: SectionContent = Field(..., description="Content of the section")


class ExecutiveBriefing(BaseModel):
    title: str = Field(..., description="Clear, specific title for the briefing")
    date: str = Field(..., description="Date of the briefing")
    executive_summary: SourcedValue = Field(
        ..., description="Comprehensive executive summary with sources"
    )
    sections: List[BriefingSection] = Field(
        ..., description="Briefing sections in any order"
    )
