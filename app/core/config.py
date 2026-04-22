from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Hermes Memory"
    app_env: str = "local"
    app_debug: bool = False
    api_v1_prefix: str = "/api/v1"

    database_url: str = "postgresql+psycopg://hermes:hermes@localhost:5432/hermes_memory"
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    opensearch_url: str = "http://localhost:9200"
    opensearch_index_chunks: str = "hermes_chunks"

    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "hermes"
    minio_secret_key: str = "hermes-secret"
    minio_bucket_documents: str = "hermes-documents"
    minio_secure: bool = False
    storage_backend: str = "local"
    local_storage_path: str = "./storage/documents"

    vector_store_provider: str = "qdrant"
    vector_dimension: int = 1024
    vector_store_url: str | None = None
    vector_store_api_key: str | None = None

    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    qdrant_collection: str = "hermes_chunks"
    qdrant_vector_size: int = 1024

    embedding_provider: str = "aliyun"
    aliyun_embedding_api_key: str | None = None
    aliyun_embedding_base_url: str = "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding"
    aliyun_embedding_model: str = "text-embedding-v3"
    aliyun_embedding_dimension: int = 1024

    rerank_provider: str = "noop"
    rerank_url: str | None = None
    rerank_enabled: bool = False
    rerank_default_enablement_enabled: bool = False
    rerank_default_enablement_source_types: str = "tender"
    rerank_default_enablement_route_types: str = "tender,tender_qa,tender_query"
    rerank_default_enablement_keywords: str = "资质,要求,条款,截止,联合体,投标,招标,开标,答疑,评分,保证金"
    rerank_default_enablement_min_candidates: int = 2
    rerank_input_cap: int = 30

    aliyun_rerank_api_key: str | None = None
    aliyun_rerank_base_url: str = "https://dashscope.aliyuncs.com"
    aliyun_rerank_model: str = "gte-rerank-v2"
    aliyun_rerank_timeout_ms: int = 600

    log_level: str = Field(default="INFO")
    db_auto_create_tables: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
