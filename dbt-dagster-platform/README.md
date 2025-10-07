# Dagster + dbt Platform

A production-ready platform for orchestrating dbt projects with Dagster, following best practices for multi-environment deployments.

## Architecture

This platform provides:
- Centralized configuration management
- Environment-specific deployments (dev, staging, prod)
- Docker containerization
- Snowflake integration
- Template system for new dbt projects

## Quick Start

1. **Setup Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your specific values
   ```

2. **Start Development Environment**
   ```bash
   docker-compose up -d
   ```

3. **Access Dagster UI**
   - Navigate to http://localhost:3000

## Project Structure

```
├── config/                 # Environment configurations
│   ├── dev/
│   ├── staging/
│   └── prod/
├── templates/              # Project templates
│   └── dbt-project/
├── docker/                 # Docker configurations
├── scripts/                # Utility scripts
└── docs/                   # Documentation
```

## Creating New dbt Projects

1. Copy the template:
   ```bash
   cp -r templates/dbt-project/ your-new-project/
   ```

2. Update configuration in your project's `assets.py`

3. Register the project in Dagster

## Best Practices

- Environment variables for all sensitive data
- Separate configurations per environment
- Containerized deployments
- Centralized credential management
- Automated testing and validation

