@echo off
echo ========================================
echo Dagster + dbt Platform Setup
echo ========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not running. Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo ✓ Docker is running

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy env.example .env
    echo.
    echo ⚠️  IMPORTANT: Please edit .env file with your Snowflake credentials
    echo    Open .env in your editor and replace the placeholder values
    echo.
    pause
)

REM Create necessary directories
echo Creating directories...
if not exist "profiles" mkdir profiles
if not exist "dbt_projects" mkdir dbt_projects
if not exist "logs" mkdir logs
if not exist "target" mkdir target

echo ✓ Directories created

REM Build Docker images
echo Building Docker images...
docker-compose build

if errorlevel 1 (
    echo ERROR: Failed to build Docker images
    pause
    exit /b 1
)

echo ✓ Docker images built successfully

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your Snowflake credentials
echo 2. Run: docker-compose up -d
echo 3. Open http://localhost:3000 in your browser
echo.
echo Commands:
echo   Start:     docker-compose up -d
echo   Stop:      docker-compose down
echo   Logs:      docker-compose logs -f
echo   Status:    docker-compose ps
echo.
pause

