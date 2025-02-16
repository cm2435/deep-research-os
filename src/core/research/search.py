from typing import List, Optional
from core.clients import EXA_CLIENT
import asyncio
import functools
from core.research.schemas import SearchDomain, SearchResponse
from pydantic import BaseModel
from typing import Literal
from core.clients import COHERE_CLIENT
from core.logger import get_logger

logger = get_logger("research.search")

# Original search functions remain unchanged
async def search(
    query: str, 
    num_results: int, 
    return_results_from: str, 
    domain: SearchDomain,
    maximum_length_search_result: int = 25000,
    rerank_model: Literal["rerank-v3.5", "rerank-v3.0"] | None = 'rerank-v3.5'
) -> list[dict]:
    logger.info(
        f"Starting search query='{query[:50]}...' domain={domain} num_results={num_results}"
    )
    
    loop = asyncio.get_event_loop()
    fut = loop.run_in_executor(
        None,
        functools.partial(
            _search,
            query=query,
            start_published_date=return_results_from,
            domain=domain,
            num_results=num_results,
            maximum_length_search_result=maximum_length_search_result,
        ),
    )
    result: list[SearchResponse] = await fut
    logger.info(f"Retrieved {len(result)} initial results from EXA")

    if rerank_model:
        logger.info(f"Reranking results using model {rerank_model}")
        reranked_indices = await COHERE_CLIENT.rerank(
            model=rerank_model,
            query=query,
            documents=[result.content for result in result],
            top_n=num_results,
        )
        result = [result[i.index] for i in reranked_indices.results]
    
    return [result.model_dump() for result in result]

def _search(
    query: str,
    num_results: int,
    start_published_date: str,
    domain: SearchDomain,
    maximum_length_search_result: int = 25000,
) -> list[SearchResponse]:
    logger.debug(
        f"Executing EXA search: query='{query[:50]}...' domain={domain} "
        f"date_from={start_published_date}"
    )
    
    results = EXA_CLIENT.search_and_contents(
        query,
        type="auto",
        text=True,
        start_published_date=start_published_date,
        category=domain.value,
        num_results=num_results,
    ).results
    
    logger.debug(f"Processing {len(results)} raw results from EXA")
    return [
        SearchResponse(
            content=result.text[:maximum_length_search_result],
            author=result.author if result.author else "unknown",
            domain=domain,
            published_date=result.published_date if result.published_date else "unknown",
        )
        for result in results
    ]