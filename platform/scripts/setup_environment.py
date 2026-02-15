#!/usr/bin/env python3
"""
Script to set up environment-specific configurations.

Usage:
    python scripts/setup_environment.py <environment>
"""

import os
import sys
import shutil
from pathlib import Path
import argparse


def setup_environment(environment: str) -> None:
    """Set up environment-specific configuration."""
    
    valid_environments = ["dev", "staging", "prod"]
    if environment not in valid_environments:
        raise ValueError(f"Environment must be one of: {valid_environments}")
    
    # Set up paths
    config_dir = Path(__file__).parent.parent / "config"
    env_file = Path(__file__).parent.parent / f".env.{environment}"
    example_file = Path(__file__).parent.parent / "env.example"
    
    # Create environment-specific .env file
    if not env_file.exists() and example_file.exists():
        print(f"Creating {env_file} from template...")
        shutil.copy(example_file, env_file)
    
    # Load environment configuration
    config_file = config_dir / f"{environment}.yml"
    if config_file.exists():
        print(f"✅ Environment configuration found: {config_file}")
    else:
        print(f"⚠️  Warning: No environment config found at {config_file}")
    
    # Create necessary directories
    directories = [
        "profiles",
        "dbt_projects",
        "logs",
        "target"
    ]
    
    for directory in directories:
        dir_path = Path(__file__).parent.parent / directory
        dir_path.mkdir(exist_ok=True)
        print(f"📁 Created directory: {dir_path}")
    
    print(f"✅ Environment '{environment}' setup complete!")
    print(f"🔧 Next steps:")
    print(f"   1. Update {env_file} with your environment-specific values")
    print(f"   2. Review {config_file} configuration")
    print(f"   3. Test connection with: docker-compose -f docker-compose.{environment}.yml up -d")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Set up environment-specific configuration")
    parser.add_argument("environment", choices=["dev", "staging", "prod"], 
                       help="Environment to set up")
    
    args = parser.parse_args()
    
    try:
        setup_environment(args.environment)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()



