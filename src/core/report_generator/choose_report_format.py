from core.common.llm_interface import generate_llm_response
from core.report_generator.prompts.choose_report_format import (
    system_prompt,
    user_prompt,
)
from core.common.schemas import ResearchCycle
from core.report_generator.schemas import ChoiceOfReportFormat, ReportType


async def choose_report_format(
    user_query: str,
    research_cycles: list[ResearchCycle],
) -> ReportType:
    choice_of_report_format_and_reasoning: ChoiceOfReportFormat = (
        await generate_llm_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt.format(
                user_query=user_query,
                research_cycles="\n".join(
                    [cycle.pretty_print() for cycle in research_cycles]
                ),
            ),
            model_name="o3-mini",
            return_type=ChoiceOfReportFormat,
        )
    )
    return choice_of_report_format_and_reasoning.model_dump()
