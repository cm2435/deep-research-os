from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "local"
    OPENAI_API_KEY: str = "na"
    ANTHROPIC_API_KEY: str = "na"
    EXA_API_KEY: str = "na"
    COHERE_API_KEY: str = "na"

    class Config:
        env_file = Path(__file__).resolve().parents[1] / ".env"


settings = Settings()
if settings.ENV == "local" and any(
    v for v in settings.model_dump().values() if v in ["na", None]
):
    print([k for k, v in settings.model_dump().items() if v in ["na", None]])

    raise ValueError("Please set all environment variables needed")
