from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Required first — no defaults, app won't start without these
    anthropic_api_key: str
    openai_api_key: str
    database_url: str

    # Optional second — have defaults, app starts fine without these in .env
    app_name: str = "LedgerMind"
    app_version: str = "0.1.0"
    llm_provider: str = "claude"
    api_version: str = "v1"

    class Config:
        env_file = ".env"


settings = Settings()
