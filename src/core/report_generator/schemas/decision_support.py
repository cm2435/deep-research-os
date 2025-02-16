from typing import List, Literal, Union
from pydantic import Field, BaseModel
from enum import StrEnum, auto
from .common import SourcedValue


class RiskSeverity(StrEnum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()


class RiskProbability(StrEnum):
    UNLIKELY = auto()
    POSSIBLE = auto()
    LIKELY = auto()
    VERY_LIKELY = auto()


class StrategicOption(BaseModel):
    name: str = Field(..., description="Name for the strategic option")
    description: SourcedValue = Field(
        ..., description="Detailed explanation of the strategic option"
    )
    reach: SourcedValue = Field(
        ..., description="Number of people impacted by this option"
    )
    impact: SourcedValue = Field(..., description="Impact score from 0.0 to 3.0")
    confidence: SourcedValue = Field(
        ..., description="Confidence percentage in estimates"
    )
    effort: SourcedValue = Field(..., description="Estimated person-months required")


class RiskLevel(BaseModel):
    description: SourcedValue = Field(
        ..., description="Description of the risk and potential impact"
    )
    severity: RiskSeverity = Field(..., description="Assessment of negative impact")
    probability: RiskProbability = Field(
        ..., description="Likelihood of risk occurring"
    )
    mitigation_strategy: SourcedValue = Field(
        ..., description="Actions to prevent or minimize risk"
    )


class MarketEvidence(BaseModel):
    finding: SourcedValue = Field(..., description="Key market finding or insight")
    relevance: SourcedValue = Field(..., description="Relevance to problem statement")


class ImplementationPhase(BaseModel):
    name: str = Field(..., description="Name of implementation phase")
    duration: SourcedValue = Field(..., description="Duration in months")
    dependencies: SourcedValue = Field(..., description="Required preceding phases")
    deliverables: SourcedValue = Field(..., description="Outputs or milestones")
    resources_required: SourcedValue = Field(..., description="Required resources")


# Section Content Types
class ProblemStatement(BaseModel):
    type: Literal["problem_statement"]
    content: SourcedValue = Field(..., description="Problem statement with sources")


class MarketEvidenceSection(BaseModel):
    type: Literal["market_evidence"]
    items: List[MarketEvidence] = Field(..., description="Market evidence items")
    analysis: SourcedValue = Field(..., description="Analysis of market evidence")


class StrategicOptionsSection(BaseModel):
    type: Literal["strategic_options"]
    items: List[StrategicOption] = Field(..., description="Strategic options")
    analysis: SourcedValue = Field(..., description="Analysis of options")


class RecommendationSection(BaseModel):
    type: Literal["recommendation"]
    content: SourcedValue = Field(..., description="Recommendation with sources")


class ImplementationSection(BaseModel):
    type: Literal["implementation"]
    phases: list[ImplementationPhase] = Field(..., description="Implementation phases")
    analysis: SourcedValue = Field(..., description="Implementation analysis")


class RiskAnalysisSection(BaseModel):
    type: Literal["risk_analysis"]
    risks: list[RiskLevel] = Field(..., description="Risk assessments")
    analysis: SourcedValue = Field(..., description="Risk analysis")


class MetricsSection(BaseModel):
    type: Literal["metrics"]
    metrics: List[SourcedValue] = Field(..., description="Success metrics with sources")


class StakeholdersSection(BaseModel):
    type: Literal["stakeholders"]
    stakeholders: SourcedValue = Field(..., description="Key stakeholders with sources")
    analysis: SourcedValue = Field(..., description="Stakeholder analysis")


class TimelineBudgetSection(BaseModel):
    type: Literal["timeline_budget"]
    timeline: SourcedValue = Field(..., description="Total timeline in months")
    budget: SourcedValue = Field(..., description="Total budget in USD")
    analysis: SourcedValue = Field(..., description="Timeline and budget analysis")


SectionContent = Union[
    ProblemStatement,
    MarketEvidenceSection,
    StrategicOptionsSection,
    RecommendationSection,
    ImplementationSection,
    RiskAnalysisSection,
    MetricsSection,
    StakeholdersSection,
    TimelineBudgetSection,
]


class DecisionSection(BaseModel):
    title: str = Field(..., description="Section title")
    content: SectionContent = Field(..., description="Section content")


class DecisionSupportReport(BaseModel):
    title: str = Field(..., description="Report title")
    date: str = Field(..., description="Report date")
    executive_summary: SourcedValue = Field(
        ..., description="Executive summary with sources"
    )
    sections: List[DecisionSection] = Field(..., description="Report sections")
