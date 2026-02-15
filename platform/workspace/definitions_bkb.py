"""
Main workspace definitions for Dagster.
"""

from pathlib import Path
from typing import Dict, Any
from google.cloud import bigquery

# -----------------------------
# Ensure Python can find `config` and `workspace`
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # /opt/dagster


# -----------------------------
# Dagster imports
# -----------------------------
from dagster import Definitions, asset, AssetExecutionContext, MaterializeResult, MetadataValue, AssetIn
from dagster_dbt import DbtCliResource, load_assets_from_dbt_project

# -----------------------------
# Local modules
# -----------------------------
import sys
sys.path.append(str(BASE_DIR))
from config.settings import get_settings
from workspace.resources import BigQueryResource

settings = get_settings()

# -----------------------------
# Platform / Demo Assets
# -----------------------------
@asset(name="platform_health_check", group_name="platform")
def platform_health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "environment": getattr(settings, "environment", "dev"),
        "data_warehouse": settings.data_warehouse,
        "gcp_configured": bool(settings.gcp_bigquery.project_id),
        "platform": "Dagster + dbt + GCP",
        "version": "2.0.0",
    }

@asset(name="bigquery_connection_test", group_name="platform")
def bigquery_connection_test(context: AssetExecutionContext, bigquery_client: BigQueryResource) -> MaterializeResult:
    """Test BigQuery connection and return detailed results."""
    context.log.info("Testing BigQuery connection...")
    
    try:
        # Test connection using resource
        connection_status = bigquery_client.test_connection()
        
        if connection_status["status"] == "success":
            return MaterializeResult(
                metadata={
                    "status": MetadataValue.text("success"),
                    "project_id": MetadataValue.text(connection_status["project_id"]),
                    "location": MetadataValue.text(connection_status["location"]),
                }
            )
        else:
            return MaterializeResult(
                metadata={
                    "status": MetadataValue.text("error"),
                    "error_message": MetadataValue.text(connection_status.get("error_message", "Unknown error")),
                }
            )
    except Exception as e:
        return MaterializeResult(
            metadata={
                "status": MetadataValue.text("error"),
                "error_message": MetadataValue.text(str(e)),
            }
        )

@asset(name="bigquery_dataset_check", group_name="platform", deps=[bigquery_connection_test])
def bigquery_dataset_check(context: AssetExecutionContext, bigquery_client: BigQueryResource) -> MaterializeResult:
    """Check and create required BigQuery datasets."""
    context.log.info("Checking BigQuery datasets...")
    
    client = bigquery_client.get_client()
    dataset_id = settings.gcp_bigquery.dataset
    full_dataset_id = f"{client.project}.{dataset_id}"
    
    try:
        # Check if dataset exists
        try:
            dataset = client.get_dataset(full_dataset_id)
            context.log.info(f"✅ Dataset '{full_dataset_id}' already exists")
            return MaterializeResult(
                metadata={
                    "status": MetadataValue.text("exists"),
                    "dataset": MetadataValue.text(full_dataset_id),
                    "location": MetadataValue.text(dataset.location),
                }
            )
        except Exception:
            # Dataset doesn't exist, create it
            context.log.info(f"📦 Creating dataset '{full_dataset_id}'...")
            dataset = bigquery.Dataset(full_dataset_id)
            dataset.location = settings.gcp_bigquery.location
            dataset = client.create_dataset(dataset, exists_ok=True)
            
            return MaterializeResult(
                metadata={
                    "status": MetadataValue.text("created"),
                    "dataset": MetadataValue.text(full_dataset_id),
                    "location": MetadataValue.text(dataset.location),
                }
            )
    except Exception as e:
        context.log.error(f"❌ Error with dataset '{full_dataset_id}': {str(e)}")
        raise e

@asset(name="dbt_connection_test", group_name="platform", deps=[bigquery_connection_test])
def dbt_connection_test(context: AssetExecutionContext, dbt: DbtCliResource) -> MaterializeResult:
    context.log.info("Testing dbt connection to BigQuery...")
    try:
        result = dbt.cli(["debug"], context=context)
        return MaterializeResult(metadata={
            "status": MetadataValue.text("success" if result.return_code == 0 else "error"),
            "output": MetadataValue.text(result.raw_output[:500] if result.raw_output else "No output")
        })
    except Exception as e:
        return MaterializeResult(metadata={
            "status": MetadataValue.text("error"),
            "error_message": MetadataValue.text(str(e)),
        })


# -----------------------------
# Workspace Assets & Resources
# -----------------------------
all_assets = [
    platform_health_check,
    bigquery_connection_test,
    bigquery_dataset_check,
    dbt_connection_test
]

# Load assets from the 'claims' dbt project
claims_dbt_project_dir = str(BASE_DIR / "dbt_projects" / "claims")
dbt_claims_assets = load_assets_from_dbt_project(
    project_dir=claims_dbt_project_dir,
    profiles_dir=settings.dbt.profiles_dir,
    key_prefix=["claims"],  # Use "claims" as the asset group name
)
all_assets.extend(dbt_claims_assets)

all_resources = {
    # This single dbt resource will be used by all dbt assets
    "dbt": DbtCliResource(
        project_dir=claims_dbt_project_dir,
        profiles_dir=settings.dbt.profiles_dir,
    ),
    "bigquery_client": BigQueryResource(
        project_id=settings.gcp_bigquery.project_id,
        location=settings.gcp_bigquery.location,
        credentials_path=settings.gcp_bigquery.credentials_path,
        service_account_json=settings.gcp_bigquery.service_account_json,
        use_adc=settings.gcp_bigquery.use_adc,
    ),
}

workspace_defs = Definitions(assets=all_assets, resources=all_resources)
__all__ = ["workspace_defs"]
