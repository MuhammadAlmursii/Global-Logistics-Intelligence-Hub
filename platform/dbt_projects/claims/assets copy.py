"""
Dagster assets for the claims dbt project.
"""

import os
from pathlib import Path
from typing import Dict, Any

from dagster import (
    Definitions,
    load_assets_from_dbt_project,
    AssetExecutionContext,
    get_dagster_logger,
)
from dagster_dbt import DbtCliResource

# Import configuration
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.settings import get_settings

logger = get_dagster_logger()


class DbtProjectConfig:
    """Configuration for dbt project integration."""
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.settings = get_settings()
        # Use path relative to this file to ensure it works locally and in Docker
        self.project_dir = Path(__file__).parent
        self.profiles_dir = self.settings.dbt.profiles_dir
        
    def get_dbt_cli_resource(self) -> DbtCliResource:
        """Get configured DbtCliResource."""
        return DbtCliResource(
            project_dir=str(self.project_dir),
            profiles_dir=self.profiles_dir,
        )


# =============================================================================
# CUSTOMIZE THIS SECTION FOR YOUR PROJECT
# =============================================================================

# Project configuration
PROJECT_NAME = "claims"
PROJECT_DESCRIPTION = "Claims processing dbt project"

# dbt project configuration
dbt_config = DbtProjectConfig(PROJECT_NAME)
dbt_resource = dbt_config.get_dbt_cli_resource()

# =============================================================================
# ASSET DEFINITIONS
# =============================================================================

# Load all dbt assets from the project
dbt_assets_from_project = load_assets_from_dbt_project(
    project_dir=str(dbt_config.project_dir),
    profiles_dir=dbt_config.profiles_dir,
    select="*",
    # BEST PRACTICE: Do not exclude tests if you want Data Quality visibility
    # exclude="*test*", 
    key_prefix=[PROJECT_NAME],
)


# =============================================================================
# CUSTOM ASSETS
# =============================================================================

from dagster import asset

@asset(
    name=f"{PROJECT_NAME}_project_health_check",
    description="Health check for dbt project",
    group_name=PROJECT_NAME,
)
def project_health_check(context: AssetExecutionContext) -> Dict[str, Any]:
    """Check the health of the dbt project."""
    logger.info(f"Running health check for {PROJECT_NAME}")
    
    health_status = {
        "project_name": PROJECT_NAME,
        "environment": context.instance.name,
        "status": "healthy",
        "checks": {
            "dbt_project_exists": dbt_config.project_dir.exists(),
            "profiles_exist": Path(dbt_config.profiles_dir).exists(),
        }
    }
    
    context.log.info(f"Health check results: {health_status}")
    return health_status


# =============================================================================
# ASSET DEFINITIONS EXPORT
# =============================================================================

# Combine all assets
all_assets = [
    *dbt_assets_from_project,
    project_health_check,
]

# Create the definitions
defs = Definitions(
    assets=all_assets,
    resources={
        "dbt": dbt_resource,
    },
)

# Export for Dagster
__all__ = ["defs"]