from core.clients import INNGEST_CLIENT
import inngest
from core.report_generator.schemas import ReportRequest, ChoiceOfReportFormat
from core.report_generator.choose_report_format import choose_report_format
from core.report_generator.generate_report import fill_report_template


@INNGEST_CLIENT.create_function(
    fn_id="generate-report",
    trigger=inngest.TriggerEvent(event="app/case/generate-report.requested"),
)
async def generate_report(
    ctx: inngest.Context, step: inngest.Step
) -> dict[str, str | list]:
    payload = ReportRequest.model_validate(ctx.event.data)
    report_type = payload.report_type
    if not report_type:
        report_type_and_reasoning = await step.run(
            "choose-report-format",
            choose_report_format,
            payload.user_query,
            payload.prior_research_cycles,
        )
        parsed_report_type_and_reasoning = ChoiceOfReportFormat.model_validate(
            report_type_and_reasoning
        )
        payload.report_type = parsed_report_type_and_reasoning.chosen_format

    report = await step.invoke(
        step_id="fill-report-template",
        function=fill_report_template,
        data=payload.model_dump(),
    )

    return report
