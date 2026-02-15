-- Initialize database for Dagster
-- Note: PostgreSQL doesn't support IF NOT EXISTS for CREATE DATABASE
-- These commands will be run only once during container initialization

-- Create users for different environments (ignore errors if they already exist)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'dagster_dev') THEN
        CREATE USER dagster_dev WITH PASSWORD 'dagster_dev_password';
    END IF;
END
$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'dagster_staging') THEN
        CREATE USER dagster_staging WITH PASSWORD 'dagster_staging_password';
    END IF;
END
$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'dagster_prod') THEN
        CREATE USER dagster_prod WITH PASSWORD 'dagster_prod_password';
    END IF;
END
$$;

-- Create databases (ignore errors if they already exist)
SELECT 'CREATE DATABASE dagster_dev'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'dagster_dev')\gexec

SELECT 'CREATE DATABASE dagster_staging'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'dagster_staging')\gexec

SELECT 'CREATE DATABASE dagster_prod'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'dagster_prod')\gexec

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE dagster_dev TO dagster_dev;
GRANT ALL PRIVILEGES ON DATABASE dagster_staging TO dagster_staging;
GRANT ALL PRIVILEGES ON DATABASE dagster_prod TO dagster_prod;

