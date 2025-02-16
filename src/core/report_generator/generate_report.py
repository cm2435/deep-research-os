from core.clients import INNGEST_CLIENT
import inngest
from core.report_generator.schemas import (
    ReportRequest,
    ReportType,
    ExecutiveBriefingResponse,
    StrategicBriefingResponse,
    MarketIntelligenceResponse,
    DecisionSupportResponse,
    GeneralInformationResponse,
    REPORT_TYPE,
)
from core.common.llm_interface import generate_llm_response
from core.report_generator.prompts.generate_report import system_prompt, user_prompt

REPORT_TYPE_FORMAT_MAPPING = {
    ReportType.EXECUTIVE_BRIEFING: ExecutiveBriefingResponse,
    ReportType.STRATEGIC_FRAMEWORK: StrategicBriefingResponse,
    ReportType.MARKET_INTELLIGENCE: MarketIntelligenceResponse,
    ReportType.DECISION_SUPPORT: DecisionSupportResponse,
    ReportType.GENERAL_INFORMATION: GeneralInformationResponse,
}


@INNGEST_CLIENT.create_function(
    fn_id="fill-report-template",
    trigger=inngest.TriggerEvent(event="app/case/fill-report-template.requested"),
)
async def fill_report_template(
    ctx: inngest.Context, step: inngest.Step
) -> dict[str, str | list]:
    payload = ReportRequest.model_validate(ctx.event.data)
    if not payload.report_type:
        raise ValueError(
            "Report type is required and should be filled before infilling a report template"
        )

    report_format = REPORT_TYPE_FORMAT_MAPPING[payload.report_type]
    report_and_reasoning: REPORT_TYPE = await generate_llm_response(
        system_prompt=system_prompt,
        user_prompt=user_prompt.format(
            user_query=payload.user_query,
            research_cycles=payload.prior_research_cycles,
        ),
        return_type=report_format,
        model_name="o3-mini",
    )
    return report_and_reasoning.report.model_dump()
