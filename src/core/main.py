from core.search_planner.schemas import SearchPlanRequest
from core.search_planner.main import generate_search_plan
from core.clients import INNGEST_CLIENT
import inngest
from core.common.schemas import UserResearchRequest
from core.logger import get_logger

logger = get_logger("core.main")


@INNGEST_CLIENT.create_function(
    fn_id="initialize-research",
    trigger=inngest.TriggerEvent(event="app/case/initialize-research.requested"),
)
async def initialize_research(ctx: inngest.Context, step: inngest.Step) -> bool:
    logger.info(f"Initializing research with event: {ctx.event.data}")
    payload = UserResearchRequest.model_validate(ctx.event.data)

    await step.invoke(
        "generate-search-plan",
        function=generate_search_plan,
        data=SearchPlanRequest(
            user_query=payload.user_query,
            prior_research_cycles=[],
            max_research_cycles=payload.max_research_cycles,
            report_type=payload.report_type,
            recommended_focus=None,
        ).model_dump(),
    )

    return True
