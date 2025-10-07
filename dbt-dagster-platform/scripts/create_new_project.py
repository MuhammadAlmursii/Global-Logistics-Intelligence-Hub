#!/usr/bin/env python3
"""
Script to create a new dbt project from the template.

Usage:
    python scripts/create_new_project.py <project_name> [target_directory]
"""

import os
import sys
import shutil
from pathlib import Path
import argparse


def create_new_project(project_name: str, target_dir: str = None) -> None:
    """Create a new dbt project from the template."""
    
    # Validate project name
    if not project_name.replace("_", "").replace("-", "").isalnum():
        raise ValueError("Project name must contain only letters, numbers, underscores, and hyphens")
    
    # Set up paths
    template_dir = Path(__file__).parent.parent / "templates" / "dbt-project"
    if target_dir:
        project_dir = Path(target_dir) / project_name
    else:
        project_dir = Path(__file__).parent.parent / "dbt_projects" / project_name
    
    # Check if template exists
    if not template_dir.exists():
        raise FileNotFoundError(f"Template directory not found: {template_dir}")
    
    # Check if project already exists
    if project_dir.exists():
        raise FileExistsError(f"Project already exists: {project_dir}")
    
    # Create project directory
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy template files
    print(f"Creating project '{project_name}' in {project_dir}")
    shutil.copytree(template_dir, project_dir, dirs_exist_ok=True)
    
    # Update project configuration files
    update_project_files(project_dir, project_name)
    
    # Create project assets directory
    assets_dir = project_dir / "assets"
    assets_dir.mkdir(exist_ok=True)
    
    # Copy and customize assets.py
    assets_src = template_dir / "assets.py"
    assets_dst = assets_dir / "assets.py"
    if assets_src.exists():
        with open(assets_src, "r") as f:
            content = f.read()
        
        # Replace template placeholders
        content = content.replace("your_project_name", project_name)
        content = content.replace("Your dbt project description", f"dbt project for {project_name}")
        
        with open(assets_dst, "w") as f:
            f.write(content)
    
    print(f"✅ Project '{project_name}' created successfully!")
    print(f"📁 Project directory: {project_dir}")
    print(f"🔧 Next steps:")
    print(f"   1. Update {project_dir}/dbt_project.yml with your project details")
    print(f"   2. Configure your dbt models in {project_dir}/models/")
    print(f"   3. Add the project to workspace/definitions.py")
    print(f"   4. Test your project with: cd {project_dir} && dbt deps && dbt run")


def update_project_files(project_dir: Path, project_name: str) -> None:
    """Update project-specific files with the new project name."""
    
    # Update dbt_project.yml
    dbt_project_file = project_dir / "dbt_project.yml"
    if dbt_project_file.exists():
        with open(dbt_project_file, "r") as f:
            content = f.read()
        
        content = content.replace("your_project_name", project_name)
        
        with open(dbt_project_file, "w") as f:
            f.write(content)
    
    # Update profiles.yml reference in models
    for sql_file in project_dir.rglob("*.sql"):
        with open(sql_file, "r") as f:
            content = f.read()
        
        if "your_project_name" in content:
            content = content.replace("your_project_name", project_name)
            
            with open(sql_file, "w") as f:
                f.write(content)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Create a new dbt project from template")
    parser.add_argument("project_name", help="Name of the new project")
    parser.add_argument("--target-dir", help="Target directory (default: ./dbt_projects)")
    
    args = parser.parse_args()
    
    try:
        create_new_project(args.project_name, args.target_dir)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()