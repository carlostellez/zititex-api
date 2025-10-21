# Makefile for Zititex API Project

.PHONY: help install dev test lint format clean docker-build docker-up docker-down docker-logs

# Default target
help:
	@echo "Zititex API - Available Commands:"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install          Install dependencies"
	@echo "  make install-dev      Install dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make dev              Run development server"
	@echo "  make test             Run tests with coverage"
	@echo "  make test-verbose     Run tests with verbose output"
	@echo "  make lint             Run linters (flake8, mypy)"
	@echo "  make format           Format code (black, isort)"
	@echo "  make pre-commit       Run pre-commit hooks"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build     Build Docker images"
	@echo "  make docker-up        Start all services"
	@echo "  make docker-up-dev    Start development services"
	@echo "  make docker-down      Stop all services"
	@echo "  make docker-logs      View container logs"
	@echo "  make docker-clean     Remove containers and volumes"
	@echo ""
	@echo "Database:"
	@echo "  make db-migrate       Run database migrations"
	@echo "  make db-upgrade       Upgrade database"
	@echo "  make db-downgrade     Downgrade database"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove generated files"
	@echo "  make clean-all        Remove all generated files and caches"

# Installation
install:
	pip install --upgrade pip
	pip install -r requirements.txt

install-dev: install
	pip install -e .

# Development
dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Testing
test:
	pytest

test-verbose:
	pytest -vv

test-coverage:
	pytest --cov=app --cov-report=html --cov-report=term

# Code Quality
lint:
	flake8 app tests
	mypy app

format:
	black app tests
	isort app tests

pre-commit:
	pre-commit run --all-files

# Docker - Production
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-restart:
	docker-compose restart

docker-clean:
	docker-compose down -v
	docker system prune -f

# Docker - Development
docker-build-dev:
	docker-compose -f docker-compose.dev.yml build

docker-up-dev:
	docker-compose -f docker-compose.dev.yml up -d

docker-down-dev:
	docker-compose -f docker-compose.dev.yml down

docker-logs-dev:
	docker-compose -f docker-compose.dev.yml logs -f

docker-shell:
	docker exec -it zititex-api-dev bash

# Database
db-migrate:
	alembic revision --autogenerate -m "$(message)"

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

db-reset:
	alembic downgrade base
	alembic upgrade head

# Cleanup
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -f test.db

clean-all: clean
	rm -rf venv
	rm -rf env
	rm -rf .tox
	rm -rf .mypy_cache
	docker-compose down -v

# AWS Lambda Deployment
deploy-prod:
	serverless deploy --stage prod

deploy-dev:
	serverless deploy --stage dev

# Run in different environments
run-local:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

run-prod:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

