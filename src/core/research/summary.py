from core.research.schemas import SearchResponse, Answer
from core.research.prompts import qa_system_prompt, qa_user_prompt
from core.research.formatting import pretty_print_search_results
from core.common.llm_interface import generate_llm_response, SUPPORTED_MODELS


async def answer_question_from_search_results(
    query: str,
    search_results: list[SearchResponse],
    model_name: SUPPORTED_MODELS = "gpt-4o-mini",
) -> Answer:
    return await generate_llm_response(
        system_prompt=qa_system_prompt,
        user_prompt=qa_user_prompt.format(
            question=query,
            search_results=pretty_print_search_results(search_results),
        ),
        model_name=model_name,
        return_type=Answer,
    )
