from config import settings
from exa_py import Exa
import inngest
import logging
from core.logger import get_logger
import cohere
logger = get_logger("deep-research-service")

EXA_CLIENT = Exa(api_key=settings.EXA_API_KEY)

INNGEST_CLIENT = inngest.Inngest(
    app_id="deep-research-service",
    logger=logging.getLogger("uvicorn"),
    is_production=False
)
COHERE_CLIENT = cohere.AsyncClientV2(api_key=settings.COHERE_API_KEY)
