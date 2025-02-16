from core.research.search import search
from core.research.summary import answer_question_from_search_results
from core.clients import INNGEST_CLIENT
import functools
import inngest
from typing import Callable, Awaitable
from core.research.schemas import (
    QuestionRequests,
    QuestionRequestWithId,
    Answer,
    SearchResponse,
    AnswerResponses,
)
from core.evaluation import generate_critic_response
from core.evaluation.schemas import CriticRequest
from core.research.schemas import QuestionAndAnswer, QuestionAnswerPairs


@INNGEST_CLIENT.create_function(
    fn_id="answer-single-question",
    trigger=inngest.TriggerEvent(event="app/case/answer-single-question.requested"),
    concurrency=[inngest.Concurrency(limit=5)],
)
async def answer_single_question(
    ctx: inngest.Context, step: inngest.Step
) -> dict[str, str | list]:
    question = QuestionRequestWithId.model_validate(ctx.event.data)

    search_results: list[dict] = await step.run(
        f"search-web-for-question-{question.query}",
        functools.partial(
            search,
            query=question.query,
            num_results=question.num_results,
            return_results_from=question.return_results_from,
            domain=question.domain,
        ),
    )
    parsed_search_results = [
        SearchResponse.model_validate(result) for result in search_results
    ]

    summary: Answer = await answer_question_from_search_results(
        question.query, parsed_search_results
    )
    return summary.model_dump()


@INNGEST_CLIENT.create_function(
    fn_id="batch-answer-questions",
    trigger=inngest.TriggerEvent(event="app/case/batch-answer-questions.requested"),
)
async def batch_answer_questions(
    ctx: inngest.Context, step: inngest.Step
) -> dict[str, list[dict]]:
    payload = QuestionRequests.model_validate(ctx.event.data)
    most_recent_research_cycle = payload.prior_research_cycles[-1]
    single_question_parallel_steps = tuple[Callable[[], Awaitable[dict]]]()

    for question_idx, question in enumerate(payload.questions):
        single_question_parallel_steps += tuple(
            [
                functools.partial(
                    step.invoke,
                    f"answer-question-id-{question_idx}-question-{question.query}",
                    function=answer_single_question,
                    data=question.model_dump(),
                )
            ]
        )

    single_question_result: list[dict] = await step.parallel(
        single_question_parallel_steps  # type: ignore
    )

    parsed_question_results = AnswerResponses(
        answers=[Answer.model_validate(result) for result in single_question_result]
    )
    question_answer_pairs = QuestionAnswerPairs(
        question_answer_pairs=[
            QuestionAndAnswer(question=question, answer=answer)
            for question, answer in zip(
                payload.questions, parsed_question_results.answers
            )
        ]
    )
    most_recent_research_cycle.question_answer_pairs = (
        question_answer_pairs.pretty_print()
    )

    await step.invoke(
        "critic-research-cycle",
        function=generate_critic_response,
        data=CriticRequest(
            user_query=payload.user_query,
            prior_research_cycles=payload.prior_research_cycles,
            max_research_cycles=payload.max_research_cycles,
            report_type=payload.report_type,
        ).model_dump(),
    )
    return parsed_question_results.model_dump()
