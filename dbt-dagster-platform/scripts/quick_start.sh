#!/bin/bash

# Quick Start Script for Dagster + dbt Platform
# This script sets up and starts the platform for the first time

set -e

echo "🚀 Starting Dagster + dbt Platform Quick Start"
echo "=============================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env with your Snowflake credentials before continuing."
    echo "   Press Enter when you're ready to continue..."
    read
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p profiles dbt_projects logs target

# Setup development environment
echo "🔧 Setting up development environment..."
python scripts/setup_environment.py dev

# Build Docker images
echo "🐳 Building Docker images..."
docker-compose build

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🔍 Checking service health..."
if docker-compose ps | grep -q "Up"; then
    echo "✅ Services are running!"
    echo ""
    echo "🎉 Setup complete! Your Dagster + dbt platform is ready."
    echo ""
    echo "📊 Access your platforms:"
    echo "   - Dagster UI: http://localhost:3000"
    echo "   - PostgreSQL: localhost:5432"
    echo ""
    echo "🔧 Next steps:"
    echo "   1. Create your first dbt project:"
    echo "      make create-project PROJECT_NAME=my_first_project"
    echo ""
    echo "   2. View logs:"
    echo "      make logs"
    echo ""
    echo "   3. Stop services:"
    echo "      make stop"
    echo ""
else
    echo "❌ Some services failed to start. Check logs with: make logs"
    exit 1
fi



