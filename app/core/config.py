from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "smart-doc-api"
    app_env: str = "local"

    database_url: str = "postgresql+psycopg://smartdoc:smartdoc@localhost:5432/smartdoc"

    ollama_base_url: str = "http://localhost:11434"
    ocr_model: str = "scb10x/typhoon-ocr1.5-3b"
    chat_model: str = "qwen3:8b"
    embedding_model: str = "bge-m3"


@lru_cache
def get_settings() -> Settings:
    return Settings()
