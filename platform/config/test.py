
from config.settings import get_settings
s = get_settings()
print("PROJECT:", s.gcp_bigquery.project_id)

