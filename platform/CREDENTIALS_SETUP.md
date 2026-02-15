# Credentials Setup Guide

Follow these steps to configure your Dagster + dbt platform with your Snowflake credentials.

## Step 1: Create Environment File

Create a `.env` file in the root directory:

```bash
copy env.example .env
```

## Step 2: Configure Snowflake Credentials

Edit the `.env` file and replace the following values with your actual Snowflake credentials:

```bash
# REQUIRED: Replace these with your actual Snowflake values
SNOWFLAKE_ACCOUNT=your_actual_account_name
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse_name
SNOWFLAKE_DATABASE=your_database_name
SNOWFLAKE_SCHEMA=your_schema_name
SNOWFLAKE_ROLE=your_role_name
```

### Example:
```bash
SNOWFLAKE_ACCOUNT=abc12345.us-east-1
SNOWFLAKE_USER=john_doe
SNOWFLAKE_PASSWORD=my_secure_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=ANALYTICS_DB
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=ANALYST_ROLE
```

## Step 3: Verify Your Snowflake Connection

You can test your Snowflake connection using dbt:

```bash
# After setting up credentials, test the connection
docker-compose exec dagster-webserver dbt debug
```

## Step 4: Start the Platform

Once credentials are configured:

```bash
# Start the development environment
docker-compose up -d

# Check if services are running
docker-compose ps

# View logs
docker-compose logs -f
```

## Step 5: Access Dagster UI

Open your browser and go to:
- **Development**: http://localhost:3000

## Common Snowflake Account Formats

Your Snowflake account name format depends on your region:

- **US West**: `account_name.us-west-2.aws`
- **US East**: `account_name.us-east-1.aws`
- **EU**: `account_name.eu-west-1.aws`
- **Azure**: `account_name.east-us-2.azure`
- **GCP**: `account_name.us-central1.gcp`

## Security Notes

- Never commit your `.env` file to version control
- Use strong passwords for your Snowflake account
- Consider using key-pair authentication instead of passwords for production
- The `.env` file is already in `.gitignore` for security

## Troubleshooting

### Connection Issues
1. Verify your Snowflake account name format
2. Check if your user has the correct permissions
3. Ensure the warehouse is running
4. Verify the database and schema exist

### Docker Issues
1. Make sure Docker is running
2. Check if ports 3000 and 5432 are available
3. Try rebuilding containers: `docker-compose build --no-cache`

### dbt Issues
1. Test connection: `dbt debug`
2. Check profiles: `dbt debug --profiles-dir /opt/dagster/dbt_profiles`

