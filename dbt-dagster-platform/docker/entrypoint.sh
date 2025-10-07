#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
  sleep 2
done

echo "PostgreSQL is ready!"

# Create DAGSTER_HOME directory if it doesn't exist
mkdir -p $DAGSTER_HOME

# Initialize Dagster home if needed
if [ ! -f "$DAGSTER_HOME/dagster.yaml" ]; then
    echo "Initializing Dagster home..."
    dagster instance migrate
fi

# Create dbt profiles directory
mkdir -p $DBT_PROFILES_DIR

# Generate dbt profiles.yml if it doesn't exist
if [ ! -f "$DBT_PROFILES_DIR/profiles.yml" ]; then
    echo "Generating dbt profiles.yml..."
    cat > $DBT_PROFILES_DIR/profiles.yml << EOF
config:
  send_anonymous_usage_stats: false
  use_colors: true

your_project_name:
  target: ${ENVIRONMENT:-dev}
  outputs:
    ${ENVIRONMENT:-dev}:
      type: snowflake
      account: ${SNOWFLAKE_ACCOUNT}
      user: ${SNOWFLAKE_USER}
      password: ${SNOWFLAKE_PASSWORD}
      role: ${SNOWFLAKE_ROLE}
      database: ${SNOWFLAKE_DATABASE}
      warehouse: ${SNOWFLAKE_WAREHOUSE}
      schema: ${SNOWFLAKE_SCHEMA}
      threads: 4
      client_session_keep_alive: False
      query_tag: dagster_dbt
EOF
fi

# Execute the main command
exec "$@"

