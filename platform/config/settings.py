"""Environment-specific settings using Pydantic for validation."""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field


# Load .env early
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

class GCPBigQuerySettings(BaseSettings):
    """Google Cloud BigQuery connection settings."""
    
    project_id: str = "scenic-style-421412"
    dataset: str = "raw"
    location: str = "us-central1"
    # project_id: str = Field(..., env="GCP_PROJECT_ID")
    # dataset: str = Field(..., env="GCP_BIGQUERY_DATASET")
    # location: str = Field("US", env="GCP_BIGQUERY_LOCATION")
    credentials_path: Optional[str] = Field(None, env="GCP_CREDENTIALS_PATH")
    # For service account JSON (can be base64 encoded or file path)
    service_account_json: Optional[str] = Field(None, env="GCP_SERVICE_ACCOUNT_JSON")
    # Use application default credentials if no explicit credentials provided
    use_adc: bool = Field(True, env="GCP_USE_ADC")
    # Job configuration
    job_timeout_seconds: int = Field(300, env="GCP_BIGQUERY_JOB_TIMEOUT")
    maximum_bytes_billed: Optional[int] = Field(None, env="GCP_BIGQUERY_MAX_BYTES_BILLED")
    priority: str = Field("INTERACTIVE", env="GCP_BIGQUERY_PRIORITY")  # INTERACTIVE or BATCH
    
    class Config:
        env_prefix = "GCP_BIGQUERY_"

# commented out for now to avoid errors
# class GCPGCSSettings(BaseSettings):
#     """Google Cloud Storage settings for document storage."""
    
#     bucket_name: str = Field(..., env="GCP_GCS_BUCKET_NAME")
#     # Buckets for different data types
#     raw_documents_bucket: Optional[str] = Field(None, env="GCP_GCS_RAW_DOCUMENTS_BUCKET")
#     processed_documents_bucket: Optional[str] = Field(None, env="GCP_GCS_PROCESSED_DOCUMENTS_BUCKET")
#     # Default to main bucket if not specified
#     location: str = Field("US", env="GCP_GCS_LOCATION")
    
#     class Config:
#         env_prefix = "GCP_GCS_"


# class VertexAISettings(BaseSettings):
#     """Vertex AI settings for embeddings and RAG."""
    
#     project_id: str = Field(..., env="GCP_PROJECT_ID")
#     location: str = Field("us-central1", env="GCP_VERTEX_AI_LOCATION")
#     # Embedding model
#     embedding_model: str = Field("textembedding-gecko@003", env="GCP_VERTEX_AI_EMBEDDING_MODEL")
#     # Vision model for multimodal processing
#     vision_model: str = Field("imagetext@001", env="GCP_VERTEX_AI_VISION_MODEL")
#     # Vector Search settings
#     vector_search_index_id: Optional[str] = Field(None, env="GCP_VECTOR_SEARCH_INDEX_ID")
#     vector_search_index_endpoint: Optional[str] = Field(None, env="GCP_VECTOR_SEARCH_INDEX_ENDPOINT")
#     # Document AI for PDF processing
#     document_ai_processor_id: Optional[str] = Field(None, env="GCP_DOCUMENT_AI_PROCESSOR_ID")
#     document_ai_location: str = Field("us", env="GCP_DOCUMENT_AI_LOCATION")
    
#     class Config:
#         env_prefix = "GCP_VERTEX_AI_"


# class GCPPubSubSettings(BaseSettings):
#     """Google Cloud Pub/Sub settings for IoT streams."""
    
#     project_id: str = Field(..., env="GCP_PROJECT_ID")
#     # IoT topic for real-time data
#     iot_topic: str = Field("iot-sensor-data", env="GCP_PUBSUB_IOT_TOPIC")
#     # Subscription for processing
#     iot_subscription: str = Field("iot-sensor-data-sub", env="GCP_PUBSUB_IOT_SUBSCRIPTION")
#     # Batch settings
#     max_messages: int = Field(100, env="GCP_PUBSUB_MAX_MESSAGES")
#     max_wait_time: int = Field(10, env="GCP_PUBSUB_MAX_WAIT_TIME")
    
#     class Config:
#         env_prefix = "GCP_PUBSUB_"


# class GCPSecuritySettings(BaseSettings):
#     """GCP security and data protection settings."""
    
#     # Cloud DLP for PII/PHI masking
#     dlp_project_id: str = Field(..., env="GCP_PROJECT_ID")
#     dlp_location: str = Field("global", env="GCP_DLP_LOCATION")
#     # Info types to detect/mask
#     dlp_info_types: str = Field("PHONE_NUMBER,EMAIL_ADDRESS,CREDIT_CARD_NUMBER,BANK_ACCOUNT", env="GCP_DLP_INFO_TYPES")
#     # IAM settings
#     service_account_email: Optional[str] = Field(None, env="GCP_SERVICE_ACCOUNT_EMAIL")
#     # RBAC - roles mapping (comma-separated)
#     rbac_roles: str = Field("viewer,editor,admin", env="GCP_RBAC_ROLES")
    
#     class Config:
#         env_prefix = "GCP_SECURITY_"


# class VectorDBSettings(BaseSettings):
#     """Vector database settings for RAG."""
    
#     # Primary vector DB (Vertex AI Vector Search or alternative)
#     provider: str = Field("vertex_ai", env="VECTOR_DB_PROVIDER")  # vertex_ai, pinecone, milvus, weaviate
#     # Vertex AI Vector Search
#     index_name: Optional[str] = Field(None, env="VECTOR_DB_INDEX_NAME")
#     dimension: int = Field(768, env="VECTOR_DB_DIMENSION")  # Default for textembedding-gecko
#     # Hybrid search settings
#     enable_hybrid_search: bool = Field(True, env="VECTOR_DB_ENABLE_HYBRID_SEARCH")
#     # BM25 settings for hybrid search
#     bm25_k1: float = Field(1.2, env="VECTOR_DB_BM25_K1")
#     bm25_b: float = Field(0.75, env="VECTOR_DB_BM25_B")
#     # Alternative providers
#     pinecone_api_key: Optional[str] = Field(None, env="PINECONE_API_KEY")
#     pinecone_environment: Optional[str] = Field(None, env="PINECONE_ENVIRONMENT")
    
#     class Config:
#         env_prefix = "VECTOR_DB_"


# class RAGSettings(BaseSettings):
#     """RAG-specific settings."""
    
#     # Chunking strategy
#     chunking_strategy: str = Field("semantic", env="RAG_CHUNKING_STRATEGY")  # semantic, recursive, fixed
#     chunk_size: int = Field(1000, env="RAG_CHUNK_SIZE")
#     chunk_overlap: int = Field(200, env="RAG_CHUNK_OVERLAP")
#     # Parent-child indexing
#     enable_parent_child: bool = Field(True, env="RAG_ENABLE_PARENT_CHILD")
#     parent_chunk_size: int = Field(5000, env="RAG_PARENT_CHUNK_SIZE")
#     # Metadata enrichment
#     enable_metadata_enrichment: bool = Field(True, env="RAG_ENABLE_METADATA_ENRICHMENT")
#     # Caching
#     enable_caching: bool = Field(True, env="RAG_ENABLE_CACHING")
#     cache_ttl_seconds: int = Field(3600, env="RAG_CACHE_TTL_SECONDS")
#     # Late interaction models (ColBERT)
#     use_late_interaction: bool = Field(False, env="RAG_USE_LATE_INTERACTION")
    
#     class Config:
#         env_prefix = "RAG_"


class DagsterSettings(BaseSettings):
    """Dagster-specific settings."""
    
    home: str = Field("/opt/dagster/dagster_home", env="DAGSTER_HOME")
    webserver_host: str = Field("0.0.0.0", env="DAGSTER_WEBSERVER_HOST")
    webserver_port: int = Field(3000, env="DAGSTER_WEBSERVER_PORT")
    telemetry_enabled: bool = Field(False, env="DAGSTER_TELEMETRY_ENABLED")
    
    class Config:
        env_prefix = "DAGSTER_"


class DbtSettings(BaseSettings):
    """dbt-specific settings."""
    
    # Default to local paths if not in Docker/Production
    _is_local = not Path("/opt/dagster").exists()
    _default_root = Path(__file__).parent.parent if _is_local else Path("/opt/dagster")
    
    profiles_dir: str = Field(str(_default_root / "profiles"), env="DBT_PROFILES_DIR")
    project_dir: str = Field(str(_default_root / "dbt_projects"), env="DBT_PROJECT_DIR")
    
    class Config:
        env_prefix = "DBT_"


class StorageSettings(BaseSettings):
    """Storage backend settings."""
    
    backend: str = Field("postgres", env="STORAGE_BACKEND")
    postgres_host: str = Field("postgres", env="POSTGRES_HOST")
    postgres_port: int = Field(5432, env="POSTGRES_PORT")
    postgres_db: str = Field("dagster", env="POSTGRES_DB")
    postgres_user: str = Field("dagster", env="POSTGRES_USER")
    postgres_password: str = Field("dagster_password", env="POSTGRES_PASSWORD")


class PlatformSettings(BaseSettings):
    """Main platform settings."""
    gcp_bigquery: GCPBigQuerySettings
    # environment: str = Field("dev", env="ENVIRONMENT")
    # debug: bool = Field(True, env="DEBUG")
    # log_level: str = Field("INFO", env="LOG_LEVEL")
    
    # Data warehouse - GCP BigQuery
    data_warehouse: str = Field("bigquery", env="DATA_WAREHOUSE")
    
    # Sub-settings
    # gcp_bigquery: GCPBigQuerySettings = Field(default_factory=GCPBigQuerySettings)
    gcp_bigquery: Optional[GCPBigQuerySettings] = None 
# commented out for now to avoid errors
    # gcp_gcs: GCPGCSSettings = Field(default_factory=GCPGCSSettings)
    # vertex_ai: VertexAISettings = Field(default_factory=VertexAISettings)
    # pubsub: GCPPubSubSettings = Field(default_factory=GCPPubSubSettings)
    # gcp_security: GCPSecuritySettings = Field(default_factory=GCPSecuritySettings)
    # vector_db: VectorDBSettings = Field(default_factory=VectorDBSettings)
    # rag: RAGSettings = Field(default_factory=RAGSettings)
    
    dagster: DagsterSettings = Field(default_factory=DagsterSettings)
    dbt: DbtSettings = Field(default_factory=DbtSettings)
    storage: StorageSettings = Field(default_factory=StorageSettings)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
_settings: Optional[PlatformSettings] = None


def get_settings() -> PlatformSettings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = PlatformSettings(
            gcp_bigquery=GCPBigQuerySettings()
        )
    return _settings


def get_bigquery_connection_dict() -> dict:
    """Get BigQuery connection dictionary for dbt."""
    settings = get_settings()
    gcp = settings.gcp_bigquery
    
    connection_dict = {
        "type": "bigquery",
        "project": gcp.project_id,
        "dataset": gcp.dataset,
        "location": gcp.location,
        "priority": gcp.priority,
        "timeout_seconds": gcp.job_timeout_seconds,
    }
    
    # Add credentials if provided
    if gcp.credentials_path:
        connection_dict["method"] = "service-account"
        connection_dict["keyfile"] = gcp.credentials_path
    elif gcp.service_account_json:
        connection_dict["method"] = "service-account-json"
        connection_dict["keyfile_json"] = gcp.service_account_json
    elif gcp.use_adc:
        connection_dict["method"] = "application-default"
    
    # Add optional settings
    if gcp.maximum_bytes_billed:
        connection_dict["maximum_bytes_billed"] = gcp.maximum_bytes_billed
    
    return connection_dict
