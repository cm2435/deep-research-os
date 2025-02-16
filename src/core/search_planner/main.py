from core.search_planner.schemas import SearchPlanRequest, SearchPlanResponse
from core.search_planner.planning import formulate_questions
from core.research.schemas import QuestionRequests, QuestionRequestWithId
from core.research.main import batch_answer_questions
from core.clients import INNGEST_CLIENT
import inngest
import functools
from core.common.schemas import ResearchCycle
import uuid


@INNGEST_CLIENT.create_function(
    fn_id="generate-search-plan",
    trigger=inngest.TriggerEvent(event="app/case/generate-search-plan.requested"),
)
async def generate_search_plan(
    ctx: inngest.Context, step: inngest.Step
) -> dict[str, list[dict]]:
    payload = SearchPlanRequest.model_validate(ctx.event.data)
    research_cycles = payload.prior_research_cycles
    search_plan = await step.run(
        "generate-search-plan",
        functools.partial(
            formulate_questions,
            request=payload,
        ),
    )
    parsed_search_plan = SearchPlanResponse.model_validate(search_plan)
    search_requests_with_ids = [
        QuestionRequestWithId(
            **question.model_dump() | {"question_id": str(uuid.uuid4().hex)}
        )
        for question in parsed_search_plan.search_requests
    ]

    # Start a new research cycle
    research_cycles.append(
        ResearchCycle(
            question_answering_round=len(payload.prior_research_cycles) + 1,
            reasoning_for_subquestions_to_answer=parsed_search_plan.reasoning_for_subquestions_to_answer,
            question_answer_pairs=[],
            critic_reasoning_of_sufficiency=None,
            is_sufficient=None,
        )
    )
    await step.invoke(
        "batch-answer-questions",
        function=batch_answer_questions,
        data=QuestionRequests(
            user_query=payload.user_query,
            prior_research_cycles=payload.prior_research_cycles,
            questions=search_requests_with_ids,
            max_research_cycles=payload.max_research_cycles,
            report_type=payload.report_type,
        ).model_dump(),
    )

    return parsed_search_plan.model_dump()
