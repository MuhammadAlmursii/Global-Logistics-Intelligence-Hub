# Phase 1: Data Engineering Architecture
## Global Logistics Intelligence Hub - Data Foundation

---

## Overview

Phase 1 focuses on building a robust data engineering foundation:
1. **Raw Data Ingestion** - APIs and OLTP databases
2. **Raw Data Storage** - BigQuery raw area
3. **Data Transformation** - dbt for structured data
4. **Incremental Loading** - Efficient data updates
5. **Data Lineage** - Full visibility in Dagster
6. **Unstructured Data Organization** - GCS structure

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DATA SOURCES                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐          ┌──────────────┐                       │
│  │   APIs       │          │   OLTP DBs    │                       │
│  │              │          │               │                       │
│  │ • Port Data  │          │ • SAP         │                       │
│  │ • Weather    │          │ • Oracle      │                       │
│  │ • Shipping   │          │ • SQL Server  │                       │
│  └──────┬───────┘          └──────┬───────┘                       │
│         │                         │                                │
└─────────┼─────────────────────────┼────────────────────────────────┘
          │                         │
          ▼                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│              DAGSTER INGESTION LAYER                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────┐  ┌──────────────────────┐               │
│  │  API Ingestion       │  │  DB Batch Ingestion  │               │
│  │  Assets              │  │  Assets              │               │
│  │                      │  │                      │               │
│  │ • Port API           │  │ • SAP Connector      │               │
│  │ • Weather API        │  │ • Oracle Connector   │               │
│  │ • Shipping API       │  │ • Incremental Logic  │               │
│  │ • Rate Limiting      │  │ • Change Detection   │               │
│  │ • Error Handling     │  │ • Schema Mapping     │               │
│  └──────────┬───────────┘  └──────────┬─────────┘               │
│             │                           │                           │
└─────────────┼───────────────────────────┼───────────────────────────┘
              │                           │
              └───────────┬───────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│              RAW DATA STORAGE (BigQuery)                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Project: {GCP_PROJECT_ID}                                         │
│  Dataset: raw                                                       │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Schema: raw_api                                             │  │
│  │  ├── port_congestion_raw                                    │  │
│  │  ├── weather_forecast_raw                                   │  │
│  │  ├── shipping_rates_raw                                     │  │
│  │  └── api_metadata (logs, errors, timestamps)                 │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Schema: raw_db                                               │  │
│  │  ├── sap_shipments_raw                                      │  │
│  │  ├── sap_vendors_raw                                        │  │
│  │  ├── oracle_contracts_raw                                   │  │
│  │  ├── oracle_transactions_raw                                │  │
│  │  └── db_metadata (load_timestamp, source_system, etc)      │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Schema: raw_unstructured                                    │  │
│  │  ├── document_metadata                                      │  │
│  │  │   ├── file_path (GCS path)                               │  │
│  │  │   ├── file_type                                          │  │
│  │  │   ├── ingestion_timestamp                                │  │
│  │  │   ├── file_size                                          │  │
│  │  │   └── source_system                                     │  │
│  │  └── document_lineage                                        │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│              DBT TRANSFORMATION LAYER                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Project: logistics_intelligence                                    │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Schema: staging                                             │  │
│  │  ├── stg_port_congestion (from raw_api.port_congestion_raw)  │  │
│  │  ├── stg_weather_forecast (from raw_api.weather_forecast_raw)│  │
│  │  ├── stg_shipments (from raw_db.sap_shipments_raw)          │  │
│  │  ├── stg_vendors (from raw_db.sap_vendors_raw)              │  │
│  │  └── stg_contracts (from raw_db.oracle_contracts_raw)       │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Schema: marts                                               │  │
│  │  ├── mart_shipments (unified shipment view)                 │  │
│  │  ├── mart_vendors (unified vendor view)                     │  │
│  │  ├── mart_logistics_intelligence (combined insights)        │  │
│  │  └── mart_delays (delay analysis)                           │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│              DAGSTER LINEAGE & MONITORING                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  • Full asset lineage visualization                                 │
│  • Incremental load tracking                                        │
│  • Data quality metrics                                             │
│  • Error monitoring                                                 │
│  • Run history                                                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## LAYER 1: RAW DATA STORAGE STRUCTURE

### 1.1 BigQuery Dataset Structure

```
Project: {GCP_PROJECT_ID}
│
├── Dataset: raw
│   ├── Schema: raw_api
│   │   ├── port_congestion_raw
│   │   ├── weather_forecast_raw
│   │   ├── shipping_rates_raw
│   │   └── api_metadata
│   │
│   ├── Schema: raw_db
│   │   ├── sap_shipments_raw
│   │   ├── sap_vendors_raw
│   │   ├── oracle_contracts_raw
│   │   ├── oracle_transactions_raw
│   │   └── db_metadata
│   │
│   └── Schema: raw_unstructured
│       ├── document_metadata
│       └── document_lineage
│
└── Dataset: staging (dbt managed)
    └── Schema: staging
        └── (dbt models)
```

### 1.2 Raw Table Schema Standards

**Standard columns for ALL raw tables:**
- `_dagster_ingestion_timestamp` (TIMESTAMP) - When Dagster ingested
- `_dagster_run_id` (STRING) - Dagster run identifier
- `_dagster_asset_key` (STRING) - Asset that created this record
- `_source_system` (STRING) - Source system name
- `_raw_data` (JSON) - Original raw payload (for API data)
- `_is_deleted` (BOOLEAN) - Soft delete flag
- `_row_hash` (STRING) - Hash of row for change detection

**Example: `raw_api.port_congestion_raw`**
```sql
CREATE TABLE `raw.raw_api.port_congestion_raw` (
  -- Standard columns
  _dagster_ingestion_timestamp TIMESTAMP NOT NULL,
  _dagster_run_id STRING NOT NULL,
  _dagster_asset_key STRING NOT NULL,
  _source_system STRING NOT NULL,
  _raw_data JSON,
  _is_deleted BOOLEAN DEFAULT FALSE,
  _row_hash STRING NOT NULL,
  
  -- API-specific columns
  port_code STRING,
  port_name STRING,
  congestion_level STRING,
  vessel_count INTEGER,
  wait_time_hours FLOAT64,
  last_updated TIMESTAMP,
  api_response_timestamp TIMESTAMP
)
PARTITION BY DATE(_dagster_ingestion_timestamp)
CLUSTER BY port_code;
```

---

## LAYER 2: API INGESTION LAYER

### 2.1 API Ingestion Architecture

**Components:**
1. **API Client Assets** - Handle API calls
2. **Rate Limiting** - Prevent API throttling
3. **Error Handling** - Retry logic, circuit breakers
4. **Data Validation** - Schema validation
5. **Incremental Logic** - Only fetch new/changed data

### 2.2 API Asset Structure

**Example: Port Congestion API**

```python
@asset(
    name="port_congestion_api_raw",
    description="Ingest port congestion data from API",
    group_name="api_ingestion",
    metadata={
        "source": "port_congestion_api",
        "refresh_frequency": "hourly",
        "api_endpoint": "https://api.ports.com/congestion"
    },
    partitions_def=DailyPartitionsDefinition(start_date="2024-01-01"),
)
def ingest_port_congestion_api(context: AssetExecutionContext) -> pd.DataFrame:
    """
    Steps:
    1. Get API credentials from Secret Manager
    2. Check last successful ingestion timestamp
    3. Make API call with rate limiting
    4. Validate response schema
    5. Transform to standard format
    6. Load to BigQuery raw table
    7. Log metadata
    """
    pass
```

### 2.3 API Ingestion Steps (Detailed)

#### Step 2.3.1: Authentication
- **Tool:** GCP Secret Manager
- **Store:** API keys, tokens, credentials
- **Retrieval:** At runtime via Dagster resources

#### Step 2.3.2: Incremental Logic
- **Checkpoint:** Last successful ingestion timestamp in BigQuery
- **Query:** Only fetch data since last checkpoint
- **Update:** Update checkpoint after successful load

#### Step 2.3.3: Rate Limiting
- **Strategy:** Token bucket algorithm
- **Implementation:** Dagster resource with rate limiter
- **Config:** Per-API rate limits

#### Step 2.3.4: Error Handling
- **Retries:** Exponential backoff (3 retries)
- **Circuit Breaker:** Stop calling if API fails repeatedly
- **Logging:** All errors to `raw_api.api_metadata`

#### Step 2.3.5: Data Validation
- **Schema Validation:** Pydantic models
- **Data Quality:** Null checks, type validation
- **Rejection:** Invalid records to error table

#### Step 2.3.6: Load to BigQuery
- **Method:** BigQuery Load Job API
- **Format:** JSON or Parquet
- **Append:** Always append (never overwrite raw)
- **Partitioning:** By ingestion date

### 2.4 API Metadata Tracking

**Table: `raw_api.api_metadata`**
```sql
CREATE TABLE `raw.raw_api.api_metadata` (
  run_id STRING NOT NULL,
  asset_key STRING NOT NULL,
  api_name STRING NOT NULL,
  api_endpoint STRING,
  request_timestamp TIMESTAMP,
  response_timestamp TIMESTAMP,
  status_code INTEGER,
  records_fetched INTEGER,
  records_loaded INTEGER,
  records_failed INTEGER,
  error_message STRING,
  execution_time_seconds FLOAT64,
  api_rate_limit_remaining INTEGER
)
PARTITION BY DATE(request_timestamp)
CLUSTER BY api_name, run_id;
```

---

## LAYER 3: DATABASE BATCH INGESTION LAYER

### 3.1 Database Connection Strategy

**Approach: Export → GCS → BigQuery Load**

**Why this approach?**
- Better performance than federated queries
- Can handle large volumes
- Allows transformation during load
- More reliable for batch processing

### 3.2 Database Ingestion Architecture

**Components:**
1. **Database Connector Assets** - Connect to SAP/Oracle
2. **Query Builder** - Build incremental queries
3. **Export to GCS** - Temporary staging
4. **BigQuery Load** - Load from GCS
5. **Schema Mapping** - Map source to target

### 3.3 Database Asset Structure

**Example: SAP Shipments**

```python
@asset(
    name="sap_shipments_raw",
    description="Ingest shipments from SAP",
    group_name="db_ingestion",
    partitions_def=DailyPartitionsDefinition(start_date="2024-01-01"),
)
def ingest_sap_shipments(context: AssetExecutionContext) -> pd.DataFrame:
    """
    Steps:
    1. Connect to SAP (via JDBC/ODBC or export file)
    2. Query incremental data (since last load)
    3. Export to GCS (temporary)
    4. Load from GCS to BigQuery
    5. Validate row counts
    6. Update checkpoint
    7. Clean up GCS temp files
    """
    pass
```

### 3.4 Database Ingestion Steps (Detailed)

#### Step 3.4.1: Connection Setup
- **SAP:** JDBC connection or export file
- **Oracle:** JDBC connection
- **Credentials:** Secret Manager
- **Connection Pooling:** For multiple tables

#### Step 3.4.2: Incremental Query Logic
- **Checkpoint Table:** `raw_db.db_metadata.checkpoints`
- **Query Pattern:**
  ```sql
  SELECT * 
  FROM source_table
  WHERE last_modified_date > :last_checkpoint
     OR created_date > :last_checkpoint
  ```

#### Step 3.4.3: Schema Discovery
- **Auto-detect:** Column names, types
- **Mapping:** Source → Target schema
- **Validation:** Schema changes detection

#### Step 3.4.4: Export to GCS
- **Format:** Parquet (recommended) or CSV
- **Location:** `gs://{bucket}/temp/{table_name}/{date}/`
- **Partitioning:** By date for large tables

#### Step 3.4.5: BigQuery Load
- **Method:** BigQuery Load Job from GCS
- **Write Disposition:** WRITE_APPEND
- **Schema:** Auto-detect or explicit
- **Error Handling:** Bad records to error table

#### Step 3.4.6: Change Detection
- **Method:** Hash-based (MD5/SHA256 of key columns)
- **Tracking:** Store hash in `_row_hash` column
- **Deduplication:** Remove duplicates if re-run

#### Step 3.4.7: Checkpoint Update
- **Table:** `raw_db.db_metadata.checkpoints`
- **Update:** After successful load
- **Fields:** table_name, last_load_timestamp, last_load_row_count

### 3.5 Database Metadata Tracking

**Table: `raw_db.db_metadata.checkpoints`**
```sql
CREATE TABLE `raw.raw_db.db_metadata.checkpoints` (
  table_name STRING NOT NULL,
  source_system STRING NOT NULL,
  last_load_timestamp TIMESTAMP,
  last_load_row_count INTEGER,
  last_successful_run_id STRING,
  schema_version STRING,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
CLUSTER BY table_name, source_system;
```

**Table: `raw_db.db_metadata.load_history`**
```sql
CREATE TABLE `raw.raw_db.db_metadata.load_history` (
  run_id STRING NOT NULL,
  table_name STRING NOT NULL,
  source_system STRING NOT NULL,
  load_timestamp TIMESTAMP,
  rows_loaded INTEGER,
  rows_failed INTEGER,
  execution_time_seconds FLOAT64,
  status STRING, -- SUCCESS, FAILED, PARTIAL
  error_message STRING
)
PARTITION BY DATE(load_timestamp)
CLUSTER BY table_name, source_system;
```

---

## LAYER 4: DBT TRANSFORMATION LAYER

### 4.1 dbt Project Structure

```
dbt_projects/
└── logistics_intelligence/
    ├── dbt_project.yml
    ├── models/
    │   ├── staging/
    │   │   ├── stg_port_congestion.sql
    │   │   ├── stg_weather_forecast.sql
    │   │   ├── stg_shipments.sql
    │   │   ├── stg_vendors.sql
    │   │   └── stg_contracts.sql
    │   │
    │   ├── marts/
    │   │   ├── mart_shipments.sql
    │   │   ├── mart_vendors.sql
    │   │   ├── mart_logistics_intelligence.sql
    │   │   └── mart_delays.sql
    │   │
    │   └── sources.yml
    │
    ├── macros/
    │   ├── incremental_strategy.sql
    │   └── schema_normalization.sql
    │
    └── tests/
        └── data_quality_tests.sql
```

### 4.2 Staging Models

**Purpose:** Clean, standardize, and validate raw data

**Example: `stg_port_congestion.sql`**
```sql
{{
    config(
        materialized='incremental',
        unique_key='port_congestion_id',
        incremental_strategy='merge',
        cluster_by=['port_code', 'last_updated']
    )
}}

WITH source AS (
    SELECT 
        *,
        -- Generate unique ID
        GENERATE_UUID() AS port_congestion_id,
        -- Standardize timestamps
        PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', last_updated) AS last_updated_parsed
    FROM {{ source('raw_api', 'port_congestion_raw') }}
    WHERE _is_deleted = FALSE
    {% if is_incremental() %}
        AND _dagster_ingestion_timestamp > (
            SELECT MAX(_dagster_ingestion_timestamp)
            FROM {{ this }}
        )
    {% endif %}
),

cleaned AS (
    SELECT
        port_congestion_id,
        port_code,
        port_name,
        congestion_level,
        vessel_count,
        wait_time_hours,
        last_updated_parsed AS last_updated,
        _dagster_ingestion_timestamp,
        _source_system
    FROM source
    WHERE port_code IS NOT NULL
      AND last_updated_parsed IS NOT NULL
)

SELECT * FROM cleaned
```

### 4.3 Mart Models

**Purpose:** Business logic and unified views

**Example: `mart_shipments.sql`**
```sql
{{
    config(
        materialized='table',
        cluster_by=['shipment_date', 'vendor_id']
    )
}}

WITH shipments AS (
    SELECT * FROM {{ ref('stg_shipments') }}
),

port_congestion AS (
    SELECT * FROM {{ ref('stg_port_congestion') }}
),

enriched AS (
    SELECT
        s.shipment_id,
        s.vendor_id,
        s.origin_port,
        s.destination_port,
        s.shipment_date,
        s.estimated_delivery_date,
        s.actual_delivery_date,
        s.status,
        -- Calculate delay
        DATE_DIFF(
            s.actual_delivery_date,
            s.estimated_delivery_date,
            DAY
        ) AS delay_days,
        -- Join port congestion
        pc.congestion_level AS origin_congestion,
        pc.wait_time_hours AS origin_wait_time
    FROM shipments s
    LEFT JOIN port_congestion pc
        ON s.origin_port = pc.port_code
        AND DATE(s.shipment_date) = DATE(pc.last_updated)
)

SELECT * FROM enriched
```

### 4.4 Incremental Strategy in dbt

**Configuration:**
- **Strategy:** `merge` (recommended for BigQuery)
- **Unique Key:** Primary key or composite key
- **Checkpoint:** Based on timestamp column

**Benefits:**
- Only process new/changed records
- Faster execution
- Lower costs

---

## LAYER 5: GCS STRUCTURE FOR UNSTRUCTURED DATA

### 5.1 GCS Bucket Structure

```
gs://{project-id}-raw-documents/
│
├── raw/
│   ├── contracts/
│   │   ├── vendor_contracts/
│   │   │   ├── 2024/
│   │   │   │   ├── 01/
│   │   │   │   │   ├── vendor_abc_contract_20240115.pdf
│   │   │   │   │   └── vendor_xyz_contract_20240120.pdf
│   │   │   │   └── ...
│   │   │   └── ...
│   │   │
│   │   └── service_contracts/
│   │       └── (similar structure)
│   │
│   ├── bills_of_lading/
│   │   ├── 2024/
│   │   │   ├── 01/
│   │   │   │   ├── bol_12345_20240115.pdf
│   │   │   │   └── bol_12346_20240116.pdf
│   │   │   └── ...
│   │   └── ...
│   │
│   ├── reports/
│   │   ├── monthly_reports/
│   │   ├── quarterly_reports/
│   │   └── annual_reports/
│   │
│   └── images/
│       ├── warehouse_photos/
│       ├── damaged_cargo/
│       └── iot_sensor_images/
│
├── processed/
│   ├── extracted_text/
│   │   └── (same folder structure as raw)
│   │
│   ├── chunks/
│   │   └── (chunked documents)
│   │
│   └── metadata/
│       └── (JSON metadata files)
│
└── archive/
    └── (moved after processing)
```

### 5.2 GCS Folder Naming Convention

**Pattern:** `{document_type}/{sub_type}/{year}/{month}/{filename}`

**Examples:**
- `contracts/vendor_contracts/2024/01/vendor_abc_contract_20240115.pdf`
- `bills_of_lading/2024/01/bol_12345_20240115.pdf`
- `reports/monthly_reports/2024/01/monthly_report_jan_2024.pdf`

### 5.3 Document Metadata Structure

**File: `metadata/{document_id}.json`**
```json
{
  "document_id": "doc_12345",
  "file_path": "gs://bucket/raw/contracts/vendor_contracts/2024/01/file.pdf",
  "file_name": "vendor_abc_contract_20240115.pdf",
  "file_type": "pdf",
  "file_size_bytes": 1024000,
  "document_type": "vendor_contract",
  "source_system": "sharepoint",
  "ingestion_timestamp": "2024-01-15T10:30:00Z",
  "vendor_id": "V001",
  "contract_date": "2024-01-15",
  "extracted_metadata": {
    "title": "Vendor Agreement - ABC Corp",
    "author": "Legal Team",
    "page_count": 25
  },
  "processing_status": "pending",
  "dagster_run_id": "run_12345"
}
```

### 5.4 GCS Lifecycle Management

**Rules:**
1. **Raw documents:** Keep for 7 years (compliance)
2. **Processed documents:** Keep for 2 years
3. **Temp files:** Delete after 7 days
4. **Archive:** Move to cold storage after 1 year

---

## LAYER 6: DAGSTER LINEAGE & MONITORING

### 6.1 Asset Lineage Structure

**Lineage Flow:**
```
API Source → api_ingestion_asset → raw_api.port_congestion_raw
                                    ↓
                            stg_port_congestion (dbt)
                                    ↓
                            mart_logistics_intelligence (dbt)
```

### 6.2 Lineage Tracking Implementation

**In Dagster Assets:**
```python
@asset(
    name="port_congestion_api_raw",
    description="Ingest port congestion data",
    metadata={
        "source": "port_congestion_api",
        "destination": "raw.raw_api.port_congestion_raw",
        "lineage": {
            "upstream": ["port_congestion_api"],
            "downstream": ["stg_port_congestion"]
        }
    }
)
```

**In dbt Models:**
```sql
-- dbt automatically tracks lineage via ref() and source()
-- Dagster will visualize this in the UI
```

### 6.3 Monitoring & Observability

**Metrics to Track:**
1. **Ingestion Metrics:**
   - Records ingested per run
   - Execution time
   - Success/failure rate
   - API call counts

2. **Data Quality Metrics:**
   - Null percentages
   - Duplicate counts
   - Schema validation failures

3. **Lineage Metrics:**
   - Asset dependencies
   - Run dependencies
   - Data freshness

**Implementation:**
- Dagster Asset Materializations
- Dagster Observations
- Custom metrics via metadata

---

## IMPLEMENTATION PLAN - PHASE 1

### Step 1: Setup Raw Area in BigQuery
1. Create `raw` dataset
2. Create schemas: `raw_api`, `raw_db`, `raw_unstructured`
3. Create standard raw tables with standard columns
4. Create metadata tables

### Step 2: API Ingestion - Port Congestion
1. Create API client resource
2. Create port congestion ingestion asset
3. Implement rate limiting
4. Implement incremental logic
5. Load to BigQuery
6. Test and validate

### Step 3: API Ingestion - Weather Forecast
1. Similar to Step 2
2. Reuse patterns from Step 2

### Step 4: Database Ingestion - SAP Shipments
1. Setup database connection
2. Create SAP shipments ingestion asset
3. Implement incremental query logic
4. Export to GCS → Load to BigQuery
5. Test and validate

### Step 5: Database Ingestion - Oracle Contracts
1. Similar to Step 4
2. Reuse patterns

### Step 6: dbt Staging Models
1. Create staging models for all raw tables
2. Implement incremental strategy
3. Add data quality tests
4. Test transformations

### Step 7: dbt Mart Models
1. Create unified marts
2. Implement business logic
3. Test joins and aggregations

### Step 8: GCS Structure Setup
1. Create bucket structure
2. Setup lifecycle policies
3. Create document metadata schema
4. Test file organization

### Step 9: Lineage & Monitoring
1. Verify lineage in Dagster UI
2. Setup monitoring dashboards
3. Configure alerts

### Step 10: Testing & Validation
1. End-to-end testing
2. Data quality validation
3. Performance testing
4. Documentation

---

## DECISIONS NEEDED

1. **API Refresh Frequency:** Hourly? Every 6 hours? Daily?
2. **Database Batch Schedule:** Daily? Twice daily?
3. **Incremental Strategy:** Timestamp-based? Hash-based? Both?
4. **Data Retention:** How long to keep raw data?
5. **Error Handling:** Fail fast? Continue with errors?
6. **GCS Bucket Naming:** What's your preferred bucket name pattern?

---

## NEXT STEPS

1. Review this architecture
2. Make decisions on questions above
3. Start with Step 1 (Raw Area Setup)
4. Implement step by step
5. Test each step before moving to next

Let's start with Step 1!


