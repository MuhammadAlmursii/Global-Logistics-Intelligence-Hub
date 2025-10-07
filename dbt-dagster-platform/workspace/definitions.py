"""
Main workspace definitions for Dagster.

This file loads all dbt project assets and combines them into a single workspace.
"""

import os
from pathlib import Path
from typing import Dict, Any

from dagster import Definitions, load_assets_from_modules
from dagster_dbt import DbtCliResource

# Import configuration
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config.settings import get_settings, get_snowflake_connection_string

# Import all dbt project assets
# Add your project imports here as you create new projects
# from dbt_projects.your_project_name.assets import defs as your_project_defs

settings = get_settings()


def create_dbt_resource() -> DbtCliResource:
    """Create a shared dbt resource for all projects."""
    return DbtCliResource(
        project_dir=settings.dbt.project_dir,
        profiles_dir=settings.dbt.profiles_dir,
    )


# =============================================================================
# PROJECT REGISTRATION
# =============================================================================

# List of all dbt projects to load
# Add your projects here as you create them
DBT_PROJECTS = [
    # "your_project_name",
    # "another_project_name",
]

# Load assets from all registered projects
all_assets = []
all_resources = {"dbt": create_dbt_resource()}

# For each project, load its assets
for project_name in DBT_PROJECTS:
    try:
        # Import project assets
        project_module = __import__(f"dbt_projects.{project_name}.assets", fromlist=["defs"])
        project_defs = getattr(project_module, "defs")
        
        # Add assets to our collection
        all_assets.extend(project_defs.assets)
        
        # Merge resources (if any)
        if hasattr(project_defs, "resources"):
            all_resources.update(project_defs.resources)
            
        print(f"Successfully loaded assets from project: {project_name}")
        
    except ImportError as e:
        print(f"Warning: Could not import project {project_name}: {e}")
    except Exception as e:
        print(f"Error loading project {project_name}: {e}")


# =============================================================================
# WORKSPACE DEFINITIONS
# =============================================================================

# Create the main workspace definitions
workspace_defs = Definitions(
    assets=all_assets,
    resources=all_resources,
)

# Export for Dagster
__all__ = ["workspace_defs"]