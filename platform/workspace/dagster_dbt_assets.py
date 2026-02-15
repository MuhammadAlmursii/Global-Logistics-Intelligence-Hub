# dagster_dbt_assets.py

import json
from pathlib import Path
from dagster import asset, AssetIn

def load_dbt_projects_as_assets(project_paths):
    all_nodes = {}

    # Load manifests
    for project_name, path in project_paths.items():
        manifest_path = Path(path) / "target" / "manifest.json"
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found for project {project_name} at {manifest_path}")
        with open(manifest_path) as f:
            manifest = json.load(f)
        for node_id, node in manifest.get("nodes", {}).items():
            node["project_name"] = project_name
            all_nodes[node_id] = node

    # Create Dagster assets
    dagster_assets = []
    for node_id, node in all_nodes.items():
        project_name = node["project_name"]
        model_name = node["name"]
        asset_name = f"{project_name}_{model_name}"

        # Wire upstream dependencies
        inputs = {}
        for upstream_id in node.get("depends_on", {}).get("nodes", []):
            if upstream_id in all_nodes:
                upstream_node = all_nodes[upstream_id]
                upstream_asset_name = f"{upstream_node['project_name']}_{upstream_node['name']}"
                inputs[upstream_asset_name] = AssetIn(upstream_asset_name)

        dagster_assets.append(
            asset(
                name=asset_name,
                ins=inputs,
                description=node.get("description", ""),
                tags={"project": project_name, "materialized": node.get("config", {}).get("materialized", "")}
            )
        )

    return dagster_assets



@dbt_assets(manifest=Path(DBT_PROJECT_DIR) / "target" / "manifest.json")
def claims_dbt_assets(context, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

defs = Definitions(
    assets=[claims_dbt_assets],
    resources={
        "dbt": DbtCliResource(
            project_dir=DBT_PROJECT_DIR,
            profiles_dir=DBT_PROFILES_DIR,
        )
    },
)