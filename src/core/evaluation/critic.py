from core.evaluation.schemas.critic import CriticRequest, CriticResponse
from core.evaluation.prompts import system_prompt, user_prompt
from core.common.llm_interface import generate_llm_response


async def _generate_critic_response(request: CriticRequest) -> CriticResponse:
    formatted_user_prompt = user_prompt.format(
        user_query=request.user_query,
        prior_research_cycles="\n".join(
            [cycle.pretty_print() for cycle in request.prior_research_cycles]
        ),
    )
    response: CriticResponse = await generate_llm_response(
        system_prompt, formatted_user_prompt, "o3-mini", CriticResponse
    )
    return response
