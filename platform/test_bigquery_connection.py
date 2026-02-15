#!/usr/bin/env python3
"""
Test BigQuery connection with the provided GCP credentials.
This script will verify if the BigQuery connection works before testing with dbt.
"""

import os
import sys
from google.cloud import bigquery
from google.cloud.exceptions import GoogleCloudError
from google.auth.exceptions import DefaultCredentialsError

def test_bigquery_connection():
    """Test BigQuery connection with the provided credentials."""
    
    # Get configuration from environment variables
    project_id = os.getenv('GCP_PROJECT_ID')
    dataset_id = os.getenv('GCP_BIGQUERY_DATASET', 'test_dataset')
    location = os.getenv('GCP_BIGQUERY_LOCATION', 'US')
    
    if not project_id:
        print("❌ Error: GCP_PROJECT_ID environment variable is not set")
        print("💡 Please set GCP_PROJECT_ID in your .env file or environment")
        return False
    
    print("🔍 Testing BigQuery Connection...")
    print("=" * 50)
    print(f"Project ID: {project_id}")
    print(f"Dataset: {dataset_id}")
    print(f"Location: {location}")
    print("=" * 50)
    
    try:
        # Initialize BigQuery client
        print("🔄 Initializing BigQuery client...")
        client = bigquery.Client(project=project_id, location=location)
        
        # Test the connection by getting project info
        print("🔄 Testing connection...")
        project = client.project
        print(f"✅ Connected to project: {project}")
        
        # Test query execution
        print("🔄 Testing query execution...")
        query = "SELECT 1 as test_value, CURRENT_TIMESTAMP() as current_time"
        query_job = client.query(query)
        results = query_job.result()
        
        for row in results:
            print(f"✅ Query executed successfully!")
            print(f"   Test value: {row.test_value}")
            print(f"   Current time: {row.current_time}")
        
        # Test dataset access (if dataset exists)
        print("🔄 Testing dataset access...")
        try:
            dataset = client.get_dataset(dataset_id)
            print(f"✅ Dataset '{dataset_id}' found")
            print(f"   Location: {dataset.location}")
            print(f"   Created: {dataset.created}")
        except Exception as e:
            print(f"⚠️  Dataset '{dataset_id}' not found (this is okay if it doesn't exist yet)")
            print(f"   Error: {str(e)}")
        
        # Get project information
        print("🔄 Getting project information...")
        project_info = client.get_project(project_id)
        print(f"✅ Project name: {project_info.friendly_name or project_id}")
        print(f"   Project number: {project_info.project_number}")
        
        print("\n🎉 ALL TESTS PASSED! BigQuery connection is working correctly.")
        return True
        
    except DefaultCredentialsError as e:
        print(f"❌ Authentication Error: {e}")
        print("\n💡 Possible solutions:")
        print("   - Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
        print("   - Run 'gcloud auth application-default login'")
        print("   - Set GCP_CREDENTIALS_PATH in .env file")
        print("   - Set GCP_SERVICE_ACCOUNT_JSON in .env file")
        return False
        
    except GoogleCloudError as e:
        print(f"❌ Google Cloud Error: {e}")
        print("\n💡 Possible solutions:")
        print("   - Check if the project ID is correct")
        print("   - Verify the service account has BigQuery permissions")
        print("   - Check if BigQuery API is enabled in the project")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        print("\n💡 Possible solutions:")
        print("   - Check network connectivity")
        print("   - Verify all credentials are correct")
        print("   - Check if BigQuery service is accessible")
        return False

if __name__ == "__main__":
    print("🧪 BigQuery Connection Test")
    print("=" * 50)
    
    # Load environment variables from .env file if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("⚠️  python-dotenv not installed, using system environment variables only")
    
    success = test_bigquery_connection()
    
    if success:
        print("\n✅ Connection test completed successfully!")
        print("You can now proceed with dbt testing.")
        sys.exit(0)
    else:
        print("\n❌ Connection test failed!")
        print("Please fix the issues before testing with dbt.")
        sys.exit(1)

