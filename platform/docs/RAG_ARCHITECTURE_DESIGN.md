# RAG Architecture Design - Global Logistics Intelligence Hub

## Overview

This document outlines the detailed architecture for building a RAG-based AI assistant for supply chain managers. We'll discuss each component step-by-step before implementation.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DATA INGESTION LAYER                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │ Unstructured │  │ Batch DB     │  │ API Sources  │            │
│  │ Data         │  │ Sources      │  │              │            │
│  │ (PDFs, Docs) │  │ (SAP/Oracle) │  │ (Port/Weather)│            │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘            │
│         │                  │                  │                    │
│         └──────────────────┼──────────────────┘                    │
│                            │                                        │
└────────────────────────────┼────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    PROCESSING & CLEANUP LAYER                        │
├─────────────────────────────────────────────────────────────────────┤
│  • Parsing & Chunking (Context-aware)                                │
│  • Schema Normalization                                              │
│  • PII/PHI Masking (Cloud DLP)                                      │
│  • Metadata Enrichment                                              │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STORAGE LAYER                                      │
├─────────────────────────────────────────────────────────────────────┤
│  • BigQuery (Structured Data)                                        │
│  • GCS (Raw Documents)                                               │
│  • Vertex AI Vector Search (Embeddings)                             │
│  • Data Catalog (Lineage)                                            │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    RAG QUERY LAYER                                    │
├─────────────────────────────────────────────────────────────────────┤
│  • Hybrid Search (BM25 + Semantic)                                  │
│  • Caching Layer                                                     │
│  • RBAC Security                                                     │
│  • Response Generation                                               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## DATA SOURCE 1: UNSTRUCTURED DATA

### 1.1 Source Details

**What we're ingesting:**
- PDF contracts (vendor agreements, service contracts)
- Bill of Lading documents
- Word documents (contracts, reports)
- Excel files (vendor lists, pricing sheets)
- Images (warehouse photos, damaged cargo photos)

**Source locations:**
- GCS buckets (primary)
- SharePoint (via API or sync)
- S3 (if needed, via transfer service)

### 1.2 Ingestion Flow - STEP BY STEP

#### Step 1.1: File Discovery & Monitoring
**Decision needed:** How do we detect new files?
- **Option A:** Scheduled batch job (daily/hourly) that scans GCS bucket
- **Option B:** GCS Cloud Function trigger on file upload (event-driven)
- **Option C:** Hybrid - Cloud Function for real-time + scheduled for backlog

**Recommendation:** Option C (Hybrid)
- Cloud Function for new uploads (real-time)
- Scheduled Dagster asset for historical/backlog processing

**Implementation:**
```python
@asset(
    name="unstructured_data_discovery",
    description="Discover new unstructured documents in GCS",
    schedule=ScheduleDefinition(cron_schedule="0 */6 * * *"),  # Every 6 hours
    group_name="ingestion"
)
def discover_unstructured_documents(context):
    # Scan GCS bucket for new/modified files
    # Return list of files to process
    pass
```

#### Step 1.2: File Validation & Classification
**What we need to decide:**
- File type validation (PDF, DOCX, XLSX, images)
- File size limits (max 50MB? 100MB?)
- Virus scanning? (Cloud Security Scanner)
- Duplicate detection (hash-based)

**Decision points:**
1. **File size limit:** What's the maximum file size we'll process?
2. **Duplicate handling:** Skip duplicates or version them?
3. **File type support:** All types from day 1 or phased approach?

#### Step 1.3: Document Parsing
**Decision needed:** Parsing strategy per file type

**For PDFs:**
- **Option A:** Vertex AI Document AI (best for structured PDFs with forms/tables)
- **Option B:** PyPDF2 + pdfplumber (lightweight, good for text)
- **Option C:** Hybrid - Document AI for complex, PyPDF2 for simple

**For Word/Excel:**
- python-docx for Word
- openpyxl for Excel
- Convert tables to Markdown format

**For Images:**
- Vertex AI Vision API for description generation
- Store as multimodal embeddings

**Recommendation:** Start with Option C (Hybrid) for PDFs

#### Step 1.4: Content Extraction & Structure Preservation
**Critical decision:** How do we preserve document structure?

**For Tables:**
- Extract tables as Markdown
- Store table metadata (row count, column names)
- Use table-aware chunking (don't split rows)

**For Text:**
- Preserve paragraph boundaries
- Maintain heading hierarchy
- Extract metadata (title, author, date)

**For Images:**
- Generate descriptive text using Vision API
- Store original image in GCS
- Link image to text description

### 1.3 Processing Pipeline

#### Step 1.5: Chunking Strategy
**Decision needed:** Which chunking approach?

**Options:**
1. **Semantic Chunking** (recommended for text)
   - Break at semantic boundaries (paragraphs, sections)
   - Use embeddings to find natural breaks
   - Pros: Better context preservation
   - Cons: More complex, slower

2. **Recursive Character Chunking**
   - Break by characters, respecting paragraph/sentence boundaries
   - Pros: Simple, fast
   - Cons: May break context

3. **Fixed-size with Overlap**
   - Simple character-based chunks
   - Pros: Very simple
   - Cons: Breaks context easily

**Recommendation:** Semantic chunking for text, table-aware for tables

#### Step 1.6: Parent-Child Indexing
**Decision needed:** Do we implement parent-child indexing?

**What it means:**
- Store small chunks for retrieval (children)
- Link to larger parent chunks for full context
- Example: Child = single paragraph, Parent = entire section

**Benefits:**
- Better retrieval precision (small chunks)
- Full context during generation (parent chunks)

**Recommendation:** Yes, implement parent-child indexing

#### Step 1.7: Metadata Enrichment
**What metadata to capture:**
- `source_type`: "pdf", "excel", "image"
- `source_path`: GCS path
- `timestamp`: ingestion time
- `document_type`: "contract", "bill_of_lading", "report"
- `vendor_id`: extracted from document
- `security_clearance`: access level
- `chunk_index`: position in document
- `parent_chunk_id`: for parent-child relationships

**Decision needed:** What other metadata fields do we need?

---

## DATA SOURCE 2: BATCH DATABASE SOURCES

### 2.1 Source Details

**What we're ingesting:**
- Shipment logs from SAP
- Vendor contracts from Oracle
- Historical transaction data
- Reference data (vendor master, product catalog)

**Source locations:**
- SAP (via BigQuery Federated Query or scheduled export)
- Oracle (via BigQuery Federated Query or scheduled export)
- Direct BigQuery tables (if already migrated)

### 2.2 Ingestion Flow - STEP BY STEP

#### Step 2.1: Connection Strategy
**Decision needed:** How do we connect to SAP/Oracle?

**Options:**
1. **BigQuery Federated Query**
   - Query external databases directly from BigQuery
   - Pros: No data movement, real-time
   - Cons: Performance depends on external DB, network latency

2. **Scheduled Export to GCS → BigQuery Load**
   - Export from SAP/Oracle to GCS (CSV/Parquet)
   - Load into BigQuery
   - Pros: Better performance, can transform during load
   - Cons: Data latency, requires export setup

3. **Direct Connection (via Cloud SQL or VPN)**
   - Connect directly from Dagster
   - Pros: Full control
   - Cons: Network complexity, security considerations

**Recommendation:** Start with Option 2 (Export → GCS → BigQuery) for reliability

#### Step 2.2: Schema Discovery
**What we need:**
- Discover table structures
- Map source schemas to normalized schema
- Handle schema evolution

**Decision needed:** How do we handle schema changes?
- **Option A:** Fail on schema mismatch (strict)
- **Option B:** Auto-detect and adapt (flexible)
- **Option C:** Version schemas and maintain compatibility

**Recommendation:** Option C (version schemas)

#### Step 2.3: Schema Normalization
**Critical decision:** How do we normalize field names?

**Problem:** Different sources use different naming
- SAP: "VendorID", "Supplier_No"
- Oracle: "VENDOR_ID", "SUPPLIER_NUMBER"

**Approach:**
1. Create mapping table in BigQuery
2. Transform during ingestion
3. Store both original and normalized names

**Decision needed:** What's our standard naming convention?
- snake_case? (vendor_id, supplier_number)
- camelCase? (vendorId, supplierNumber)

**Recommendation:** snake_case (standard for BigQuery)

#### Step 2.4: Incremental Loading Strategy
**Decision needed:** Full load or incremental?

**Options:**
1. **Full Load** (daily)
   - Simple, ensures consistency
   - Cons: Slow, expensive for large tables

2. **Incremental Load** (with change detection)
   - Only load changed records
   - Pros: Fast, efficient
   - Cons: Requires change tracking

3. **CDC (Change Data Capture)**
   - Real-time change detection
   - Pros: Near real-time
   - Cons: Complex setup

**Recommendation:** Start with Option 2 (Incremental with timestamp/ID)

#### Step 2.5: Data Quality Checks
**What checks do we need?**
- Null checks on required fields
- Data type validation
- Referential integrity
- Business rule validation

**Decision needed:** Fail on quality issues or log and continue?

**Recommendation:** Log and continue (with alerts for critical issues)

#### Step 2.6: Transformation for RAG
**Decision needed:** How do we convert structured data to text for RAG?

**Approach:**
- Convert each row to natural language
- Example: "Shipment SH12345 from Vendor V001 (ABC Corp) was delayed by 2 days. 
            Original ETA: 2024-01-15, Actual delivery: 2024-01-17. 
            Reason: Port congestion at Los Angeles."

**Decision needed:** 
- Pre-generate text during ingestion? (faster queries)
- Generate on-the-fly during query? (more flexible)

**Recommendation:** Pre-generate during ingestion (better performance)

---

## DATA SOURCE 3: API SOURCES

### 3.1 Source Details

**What we're ingesting:**
- Real-time port congestion data
- Weather forecasts
- Shipping rates
- Customs clearance status

**Source types:**
- REST APIs
- GraphQL APIs
- Webhooks (if available)

### 3.2 Ingestion Flow - STEP BY STEP

#### Step 3.1: API Connection Strategy
**Decision needed:** How do we handle API connections?

**Options:**
1. **Direct API calls from Dagster assets**
   - Simple, direct
   - Cons: Rate limiting, error handling complexity

2. **Cloud Functions/Cloud Run as API proxy**
   - Handle rate limiting, retries
   - Pros: Better error handling, can cache
   - Cons: Additional service to manage

3. **API Gateway + Cloud Functions**
   - Enterprise-grade API management
   - Pros: Rate limiting, authentication, monitoring
   - Cons: More complex setup

**Recommendation:** Option 2 (Cloud Functions) for reliability

#### Step 3.2: Authentication & Security
**Decision needed:** How do we store API credentials?
- **Option A:** Secret Manager (recommended)
- **Option B:** Environment variables
- **Option C:** Encrypted in database

**Recommendation:** Secret Manager (GCP Secret Manager)

#### Step 3.3: Rate Limiting & Throttling
**Decision needed:** How do we handle API rate limits?

**Approach:**
- Implement exponential backoff
- Queue requests if rate limited
- Cache responses when possible

**Decision needed:** What's our retry strategy?
- Max retries: 3? 5?
- Backoff multiplier: 2x? Exponential?

#### Step 3.4: Data Freshness Requirements
**Decision needed:** How often do we need to refresh?

**Options:**
1. **Real-time** (every few minutes)
   - For critical data (port congestion)
   - Use sensors/triggers

2. **Near real-time** (hourly)
   - For less critical data
   - Scheduled jobs

3. **Daily** (once per day)
   - For reference data

**Decision needed:** What's the refresh frequency for each API?

#### Step 3.5: Data Storage Strategy
**Decision needed:** Where do we store API data?

**Options:**
1. **BigQuery only** (structured data)
2. **GCS + BigQuery** (raw JSON + processed)
3. **Both** (raw for audit, processed for query)

**Recommendation:** Option 3 (both raw and processed)

#### Step 3.6: Error Handling & Monitoring
**Decision needed:** How do we handle API failures?

**Approach:**
- Log all API calls
- Alert on failures
- Store failure reasons
- Implement circuit breaker pattern

---

## UNIFIED PROCESSING LAYER

### 4.1 PII/PHI Masking

#### Step 4.1: Detection Strategy
**Decision needed:** What do we mask?

**Common PII/PHI:**
- Phone numbers
- Email addresses
- Credit card numbers
- Bank account numbers
- Driver license numbers
- Social security numbers

**Decision needed:** Do we mask or redact?
- **Mask:** Replace with [REDACTED] or [PHONE_NUMBER]
- **Redact:** Remove completely
- **Hash:** Replace with hash (for joins)

**Recommendation:** Mask with type indicator ([PHONE_NUMBER])

#### Step 4.2: Implementation
**Tool:** Cloud DLP (Data Loss Prevention)

**Decision needed:** When do we mask?
- **Option A:** During ingestion (before storage)
- **Option B:** During query (on-the-fly)
- **Option C:** Both (ingestion + query-time for safety)

**Recommendation:** Option A (during ingestion) for performance

### 4.2 Data Lineage Tracking

#### Step 4.3: Lineage Implementation
**Decision needed:** How detailed should lineage be?

**What to track:**
- Source → Raw storage
- Raw → Processed
- Processed → Chunks
- Chunks → Embeddings
- Embeddings → Vector DB

**Tool:** Data Catalog (GCP) or custom metadata store

**Decision needed:** Do we use Data Catalog or build custom?

**Recommendation:** Use Data Catalog (native GCP integration)

### 4.3 Versioned Document Index

#### Step 4.4: Versioning Strategy
**Decision needed:** How do we handle document updates?

**Options:**
1. **Version by timestamp** (new version on update)
2. **Version by hash** (only new version if content changed)
3. **Soft delete + insert** (mark old as deleted)

**Recommendation:** Option 2 (version by hash) - efficient

---

## VECTOR DATABASE & EMBEDDINGS

### 5.1 Embedding Generation

#### Step 5.1: Embedding Model
**Decision needed:** Which model?

**Options:**
1. **Vertex AI textembedding-gecko@003** (recommended)
   - 768 dimensions
   - Optimized for GCP
   - Good performance

2. **OpenAI text-embedding-ada-002**
   - 1536 dimensions
   - Pros: Widely used
   - Cons: External dependency, cost

3. **Sentence Transformers (local)**
   - Pros: No API calls, free
   - Cons: Less powerful, requires compute

**Recommendation:** Vertex AI textembedding-gecko@003

#### Step 5.2: Embedding Strategy
**Decision needed:** What do we embed?

**Options:**
1. **Text chunks only** (standard)
2. **Text + metadata** (enriched)
3. **Multimodal** (text + images)

**Recommendation:** Start with Option 1, add Option 2 later

### 5.2 Vector Database Setup

#### Step 5.3: Vector DB Choice
**Decision needed:** Which vector database?

**Options:**
1. **Vertex AI Vector Search** (recommended)
   - Native GCP integration
   - Managed service
   - Hybrid search support

2. **Pinecone**
   - Pros: Easy to use, good performance
   - Cons: External service, cost

3. **ChromaDB (self-hosted)**
   - Pros: Free, open source
   - Cons: Requires management

**Recommendation:** Vertex AI Vector Search

#### Step 5.4: Hybrid Search Setup
**Decision needed:** Do we implement hybrid search?

**What it means:**
- BM25 (keyword search) + Semantic search
- Combine results for better retrieval

**Recommendation:** Yes, implement hybrid search

---

## SECURITY & ACCESS CONTROL

### 6.1 RBAC Implementation

#### Step 6.1: Role Definition
**Decision needed:** What roles do we need?

**Suggested roles:**
- `viewer`: Read-only access
- `analyst`: Can query, view documents
- `manager`: Can query, view, add documents
- `admin`: Full access

**Decision needed:** What are your actual roles?

#### Step 6.2: Implementation
**Tool:** IAM (GCP) + Custom application logic

**Decision needed:** Where do we enforce RBAC?
- **Option A:** At query time (filter results)
- **Option B:** At ingestion (tag with clearance level)
- **Option C:** Both

**Recommendation:** Option C (both for defense in depth)

---

## CACHING LAYER

### 7.1 Caching Strategy

#### Step 7.1: What to Cache
**Decision needed:** What do we cache?

**Options:**
1. **Query results** (full responses)
2. **Embeddings** (computed embeddings)
3. **Retrieved chunks** (from vector search)
4. **All of the above**

**Recommendation:** All of the above (with different TTLs)

#### Step 7.2: Cache Storage
**Decision needed:** Where to cache?

**Options:**
1. **Cloud Memorystore (Redis)** (recommended)
   - Managed, fast
   - Good for distributed systems

2. **In-memory (Dagster)**
   - Simple
   - Cons: Lost on restart, not shared

3. **BigQuery** (for long-term cache)
   - Pros: Persistent
   - Cons: Slower

**Recommendation:** Cloud Memorystore (Redis) for hot cache

---

## QUESTIONS FOR DISCUSSION

### Critical Decisions Needed:

1. **File Discovery:** Scheduled vs Event-driven vs Hybrid?
2. **PDF Parsing:** Document AI vs PyPDF2 vs Hybrid?
3. **Chunking:** Semantic vs Recursive vs Fixed-size?
4. **DB Connection:** Federated Query vs Export → Load?
5. **Schema Normalization:** Standard naming convention?
6. **API Strategy:** Direct calls vs Cloud Functions?
7. **PII Masking:** When? (Ingestion vs Query-time)
8. **Vector DB:** Vertex AI vs Pinecone vs ChromaDB?
9. **RBAC Roles:** What roles do you need?
10. **Caching:** What to cache and where?

### Next Steps:

1. Review this document
2. Answer the questions above
3. Agree on architecture decisions
4. Create implementation plan
5. Start with one data source (recommend: Unstructured data first)

---

## RECOMMENDED IMPLEMENTATION ORDER

1. **Phase 1:** Unstructured Data Ingestion (PDFs, Docs)
2. **Phase 2:** Processing Pipeline (Chunking, Embeddings)
3. **Phase 3:** Vector DB Setup & Hybrid Search
4. **Phase 4:** Batch DB Sources
5. **Phase 5:** API Sources
6. **Phase 6:** Security & RBAC
7. **Phase 7:** Caching & Optimization

---

Please review and let's discuss each section before we start implementation!


