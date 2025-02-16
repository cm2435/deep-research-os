from core.search_planner.schemas import SearchPlanRequest, SearchPlanResponse
from core.search_planner.prompts import system_prompt, user_prompt
from core.common.llm_interface import generate_llm_response


async def formulate_questions(
    request: SearchPlanRequest,
) -> dict[str, str | list[dict]]:
    formatted_user_prompt = user_prompt.format(
        user_query=request.user_query,
        prior_research_cycles="\n".join(
            [cycle.pretty_print() for cycle in request.prior_research_cycles],
        )
        if request.prior_research_cycles
        else "No prior research cycles have been conducted yet",
        recommended_focus=request.recommended_focus
        if request.recommended_focus
        else "No recommended focus, please assertain this yourself",
    )
    response: SearchPlanResponse = await generate_llm_response(
        system_prompt, formatted_user_prompt, "o3-mini", SearchPlanResponse
    )
    return response.model_dump()
