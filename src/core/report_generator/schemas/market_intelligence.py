from typing import List, Literal, Union
from pydantic import Field, BaseModel
from enum import StrEnum, auto

from .common import Citation, SourcedValue


class CompetitorCategory(StrEnum):
    DIRECT = auto()
    INDIRECT = auto()
    EMERGING = auto()
    POTENTIAL = auto()


class MetricCategory(StrEnum):
    PRODUCT = auto()
    MARKET = auto()
    FINANCIAL = auto()
    TECHNICAL = auto()
    OPERATIONAL = auto()
    CUSTOMER = auto()


class TechnologyCategory(StrEnum):
    CORE = auto()
    ADJACENT = auto()
    TRANSFORMATIONAL = auto()
    EMERGING = auto()


class Competitor(BaseModel):
    name: str = Field(..., description="Company name")
    category: CompetitorCategory = Field(..., description="Type of competitor")
    description: SourcedValue | None = Field(
        None, description="Brief description with source"
    )
    key_strengths: SourcedValue | None = Field(
        None, description="Main competitive advantages with sources"
    )
    key_weaknesses: SourcedValue | None = Field(
        None, description="Notable competitive disadvantages with sources"
    )
    market_share: SourcedValue | None = Field(
        None, description="Estimated market share percentage with source"
    )
    annual_revenue: SourcedValue | None = Field(
        None, description="Annual revenue with source"
    )
    target_segments: SourcedValue | None = Field(
        None, description="Primary market segments with sources"
    )
    last_updated: str = Field(
        ..., description="When this competitor data was last verified"
    )


class CompetitiveHeatmap(BaseModel):
    type: Literal["competitive_heatmap"]
    competitors: List[Competitor] = Field(
        ..., description="List of competitors being analyzed"
    )
    methodology: Citation = Field(
        ..., description="Description and source of scoring methodology"
    )
    analysis: SourcedValue = Field(
        ..., description="An overall analysis with sources (over 100 words)"
    )
    data_quality_score: float = Field(
        ..., description="Overall quality score of data sources (0-1)"
    )
    source_coverage: float = Field(
        ..., description="Percentage of data points with primary sources"
    )


class TechnologyRadarItem(BaseModel):
    name: str = Field(..., description="Name of the technology")
    category: TechnologyCategory = Field(..., description="Category of technology")
    maturity: SourcedValue = Field(
        ..., description="Current maturity level with source"
    )
    adoption_timeline: SourcedValue = Field(
        ..., description="Expected adoption timeline with source"
    )
    business_impact: SourcedValue = Field(
        ..., description="Potential business impact with source"
    )
    investment_required: SourcedValue = Field(
        ..., description="Required investment level with source"
    )
    risk_level: SourcedValue = Field(
        ..., description="Associated risk level with source"
    )
    sources_consulted: List[Citation] = Field(
        ..., description="All sources used for this assessment"
    )


class TechnologyRadarSection(BaseModel):
    category: TechnologyCategory = Field(..., description="Category of technologies")
    items: List[TechnologyRadarItem] = Field(
        ..., description="Technologies in this category"
    )
    methodology: Citation = Field(
        ..., description="Methodology used for this category's assessment"
    )


class TechnologyRadar(BaseModel):
    type: Literal["technology_radar"]
    sections: List[TechnologyRadarSection] = Field(
        ..., description="Technology sections by category"
    )


class MissingDataSection(BaseModel):
    type: Literal["missing_data"]
    items: List[str] = Field(
        ...,
        description="List of important data points where reliable sources couldn't be found",
    )


# Union type for section content
SectionContent = Union[
    CompetitiveHeatmap, TechnologyRadar, SourcedValue, MissingDataSection
]


class ReportSection(BaseModel):
    title: str = Field(..., description="Title of this section")
    content: SectionContent = Field(..., description="Content of the section")


class MarketIntelligenceReport(BaseModel):
    title: str = Field(
        ..., description="Clear, specific title for the report (10-200 characters)"
    )
    date: str = Field(..., description="Date of report generation")
    executive_summary: SourcedValue = Field(
        ...,
        description="Brief summary of key findings with sources (100-1000 characters)",
    )
    sections: List[ReportSection] = Field(
        ..., description="Report sections in any order"
    )
