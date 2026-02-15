#!/usr/bin/env python3
"""
Test dbt connection to BigQuery.
This script tests if dbt can connect to BigQuery using the profiles.yml configuration.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_dbt_connection():
    """Test dbt connection to BigQuery."""
    
    print("🧪 Testing dbt Connection to BigQuery")
    print("=" * 60)
    
    # Check if dbt is installed
    try:
        import subprocess
        result = subprocess.run(
            ["dbt", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            print("❌ dbt is not installed or not in PATH")
            return False
        print(f"✅ dbt version: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Error checking dbt installation: {e}")
        return False
    
    # Check profiles directory
    profiles_dir = os.getenv("DBT_PROFILES_DIR", str(project_root / "profiles"))
    print(f"\n📁 Profiles directory: {profiles_dir}")
    
    if not os.path.exists(profiles_dir):
        print(f"❌ Profiles directory does not exist: {profiles_dir}")
        return False
    
    profiles_file = Path(profiles_dir) / "profiles.yml"
    if not profiles_file.exists():
        print(f"❌ profiles.yml not found: {profiles_file}")
        return False
    
    print(f"✅ Found profiles.yml: {profiles_file}")
    
    # Check environment variables
    required_vars = [
        "GCP_PROJECT_ID",
        "GCP_BIGQUERY_DATASET",
    ]
    
    print("\n🔍 Checking environment variables...")
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
            print(f"   ❌ {var}: Not set")
        else:
            # Mask sensitive values
            if "PASSWORD" in var or "KEY" in var or "JSON" in var:
                print(f"   ✅ {var}: {'*' * 20}")
            else:
                print(f"   ✅ {var}: {value}")
    
    if missing_vars:
        print(f"\n❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    # Run dbt debug
    print("\n🔄 Running dbt debug...")
    try:
        result = subprocess.run(
            ["dbt", "debug", "--profiles-dir", profiles_dir],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=project_root
        )
        
        print("\n" + "=" * 60)
        print("dbt debug output:")
        print("=" * 60)
        print(result.stdout)
        
        if result.stderr:
            print("\n" + "=" * 60)
            print("dbt debug errors:")
            print("=" * 60)
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n" + "=" * 60)
            print("✅ dbt connection test PASSED!")
            print("=" * 60)
            return True
        else:
            print("\n" + "=" * 60)
            print("❌ dbt connection test FAILED!")
            print("=" * 60)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ dbt debug timed out")
        return False
    except Exception as e:
        print(f"❌ Error running dbt debug: {e}")
        return False


if __name__ == "__main__":
    success = test_dbt_connection()
    sys.exit(0 if success else 1)


