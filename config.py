from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str
    openai_api_key: str
    llm_provider: str = "claude"
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings();