# portfolio_manager/src/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str = "DANELFIN_API_KEY"  # Required
    base_url: str = "https://apirest.danelfin.com"

    class Config:
        env_file = ".env"
        env_prefix = "DANELFIN_"


settings = Settings()

# Validate API Key presence
if not settings.api_key:
    raise ValueError("API Key is missing. Ensure DANELFIN_API_KEY is set in the .env file.")

