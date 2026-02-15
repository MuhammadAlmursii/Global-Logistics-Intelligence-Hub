"""
Dagster resources for GCP connections.
"""

from typing import Optional, Dict, Any
import json
import base64
from pathlib import Path

from google.cloud import bigquery
from google.auth.exceptions import DefaultCredentialsError
from dagster import ConfigurableResource
from pydantic import Field

class BigQueryResource(ConfigurableResource):
    """BigQuery resource using modern ConfigurableResource pattern."""
    
    project_id: str = Field(description="GCP Project ID")
    location: str = Field(default="us-central1", description="BigQuery dataset location")
    credentials_path: Optional[str] = Field(default=None, description="Path to service account key")
    service_account_json: Optional[str] = Field(default=None, description="Service account JSON string")
    use_adc: bool = Field(default=True, description="Use Application Default Credentials")

    def get_client(self) -> bigquery.Client:
        """Get BigQuery client with proper authentication."""
        
        # Handle authentication
        if self.credentials_path:
            # Resolve relative paths to absolute
            creds_path = Path(self.credentials_path)
            if not creds_path.is_absolute():
                # Resolve relative to project root (parent of workspace)
                # Assuming running from root or absolute path provided in settings
                pass
            
            # Use service account keyfile
            return bigquery.Client.from_service_account_json(
                str(creds_path),
                project=self.project_id,
                location=self.location
            )
        elif self.service_account_json:
            # Use service account JSON string
            
            # Parse JSON string
            if isinstance(self.service_account_json, str):
                try:
                    # Try to parse as JSON string
                    sa_info = json.loads(self.service_account_json)
                except json.JSONDecodeError:
                    # If not JSON, might be base64 encoded
                    sa_info = json.loads(base64.b64decode(self.service_account_json).decode())
            else:
                sa_info = self.service_account_json
            
            return bigquery.Client.from_service_account_info(
                sa_info,
                project=self.project_id,
                location=self.location
            )
        else:
            # Use Application Default Credentials
            return bigquery.Client(
                project=self.project_id,
                location=self.location
            )
    
    def test_connection(self) -> Dict[str, Any]:
        """Test BigQuery connection and return status."""
        try:
            client = self.get_client()
            
            # Test basic connection
            project = client.project
            project_info = client.get_project(project)
            
            # Test query execution
            query = "SELECT 1 as test_value, CURRENT_TIMESTAMP() as current_time"
            query_job = client.query(query)
            results = query_job.result()
            
            result_data = None
            for row in results:
                result_data = {
                    "test_value": row.test_value,
                    "current_time": str(row.current_time)
                }
            
            return {
                "status": "success",
                "project_id": project,
                "project_number": project_info.project_number,
                "project_name": project_info.friendly_name or project,
                "query_test": result_data,
                "location": self.location
            }
        except DefaultCredentialsError as e:
            return {
                "status": "error",
                "error_type": "authentication",
                "error_message": str(e),
                "suggestion": "Set GOOGLE_APPLICATION_CREDENTIALS or provide service account credentials"
            }
        except Exception as e:
            return {
                "status": "error",
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
