from core.evaluation.schemas.critic import CriticRequest, CriticResponse
from core.evaluation.critic import _generate_critic_response
import inngest
from core.clients import INNGEST_CLIENT


@INNGEST_CLIENT.create_function(
    fn_id="generate-critic-response",
    trigger=inngest.TriggerEvent(event="app/case/generate-critic-response.requested"),
)
async def generate_critic_response(
    ctx: inngest.Context, step: inngest.Step
) -> dict[str, bool]:
    payload = CriticRequest.model_validate(ctx.event.data)
    response: CriticResponse = await _generate_critic_response(payload)

    if (
        not response.is_sufficient
        and len(payload.prior_research_cycles) < payload.max_research_cycles
    ):
        await step.send_event(
            step_id="generate-search-plan",
            events=inngest.Event(
                name="app/case/generate-search-plan.requested",
                data={
                    "user_query": payload.user_query,
                    "prior_research_cycles": payload.prior_research_cycles,
                    "max_research_cycles": payload.max_research_cycles,
                    "report_type": payload.report_type,
                    "recommended_focus": response.recommended_focus,
                },
            ),
        )

    else:
        await step.send_event(
            step_id="generate-report",
            events=inngest.Event(
                name="app/case/generate-report.requested",
                data={
                    "user_query": payload.user_query,
                    "prior_research_cycles": payload.prior_research_cycles,
                    "report_type": payload.report_type,
                },
            ),
        )
    return response.model_dump()
