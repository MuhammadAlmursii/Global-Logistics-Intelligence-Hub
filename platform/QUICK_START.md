# Quick Start - Test GCP Connection

## ✅ Your Setup

- **Service Account File:** `secrets/gcp-sa.json` ✅
- **Project ID:** `scenic-style-421412` ✅
- **Service Account:** `bigquery-admin@scenic-style-421412.iam.gserviceaccount.com` ✅

## Step 1: Create .env File

```bash
cd /Users/malmursi/Downloads/DagesterDBT/dbt-dagster-platform
cp env.example .env
```

## Step 2: Edit .env File

Add these lines to your `.env` file:

```bash
# GCP BigQuery Configuration
GCP_PROJECT_ID=scenic-style-421412
GCP_BIGQUERY_DATASET=raw
GCP_BIGQUERY_LOCATION=US
GCP_BIGQUERY_METHOD=service-account
GCP_CREDENTIALS_PATH=secrets/gcp-sa.json
```

## Step 3: Test Connection

### Test 1: BigQuery Python Connection
```bash
python3 test_bigquery_connection.py
```

**Expected:** ✅ All tests passed

### Test 2: dbt Connection
```bash
python3 scripts/test_dbt_connection.py
```

**Expected:** ✅ dbt connection test PASSED

### Test 3: Dagster UI
```bash
dagster dev
```

Then:
1. Open http://localhost:3000
2. Go to Assets
3. Run these assets in order:
   - `platform_health_check`
   - `bigquery_connection_test`
   - `bigquery_dataset_check` (will create `raw` dataset if needed)
   - `dbt_connection_test`

## What Happens

1. ✅ BigQuery connection verified
2. ✅ `raw` dataset created in BigQuery (if doesn't exist)
3. ✅ dbt can connect to BigQuery
4. ✅ Ready for data ingestion!

## Troubleshooting

### "File not found" error
- Use absolute path in `.env`: 
  ```bash
  GCP_CREDENTIALS_PATH=/Users/malmursi/Downloads/DagesterDBT/dbt-dagster-platform/secrets/gcp-sa.json
  ```

### "Permission denied" error
- Check service account has BigQuery permissions in GCP Console
- Required roles: `BigQuery Data Editor`, `BigQuery Job User`

### "Dataset not found"
- The `bigquery_dataset_check` asset will create it automatically
- Or create manually in BigQuery Console

## Next Steps

Once all tests pass ✅:
- Proceed to Step 2: Setup Raw Area in BigQuery
- Start building data ingestion assets

