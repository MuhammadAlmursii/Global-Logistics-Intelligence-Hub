# Global Logistics Intelligence Hub

**Objective:** Build a scalable data engineering platform for supply chain intelligence.

**Current Focus:** Data Engineering (Dagster, dbt, GCP, MinIO, Nessie)

**Use Case:** Ingest, clean, and serve shipment logs, vendor contracts, and IoT sensor data for downstream AI/ML applications.

---

## Core Components

- **Dagster**: Orchestration of pipelines
- **dbt**: Data transformations and modeling
- **GCP**: Storage (BigQuery), compute, and orchestration support
- **MinIO**: Object storage for raw and processed files
- **Nessie**: Versioned data & lineage tracking

---

## Directory Structure

Global-Logistics-Intelligence-Hub/
│
├── platform/ # Dagster pipelines & Python scripts
├── dbt/ # dbt models, seeds, snapshots
├── docker/ # Dockerfiles & Docker Compose
├── configs/ # Configuration files (YAML, JSON)
├── docs/ # Documentation files
├── tests/ # Unit and integration tests
├── README.md # Project overview
└── airbyte-config.json # Airbyte integration config


---

## Getting Started

1. Clone the repo:

```bash
git clone https://github.com/MuhammadAlmursii/Global-Logistics-Intelligence-Hub.git
cd Global-Logistics-Intelligence-Hub

2. Set up environment variables (GCP, MinIO, Nessie)

3. Start Docker Compose:
- docker-compose up -d

4. Run Dagster pipelines:

- dagster dev


5. Apply dbt transformations:

- dbt run --profiles-dir dbt/profiles

