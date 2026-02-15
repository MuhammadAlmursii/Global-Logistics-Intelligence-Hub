# Quick Setup Guide - GCP Connection

## ✅ Service Account File Detected

I can see you've already added your service account JSON file at:
```
secrets/gcp-sa.json
```

## Step 1: Create .env File

Copy the example and update with your values:

```bash
cp env.example .env
```

## Step 2: Update .env File

Edit `.env` and set these values (I've detected your project ID from the service account):

```bash
# GCP Configuration
GCP_PROJECT_ID=scenic-style-421412
GCP_BIGQUERY_DATASET=raw
GCP_BIGQUERY_LOCATION=US
GCP_BIGQUERY_METHOD=service-account
GCP_CREDENTIALS_PATH=secrets/gcp-sa.json
```

**Note:** The path `secrets/gcp-sa.json` is relative to the project root where you run dbt/Dagster commands.

## Step 3: Test Connection

### Option A: Test BigQuery Connection (Python)
```bash
python test_bigquery_connection.py
```

### Option B: Test dbt Connection
```bash
python scripts/test_dbt_connection.py
```

### Option C: Test in Dagster UI
```bash
dagster dev
```

Then open http://localhost:3000 and run:
1. `platform_health_check`
2. `bigquery_connection_test`
3. `bigquery_dataset_check`
4. `dbt_connection_test`

## Verification

✅ Service account file: `secrets/gcp-sa.json` (already added)
✅ Project ID: `scenic-style-421412` (detected from service account)
✅ Service account email: `bigquery-admin@scenic-style-421412.iam.gserviceaccount.com`

## Next Steps

Once connection tests pass:
1. The `raw` dataset will be automatically created in BigQuery
2. You can proceed with data ingestion setup

## Troubleshooting

### If path doesn't work:
- Use absolute path: `/Users/malmursi/Downloads/DagesterDBT/dbt-dagster-platform/secrets/gcp-sa.json`
- Or set `GCP_CREDENTIALS_PATH` in `.env` with absolute path

### If permissions error:
- Ensure service account has BigQuery permissions:
  - `BigQuery Data Editor`
  - `BigQuery Job User`
  - `BigQuery User`


