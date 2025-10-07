"""Environment-specific settings using Pydantic for validation."""

import os
from typing import Optional
from pydantic import BaseSettings, Field


class SnowflakeSettings(BaseSettings):
    """Snowflake connection settings."""
    
    account: str = Field(..., env="SNOWFLAKE_ACCOUNT")
    user: str = Field(..., env="SNOWFLAKE_USER")
    password: str = Field(..., env="SNOWFLAKE_PASSWORD")
    warehouse: str = Field(..., env="SNOWFLAKE_WAREHOUSE")
    database: str = Field(..., env="SNOWFLAKE_DATABASE")
    schema: str = Field(..., env="SNOWFLAKE_SCHEMA")
    role: str = Field(..., env="SNOWFLAKE_ROLE")
    
    # Alternative connection string format
    connection_string: Optional[str] = Field(None, env="SNOWFLAKE_CONNECTION_STRING")
    
    class Config:
        env_prefix = "SNOWFLAKE_"


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
    
    profiles_dir: str = Field("/opt/dagster/dbt_profiles", env="DBT_PROFILES_DIR")
    project_dir: str = Field("/opt/dagster/dbt_projects", env="DBT_PROJECT_DIR")
    
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
    
    environment: str = Field("dev", env="ENVIRONMENT")
    debug: bool = Field(True, env="DEBUG")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    
    # Sub-settings
    snowflake: SnowflakeSettings = Field(default_factory=SnowflakeSettings)
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
        _settings = PlatformSettings()
    return _settings


def get_snowflake_connection_string() -> str:
    """Get Snowflake connection string in the format expected by dbt."""
    settings = get_settings()
    
    if settings.snowflake.connection_string:
        return settings.snowflake.connection_string
    
    # Build connection string from individual components
    return (
        f"snowflake://{settings.snowflake.user}:{settings.snowflake.password}"
        f"@{settings.snowflake.account}/{settings.snowflake.database}/{settings.snowflake.schema}"
        f"?warehouse={settings.snowflake.warehouse}&role={settings.snowflake.role}"
    )
