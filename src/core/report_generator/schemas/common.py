from pydantic import BaseModel, Field
from typing import List, Literal
from enum import StrEnum, auto


class MarketMetric(BaseModel):
    name: str = Field(
        ...,
        description="Name of the metric (e.g., 'User Retention Rate', 'Total Addressable Market')",
    )
    definition: str | None = Field(
        ..., description="Precise definition of how the metric is calculated"
    )
    current_value: float | None = Field(
        None, description="Current baseline value of the metric, if available"
    )
    target_value: float = Field(
        ..., description="Target value to achieve within the specified timeframe"
    )
    measurement_frequency: str = Field(
        ...,
        description="How often the metric should be measured (e.g., 'daily', 'weekly', 'monthly')",
    )
    data_source: str = Field(
        ..., description="Specific source or tool used to measure this metric"
    )


class CompetitorInfo(BaseModel):
    name: str
    market_share: float
    strengths: List[str]
    weaknesses: List[str]
    key_technologies: List[str]


class TrendData(BaseModel):
    trend_name: str
    description: str
    impact_score: float = Field(ge=1, le=10)
    timeline: str
    supporting_evidence: List[str]


class FindingCategory(StrEnum):
    MARKET = auto()
    COMPETITIVE = auto()
    OPERATIONAL = auto()
    FINANCIAL = auto()
    TECHNICAL = auto()
    CUSTOMER = auto()


class KeyFinding(BaseModel):
    category: FindingCategory = Field(..., description="Category of the finding")
    finding: str = Field(..., description="Clear statement of the finding")
    impact: str = Field(..., description="Business impact of this finding")
    supporting_data: str | None = Field(
        None, description="Specific data points supporting this finding"
    )


class Citation(BaseModel):
    source: str = Field(
        ..., description="Name of the source (e.g. company report, research paper)"
    )
    url: str | None = Field(None, description="URL of the source if available")
    date: str = Field(..., description="Date the information was published")
    question_id: str = Field(
        ...,
        description="The question ID of the question from where the question that surfaced the information",
    )


class SourcedValue(BaseModel):
    type: Literal["sourced_value"]
    value: float | str | List[str]
    citations: list[Citation] | None = Field(
        None, description="Any citations for this information (if applicable)"
    )
    notes: str | None = Field(
        None, description="Any caveats or context about this data point"
    )
