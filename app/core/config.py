from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Resume Agent"
    ENV: str = "development"
    API_PREFIX: str = "/api/v1"

    # Optional LLM credentials used only for the "optimize" agent step.
    # All other features work fully offline without these set.
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    MAX_UPLOAD_SIZE_MB: int = 5

    class Config:
        env_file = ".env"


settings = Settings()
