-- Initialize database for Dagster
CREATE DATABASE IF NOT EXISTS dagster_dev;
CREATE DATABASE IF NOT EXISTS dagster_staging;
CREATE DATABASE IF NOT EXISTS dagster_prod;

-- Create users for different environments
CREATE USER IF NOT EXISTS dagster_dev WITH PASSWORD 'dagster_dev_password';
CREATE USER IF NOT EXISTS dagster_staging WITH PASSWORD 'dagster_staging_password';
CREATE USER IF NOT EXISTS dagster_prod WITH PASSWORD 'dagster_prod_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE dagster_dev TO dagster_dev;
GRANT ALL PRIVILEGES ON DATABASE dagster_staging TO dagster_staging;
GRANT ALL PRIVILEGES ON DATABASE dagster_prod TO dagster_prod;

