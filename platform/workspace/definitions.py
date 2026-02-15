from pathlib import Path
from dagster import Definitions
from dagster_dbt import DbtCliResource, load_assets_from_dbt_project

# Directory containing all dbt projects
DBT_PROJECTS_DIR = Path("/opt/dagster/dbt_projects")

all_assets = []
all_resources = {}

for project_folder in DBT_PROJECTS_DIR.iterdir():
    # Only include folders containing dbt_project.yml
    if (project_folder / "dbt_project.yml").exists():
        project_name = project_folder.name

        # Create a dbt CLI resource for this project
        resource = DbtCliResource(
            project_dir=str(project_folder),
            profiles_dir="/opt/dagster/dbt_profiles",
        )

        # Load all dbt assets from this project
        assets = load_assets_from_dbt_project(
            project_dir=str(project_folder),
            profiles_dir="/opt/dagster/dbt_profiles",
            key_prefix=[project_name],  # prefix asset keys with project name
        )

        # Add to lists for Definitions
        all_assets.extend(assets)
        all_resources[f"{project_name}_dbt"] = resource

# Combine all assets and resources into a single Definitions object
defs = Definitions(
    assets=all_assets,
    resources=all_resources,
)

# Export for Dagster
__all__ = ["defs"]
