# Makefile for Dagster + dbt Platform

.PHONY: help setup dev staging prod clean test lint

# Default target
help:
	@echo "Available commands:"
	@echo "  setup          - Setup development environment"
	@echo "  dev            - Start development environment"
	@echo "  staging        - Start staging environment"
	@echo "  prod           - Start production environment"
	@echo "  stop           - Stop all services"
	@echo "  clean          - Clean up containers and volumes"
	@echo "  test           - Run tests"
	@echo "  lint           - Run linting"
	@echo "  logs           - View logs"
	@echo "  shell          - Open shell in container"
	@echo "  create-project - Create new dbt project (usage: make create-project PROJECT_NAME=my_project)"

# Setup development environment
setup:
	@echo "Setting up development environment..."
	cp env.example .env
	@echo "Please edit .env with your configuration values"
	python scripts/setup_environment.py dev
	@echo "Setup complete! Edit .env and run 'make dev' to start."

# Development environment
dev:
	@echo "Starting development environment..."
	docker-compose up -d
	@echo "Dagster UI available at: http://localhost:3000"

# Staging environment
staging:
	@echo "Starting staging environment..."
	python scripts/setup_environment.py staging
	docker-compose -f docker-compose.staging.yml up -d
	@echo "Dagster UI available at: http://localhost:3001"

# Production environment
prod:
	@echo "Starting production environment..."
	python scripts/setup_environment.py prod
	docker-compose -f docker-compose.prod.yml up -d
	@echo "Dagster UI available at: http://localhost:3002"

# Stop all services
stop:
	@echo "Stopping all services..."
	docker-compose down
	docker-compose -f docker-compose.staging.yml down
	docker-compose -f docker-compose.prod.yml down

# Clean up containers and volumes
clean:
	@echo "Cleaning up containers and volumes..."
	docker-compose down -v
	docker-compose -f docker-compose.staging.yml down -v
	docker-compose -f docker-compose.prod.yml down -v
	docker system prune -f

# Run tests
test:
	@echo "Running tests..."
	docker-compose exec dagster-webserver python -m pytest tests/ -v

# Run linting
lint:
	@echo "Running linting..."
	docker-compose exec dagster-webserver black .
	docker-compose exec dagster-webserver isort .
	docker-compose exec dagster-webserver mypy .

# View logs
logs:
	@echo "Viewing logs..."
	docker-compose logs -f

# Open shell in container
shell:
	@echo "Opening shell in dagster-webserver container..."
	docker-compose exec dagster-webserver /bin/bash

# Create new dbt project
create-project:
ifndef PROJECT_NAME
	@echo "Usage: make create-project PROJECT_NAME=my_project"
	@exit 1
endif
	@echo "Creating new dbt project: $(PROJECT_NAME)"
	python scripts/create_new_project.py $(PROJECT_NAME)

# Build Docker image
build:
	@echo "Building Docker image..."
	docker-compose build

# Rebuild Docker image
rebuild:
	@echo "Rebuilding Docker image..."
	docker-compose build --no-cache

# Check service health
health:
	@echo "Checking service health..."
	@docker-compose ps

# Backup database
backup:
	@echo "Backing up database..."
	docker-compose exec postgres pg_dump -U dagster dagster > backup_$(shell date +%Y%m%d_%H%M%S).sql

# Restore database
restore:
ifndef BACKUP_FILE
	@echo "Usage: make restore BACKUP_FILE=backup_file.sql"
	@exit 1
endif
	@echo "Restoring database from $(BACKUP_FILE)..."
	docker-compose exec -T postgres psql -U dagster dagster < $(BACKUP_FILE)

# Update dependencies
update:
	@echo "Updating dependencies..."
	docker-compose exec dagster-webserver pip install --upgrade -r requirements.txt

# Format code
format:
	@echo "Formatting code..."
	black .
	isort .

# Security scan
security:
	@echo "Running security scan..."
	docker-compose exec dagster-webserver safety check
	docker-compose exec dagster-webserver bandit -r .



