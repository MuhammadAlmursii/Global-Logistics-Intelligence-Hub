# Setup Guide

This guide will walk you through setting up the Dagster + dbt platform for your organization.

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Snowflake account and credentials
- Git

## Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd dbt-dagster-platform

# Copy environment template
cp env.example .env

# Edit environment variables
nano .env
```

### 2. Configure Environment Variables

Edit `.env` with your specific values:

```bash
# Snowflake Configuration
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
SNOWFLAKE_ROLE=your_role

# Environment
ENVIRONMENT=dev
```

### 3. Start Development Environment

```bash
# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f dagster-webserver
```

### 4. Access Dagster UI

Open your browser and navigate to:
- Development: http://localhost:3000
- Staging: http://localhost:3001 (if running staging)
- Production: http://localhost:3002 (if running production)

## Environment Setup

### Development Environment

```bash
# Setup development environment
python scripts/setup_environment.py dev

# Start development services
docker-compose up -d
```

### Staging Environment

```bash
# Setup staging environment
python scripts/setup_environment.py staging

# Copy staging environment variables
cp env.example .env.staging
# Edit .env.staging with staging values

# Start staging services
docker-compose -f docker-compose.staging.yml up -d
```

### Production Environment

```bash
# Setup production environment
python scripts/setup_environment.py prod

# Copy production environment variables
cp env.example .env.prod
# Edit .env.prod with production values

# Start production services
docker-compose -f docker-compose.prod.yml up -d
```

## Creating New dbt Projects

### 1. Create Project from Template

```bash
# Create a new project
python scripts/create_new_project.py my_analytics_project

# This creates:
# - dbt_projects/my_analytics_project/
# - All necessary dbt files
# - Customized assets.py for Dagster integration
```

### 2. Customize Your Project

Edit the following files in your new project:

- `dbt_project.yml` - Project configuration
- `models/` - Your dbt models
- `assets/assets.py` - Dagster asset definitions

### 3. Register Project in Workspace

Add your project to `workspace/definitions.py`:

```python
# Add to DBT_PROJECTS list
DBT_PROJECTS = [
    "my_analytics_project",
    # ... other projects
]
```

### 4. Test Your Project

```bash
# Navigate to your project
cd dbt_projects/my_analytics_project

# Install dependencies
dbt deps

# Test compilation
dbt compile

# Run models
dbt run

# Run tests
dbt test
```

## Best Practices

### Environment Management

1. **Use Environment Variables**: All sensitive data should be in environment variables
2. **Separate Configurations**: Different configs for dev/staging/prod
3. **Secure Credentials**: Never commit credentials to version control

### dbt Project Structure

```
my_analytics_project/
├── dbt_project.yml          # Project configuration
├── models/
│   ├── staging/             # Staging models (views)
│   ├── marts/               # Business models (tables)
│   ├── schema.yml           # Model documentation
│   └── sources.yml          # Source definitions
├── tests/                   # Custom tests
├── macros/                  # Custom macros
├── seeds/                   # Seed data
└── assets/
    └── assets.py            # Dagster integration
```

### Naming Conventions

- **Projects**: `snake_case` (e.g., `user_analytics`)
- **Models**: `snake_case` with prefixes:
  - Staging: `stg_` prefix
  - Marts: `mart_` prefix
- **Assets**: `project_name_asset_name`

### Testing Strategy

1. **Unit Tests**: Test individual models
2. **Integration Tests**: Test model dependencies
3. **Data Quality Tests**: Test for data issues
4. **Performance Tests**: Monitor query performance

## Troubleshooting

### Common Issues

1. **Connection Issues**
   ```bash
   # Check Snowflake connection
   dbt debug
   
   # Verify credentials
   echo $SNOWFLAKE_ACCOUNT
   ```

2. **Docker Issues**
   ```bash
   # Rebuild containers
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

3. **Permission Issues**
   ```bash
   # Fix file permissions
   chmod +x scripts/*.py
   chmod +x docker/entrypoint.sh
   ```

### Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs dagster-webserver
docker-compose logs postgres
```

## Security Considerations

1. **Environment Variables**: Use `.env` files for local development
2. **Secrets Management**: Use proper secrets management in production
3. **Network Security**: Configure proper firewall rules
4. **Access Control**: Implement proper user access controls
5. **Audit Logging**: Enable audit logging for compliance

## Monitoring and Alerting

1. **Health Checks**: Built-in health check endpoints
2. **Logging**: Structured logging with different levels
3. **Metrics**: Dagster provides built-in metrics
4. **Alerts**: Configure alerts for failures and performance issues

## Scaling Considerations

1. **Resource Limits**: Set appropriate Docker resource limits
2. **Database Scaling**: Consider PostgreSQL scaling options
3. **Horizontal Scaling**: Use multiple Dagster instances if needed
4. **Storage Scaling**: Plan for data growth in Snowflake



