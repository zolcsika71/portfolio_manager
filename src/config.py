from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: str
    base_url: str = "https://apirest.danelfin.com"

    class Config:
        env_file = ".env"
        env_prefix = "DANELFIN_"


settings = Settings()
