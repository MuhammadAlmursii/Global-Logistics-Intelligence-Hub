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

# Global Logistics Intelligence Hub – Directory Structure

Global-Logistics-Intelligence-Hub/
├── platform/                # Dagster pipelines & Python scripts
│   ├── pipelines/           # Dagster pipeline definitions
│   ├── assets/              # Dagster asset definitions
│   ├── jobs/                # Predefined Dagster jobs
│   └── utils/               # Utility scripts
│
├── dbt/                     # dbt projects and transformations
│   ├── projects/            # Each dbt project (e.g., analytics, marts)
│   ├── seeds/               # Seed data
│   └── snapshots/           # dbt snapshots
│
├── docker/                   # Dockerfiles & Docker Compose
│   ├── dev/                 # Dev environment compose
│   ├── staging/             # Staging compose
│   ├── prod/                # Production compose
│   └── entrypoint.sh        # Common entrypoint
│
├── configs/                  # Configuration files
│   ├── dev/                 # Dev configs
│   ├── staging/             # Staging configs
│   └── prod/                # Production configs
│
├── docs/                     # Project documentation
│   ├── architecture.md
│   ├── data_ingestion.md
│   ├── security.md
│   ├── storage_scaling.md
│   ├── setup.md
│   └── archive/             # Old docs backup
│
├── tests/                    # Unit & integration tests
│   ├── dagster/             # Dagster pipeline tests
│   └── dbt/                 # dbt model tests
│
├── .env.example              # Environment variable template
├── README.md                 # Project overview
└── airbyte-config.json       # Airbyte configuration


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

