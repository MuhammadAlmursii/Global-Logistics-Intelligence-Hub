FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DAGSTER_HOME=/opt/dagster/dagster_home
ENV DBT_PROFILES_DIR=/opt/dagster/dbt_profiles

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories
RUN mkdir -p /opt/dagster/dagster_home \
    /opt/dagster/dbt_profiles \
    /opt/dagster/dbt_projects \
    /opt/dagster/workspace

# Set working directory
WORKDIR /opt/dagster

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy configuration files
COPY config/ ./config/
COPY docker/entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Copy workspace files
COPY workspace/ ./workspace/

# Create non-root user
RUN useradd --create-home --shell /bin/bash dagster && \
    chown -R dagster:dagster /opt/dagster

USER dagster

# Expose port
EXPOSE 3000

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]
