#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
python -c "
import time
import psycopg2
import os

host = os.environ.get('POSTGRES_HOST', 'postgres')
port = os.environ.get('POSTGRES_PORT', '5432')
user = os.environ.get('POSTGRES_USER', 'dagster')
db = os.environ.get('POSTGRES_DB', 'dagster')

while True:
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            database=db,
            password=os.environ.get('POSTGRES_PASSWORD', 'dagster_password')
        )
        conn.close()
        print('PostgreSQL is ready!')
        break
    except psycopg2.OperationalError:
        print('Waiting for PostgreSQL...')
        time.sleep(2)
"

echo "PostgreSQL connection verified!"

# Create DAGSTER_HOME directory if it doesn't exist
mkdir -p $DAGSTER_HOME

# Initialize Dagster home if needed
if [ ! -f "$DAGSTER_HOME/dagster.yaml" ]; then
    echo "Initializing Dagster home..."
    dagster instance migrate
fi

# Create dbt profiles directory
mkdir -p $DBT_PROFILES_DIR

# Copy existing profiles.yml if it exists
if [ -f "/opt/dagster/dbt_profiles/profiles.yml" ]; then
    echo "Using existing profiles.yml"
else
    echo "No profiles.yml found - please ensure it's mounted correctly"
fi

# Execute the main command
exec "$@"

