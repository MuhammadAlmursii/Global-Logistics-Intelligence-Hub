# Architecture Overview

This document describes the architecture of the Dagster + dbt platform.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Dagster + dbt Platform                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Dagster UI    │    │   Dagster       │                │
│  │   (Web UI)      │    │   Daemon        │                │
│  │   Port: 3000    │    │   (Background)  │                │
│  └─────────────────┘    └─────────────────┘                │
│           │                       │                         │
│           └───────────┬───────────┘                         │
│                       │                                     │
│  ┌─────────────────────────────────────────────────────────┤
│  │              Dagster Core                               │
│  │  - Asset Management                                     │
│  │  - Orchestration                                        │
│  │  - Scheduling                                          │
│  │  - Monitoring                                          │
│  └─────────────────────────────────────────────────────────┤
│                       │                                     │
│  ┌─────────────────────────────────────────────────────────┤
│  │              dbt Integration                            │
│  │  - dbt Projects                                        │
│  │  - Model Execution                                     │
│  │  - Testing                                            │
│  │  - Documentation                                      │
│  └─────────────────────────────────────────────────────────┤
│                       │                                     │
│  ┌─────────────────────────────────────────────────────────┤
│  │              Storage Layer                              │
│  │  - PostgreSQL (Dagster Metadata)                       │
│  │  - Snowflake (Data Warehouse)                          │
│  └─────────────────────────────────────────────────────────┤
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Dagster Components

#### Dagster Webserver
- **Purpose**: Web UI for monitoring and managing data pipelines
- **Port**: 3000 (dev), 3001 (staging), 3002 (prod)
- **Features**:
  - Asset lineage visualization
  - Run monitoring and history
  - Configuration management
  - Log viewing

#### Dagster Daemon
- **Purpose**: Background service for scheduling and execution
- **Functions**:
  - Asset scheduling
  - Run queuing and execution
  - Sensor evaluation
  - Scheduler management

### 2. dbt Integration

#### Project Structure
```
dbt_projects/
├── project_1/
│   ├── dbt_project.yml
│   ├── models/
│   ├── tests/
│   ├── macros/
│   └── assets/
│       └── assets.py          # Dagster integration
├── project_2/
│   └── ...
└── ...
```

#### Asset Loading
- Each dbt project has its own `assets.py` file
- Assets are automatically loaded into Dagster workspace
- Supports dbt models, tests, and custom assets

### 3. Configuration Management

#### Environment-Specific Configs
```
config/
├── dev.yml          # Development configuration
├── staging.yml      # Staging configuration
└── prod.yml         # Production configuration
```

#### Settings System
- Uses Pydantic for validation
- Environment variable based configuration
- Type-safe configuration loading

### 4. Storage Layer

#### PostgreSQL
- **Purpose**: Dagster metadata storage
- **Data**: Run history, asset definitions, configuration
- **Environments**: Separate databases per environment

#### Snowflake
- **Purpose**: Data warehouse for analytics
- **Connection**: Environment-specific credentials
- **Features**: 
  - Multi-environment support
  - Role-based access control
  - Query tagging for monitoring

## Data Flow

### 1. Development Workflow

```
Developer → Git Push → CI/CD → Staging → Production
    ↓           ↓         ↓        ↓         ↓
  Local     Automated   Deploy   Test    Deploy
 Testing    Testing     dbt      Run     dbt
```

### 2. Asset Execution Flow

```
Dagster Scheduler → dbt Project → Snowflake → Asset Update
       ↓              ↓            ↓           ↓
   Schedule      Execute Models   Query     Update
   Trigger       & Tests         Data      Metadata
```

### 3. Monitoring Flow

```
dbt Execution → Logs → Dagster UI → Alerts/Notifications
      ↓          ↓         ↓           ↓
   Run dbt    Capture   Display     Notify
   Models     Results   Status      Team
```

## Security Architecture

### 1. Authentication & Authorization

- **Environment Variables**: Secure credential storage
- **Snowflake Roles**: Environment-specific roles
- **Docker Security**: Non-root user execution

### 2. Network Security

- **Internal Communication**: Docker network isolation
- **External Access**: Controlled port exposure
- **Database Security**: Connection encryption

### 3. Data Security

- **Credential Management**: Environment-based secrets
- **Query Tagging**: Audit trail for all queries
- **Access Control**: Role-based data access

## Scalability Considerations

### 1. Horizontal Scaling

- **Multiple Dagster Instances**: Load balancing across instances
- **Database Scaling**: PostgreSQL read replicas
- **Snowflake Scaling**: Automatic warehouse scaling

### 2. Vertical Scaling

- **Resource Limits**: Docker resource constraints
- **Database Tuning**: PostgreSQL configuration optimization
- **Query Optimization**: dbt model optimization

### 3. Storage Scaling

- **Data Partitioning**: Snowflake table partitioning
- **Archival Strategy**: Data lifecycle management
- **Backup Strategy**: Automated backups

## Deployment Architecture

### 1. Development Environment

```yaml
Services:
  - postgres (port 5432)
  - dagster-webserver (port 3000)
  - dagster-daemon
```

### 2. Staging Environment

```yaml
Services:
  - postgres (port 5433)
  - dagster-webserver (port 3001)
  - dagster-daemon
```

### 3. Production Environment

```yaml
Services:
  - postgres (port 5434)
  - dagster-webserver (port 3002)
  - dagster-daemon
  - monitoring (optional)
```

## Integration Points

### 1. External Systems

- **Git**: Source code management
- **CI/CD**: Automated deployment
- **Monitoring**: System monitoring
- **Alerting**: Failure notifications

### 2. Data Sources

- **Snowflake**: Primary data warehouse
- **External APIs**: Data ingestion
- **File Systems**: File-based data
- **Databases**: Direct database connections

## Performance Considerations

### 1. Query Performance

- **Snowflake Optimization**: Proper warehouse sizing
- **dbt Optimization**: Model materialization strategies
- **Indexing**: Proper database indexing

### 2. System Performance

- **Resource Allocation**: Appropriate Docker resources
- **Caching**: Dagster asset caching
- **Parallelization**: Concurrent execution

### 3. Monitoring Performance

- **Metrics Collection**: System and business metrics
- **Logging**: Structured logging
- **Alerting**: Performance threshold alerts

## Disaster Recovery

### 1. Backup Strategy

- **Database Backups**: Regular PostgreSQL backups
- **Configuration Backups**: Environment configuration
- **Code Backups**: Git repository backups

### 2. Recovery Procedures

- **Database Recovery**: Point-in-time recovery
- **Service Recovery**: Container restart procedures
- **Data Recovery**: Snowflake data recovery

### 3. High Availability

- **Service Redundancy**: Multiple service instances
- **Database Clustering**: PostgreSQL clustering
- **Load Balancing**: Traffic distribution



