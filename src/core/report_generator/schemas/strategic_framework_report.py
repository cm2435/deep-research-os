from typing import List, Literal, Union
from pydantic import Field, BaseModel
from enum import StrEnum, auto
from .common import SourcedValue


class PorterDimension(StrEnum):
    SUPPLIER_POWER = auto()
    BUYER_POWER = auto()
    COMPETITIVE_RIVALRY = auto()
    THREAT_OF_SUBSTITUTES = auto()
    THREAT_OF_NEW_ENTRANTS = auto()


class MatrixQuadrant(StrEnum):
    STAR = auto()
    QUESTION_MARK = auto()
    CASH_COW = auto()
    DOG = auto()


class SWOTSection(BaseModel):
    type: Literal["swot"]
    strengths: SourcedValue = Field(
        ..., description="Organizational strengths with evidence"
    )
    weaknesses: SourcedValue = Field(
        ..., description="Organizational weaknesses with evidence"
    )
    opportunities: SourcedValue = Field(
        ..., description="Market opportunities with evidence"
    )
    threats: SourcedValue = Field(..., description="Market threats with evidence")
    analysis: SourcedValue = Field(
        ..., description="Overall SWOT analysis with sources"
    )


class PorterForceItem(BaseModel):
    score: SourcedValue = Field(..., description="Force rating with evidence")
    rationale: SourcedValue = Field(
        ..., description="Explanation of rating with sources"
    )
    key_factors: SourcedValue = Field(
        ..., description="Key contributing factors with sources"
    )


class PorterForcesSection(BaseModel):
    type: Literal["porter_forces"]
    dimension: PorterDimension = Field(..., description="The dimension of the force")
    forces: list[PorterForceItem] = Field(..., description="Analysis of each force")
    analysis: SourcedValue = Field(
        ..., description="Overall Porter's Five Forces analysis"
    )


class MatrixProduct(BaseModel):
    product_name: str = Field(..., description="The name of the product")
    market_growth: SourcedValue = Field(
        ..., description="Market growth rate with sources"
    )
    market_share: SourcedValue = Field(
        ..., description="Relative market share with sources"
    )
    revenue: SourcedValue = Field(..., description="Current revenue with sources")
    quadrant: MatrixQuadrant = Field(..., description="Assigned quadrant")
    rationale: SourcedValue = Field(..., description="Reasoning for quadrant placement")


class GrowthShareMatrixSection(BaseModel):
    type: Literal["growth_share_matrix"]
    products: list[MatrixProduct] = Field(..., description="Product portfolio analysis")
    analysis: SourcedValue = Field(..., description="Overall portfolio analysis")


class CompetitivePosition(BaseModel):
    type: Literal["competitive_position"]
    market_position: SourcedValue = Field(
        ..., description="Current market position assessment"
    )
    key_advantages: SourcedValue = Field(
        ..., description="Competitive advantages analysis"
    )
    key_challenges: SourcedValue = Field(
        ..., description="Competitive challenges analysis"
    )
    analysis: SourcedValue = Field(
        ..., description="Overall competitive position analysis"
    )


class MarketTrends(BaseModel):
    type: Literal["market_trends"]
    trends: SourcedValue = Field(..., description="Key market trends with evidence")
    implications: SourcedValue = Field(
        ..., description="Business implications of trends"
    )
    analysis: SourcedValue = Field(..., description="Overall market trends analysis")


class StrategicImplications(BaseModel):
    type: Literal["strategic_implications"]
    short_term: SourcedValue = Field(
        ..., description="Short-term strategic implications"
    )
    long_term: SourcedValue = Field(..., description="Long-term strategic implications")
    key_recommendations: SourcedValue = Field(
        ..., description="Key strategic recommendations"
    )
    analysis: SourcedValue = Field(
        ..., description="Overall strategic implications analysis"
    )


SectionContent = Union[
    SWOTSection,
    PorterForcesSection,
    GrowthShareMatrixSection,
    CompetitivePosition,
    MarketTrends,
    StrategicImplications,
]


class FrameworkSection(BaseModel):
    title: str = Field(..., description="Section title")
    content: SectionContent = Field(..., description="Section content")


class StrategicFrameworkReport(BaseModel):
    title: str = Field(..., description="Report title")
    date: str = Field(..., description="Report date")
    executive_summary: SourcedValue = Field(
        ..., description="Executive summary with sources"
    )
    sections: List[FrameworkSection] = Field(..., description="Report sections")
