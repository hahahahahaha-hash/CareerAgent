from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AI Agent Platform"
    model_name: str = "deepseek-chat"
    openai_api_key: str = ""
    base_url: str = "https://api.deepseek.com"
    class Config:
        env_file = ".env"
settings = Settings()