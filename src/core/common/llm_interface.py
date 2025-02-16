from typing import Literal, Type, TypeVar
from pydantic import BaseModel
from litellm import acompletion

from core.clients import logger


SUPPORTED_MODELS = Literal["gpt-4o", "gpt-4o-mini", "claude-3.5", "o3-mini"]
T = TypeVar("T", bound=BaseModel)


async def generate_llm_response(
    system_prompt: str,
    user_prompt: str,
    model_name: SUPPORTED_MODELS,
    return_type: Type[T],
) -> T:
    logger.info(
        f"Generating summary for system prompt {system_prompt[:100]}... and user prompt {user_prompt[:100]}..."
    )
    result = await acompletion(
        model=model_name,
        response_format=return_type,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    if not result.choices[0].message.content:  # type: ignore
        raise ValueError(
            f"No parsed result from LLM for generation of {return_type.__name__} for system prompt: {system_prompt[:100]}... and user prompt: {user_prompt[:100]}..."
        )
    return return_type.model_validate_json(result.choices[0].message.content)  # type: ignore
