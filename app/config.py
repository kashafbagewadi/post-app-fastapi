from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Values come from the environment, or from .env when running outside Docker
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str
    secret_key: str
    algorithm: str
    access_token_expiration_minutes: int

settings = Settings()