from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    pinecone_api_key: str | None = None
    pinecone_assistant_name: str = "policy-support-agent"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
