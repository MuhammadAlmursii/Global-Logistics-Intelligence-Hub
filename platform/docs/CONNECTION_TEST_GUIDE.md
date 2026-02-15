# GCP BigQuery Connection Test Guide

This guide will help you test the connection to GCP BigQuery for both Dagster and dbt.

## Prerequisites

1. **GCP Project Setup:**
   - GCP Project ID
   - BigQuery API enabled
   - Service account with BigQuery permissions OR Application Default Credentials configured

2. **Environment Variables:**
   - Copy `env.example` to `.env`
   - Fill in your GCP credentials

## Step 1: Configure Environment Variables

Edit your `.env` file with the following required variables:

```bash
# Required
GCP_PROJECT_ID=your-gcp-project-id
GCP_BIGQUERY_DATASET=your_dataset_name
GCP_BIGQUERY_LOCATION=US

# Authentication (choose one method)
# Method 1: Application Default Credentials (recommended for local dev)
GCP_BIGQUERY_METHOD=application-default

# Method 2: Service Account Keyfile
# GCP_CREDENTIALS_PATH=/path/to/service-account-key.json
# GCP_BIGQUERY_METHOD=service-account

# Method 3: Service Account JSON String
# GCP_SERVICE_ACCOUNT_JSON='{"type": "service_account", ...}'
# GCP_BIGQUERY_METHOD=service-account-json
```

## Step 2: Test BigQuery Connection (Python Script)

Run the standalone connection test:

```bash
python test_bigquery_connection.py
```

**Expected Output:**
```
🔍 Testing BigQuery Connection...
==================================================
Project ID: your-project-id
Dataset: your_dataset_name
Location: US
==================================================
🔄 Initializing BigQuery client...
🔄 Testing connection...
✅ Connected to project: your-project-id
🔄 Testing query execution...
✅ Query executed successfully!
   Test value: 1
   Current time: 2024-01-15 10:30:00
🔄 Testing dataset access...
✅ Dataset 'your_dataset_name' found
   Location: US
   Created: 2024-01-01 00:00:00
🔄 Getting project information...
✅ Project name: Your Project Name
   Project number: 123456789

🎉 ALL TESTS PASSED! BigQuery connection is working correctly.
```

## Step 3: Test dbt Connection

Test dbt connection to BigQuery:

```bash
python scripts/test_dbt_connection.py
```

**Expected Output:**
```
🧪 Testing dbt Connection to BigQuery
============================================================
✅ dbt version: 1.7.13

📁 Profiles directory: /path/to/profiles
✅ Found profiles.yml: /path/to/profiles/profiles.yml

🔍 Checking environment variables...
   ✅ GCP_PROJECT_ID: your-project-id
   ✅ GCP_BIGQUERY_DATASET: your_dataset_name

🔄 Running dbt debug...
============================================================
dbt debug output:
============================================================
[Connection test output]

✅ dbt connection test PASSED!
```

## Step 4: Test in Dagster UI

1. **Start Dagster:**
   ```bash
   dagster dev
   ```

2. **Access Dagster UI:**
   - Open http://localhost:3000

3. **Run Connection Test Assets:**
   - Navigate to Assets
   - Find the `platform` group
   - Run these assets in order:
     1. `platform_health_check` - Basic platform check
     2. `bigquery_connection_test` - Tests BigQuery connection
     3. `bigquery_dataset_check` - Checks/creates required datasets
     4. `dbt_connection_test` - Tests dbt connection

4. **Check Results:**
   - Click on each asset to see detailed metadata
   - Check logs for any errors
   - Verify all assets show ✅ status

## Troubleshooting

### Authentication Errors

**Error:** `DefaultCredentialsError` or `Could not automatically determine credentials`

**Solutions:**
1. **Use Application Default Credentials:**
   ```bash
   gcloud auth application-default login
   ```

2. **Or set service account keyfile:**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
   ```

3. **Or set in .env:**
   ```bash
   GCP_CREDENTIALS_PATH=/path/to/service-account-key.json
   ```

### Permission Errors

**Error:** `Access Denied` or `Permission denied`

**Solutions:**
1. Ensure service account has these roles:
   - `BigQuery Data Editor`
   - `BigQuery Job User`
   - `BigQuery User`

2. Check IAM permissions in GCP Console

### Dataset Not Found

**Error:** `Dataset not found`

**Solutions:**
1. The `bigquery_dataset_check` asset will automatically create the `raw` dataset
2. Or create manually in BigQuery Console
3. Verify dataset name matches `GCP_BIGQUERY_DATASET` in `.env`

### dbt Connection Issues

**Error:** `dbt debug` fails

**Solutions:**
1. Verify `profiles.yml` is correctly configured
2. Check environment variables are set
3. Test BigQuery connection first (Step 2)
4. Ensure `dbt-bigquery` adapter is installed:
   ```bash
   pip install dbt-bigquery
   ```

## Next Steps

Once all connection tests pass:

1. ✅ BigQuery connection working
2. ✅ dbt connection working
3. ✅ Dagster assets can connect to BigQuery
4. ✅ Required datasets created

You're ready to proceed with:
- **Step 2:** Setup Raw Area in BigQuery
- **Step 3:** API Ingestion Layer
- **Step 4:** Database Batch Ingestion


