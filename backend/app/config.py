from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    nvidia_api_key: str = ""
    nvidia_model: str = "meta/llama-3.1-8b-instruct"
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    chunk_size: int = 800
    chunk_overlap: int = 120
    retriever_k: int = 4

    llm_temperature: float = 0.2
    llm_max_tokens: int = 1024

    data_dir: str = "data"

    allowed_origins: str = "http://localhost:5173"
    reindex_token: str = "change-me"

    # Self-ping keep-alive (comma-separated URLs, active window in IST hours [start, end))
    self_ping_urls: str = ""
    self_ping_interval_seconds: int = 600
    self_ping_start_hour_ist: int = 7
    self_ping_end_hour_ist: int = 13

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    @property
    def self_ping_url_list(self) -> list[str]:
        return [u.strip() for u in self.self_ping_urls.split(",") if u.strip()]


settings = Settings()
