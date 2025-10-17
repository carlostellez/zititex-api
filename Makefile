.PHONY: help install install-dev run test lint format clean docker-up docker-down migrate

help:
	@echo "Available commands:"
	@echo "  make install        - Install production dependencies"
	@echo "  make install-dev    - Install development dependencies"
	@echo "  make run            - Run the application"
	@echo "  make test           - Run tests with coverage"
	@echo "  make lint           - Run linters (flake8, mypy)"
	@echo "  make format         - Format code (black, isort)"
	@echo "  make clean          - Clean cache and build files"
	@echo "  make docker-up      - Start Docker containers"
	@echo "  make docker-down    - Stop Docker containers"
	@echo "  make migrate        - Run database migrations"
	@echo "  make pre-commit     - Install pre-commit hooks"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

install-dev:
	pip install --upgrade pip
	pip install -r requirements-dev.txt

pre-commit:
	pre-commit install
	@echo "✅ Pre-commit hooks installed"

run:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -v --cov=src --cov-report=term-missing --cov-report=html

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

lint:
	flake8 src tests --max-line-length=88 --extend-ignore=E203,W503
	mypy src --ignore-missing-imports

format:
	black src tests
	isort src tests

format-check:
	black --check src tests
	isort --check-only src tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -f .coverage

docker-up:
	docker-compose up --build -d
	@echo "✅ Docker containers started"
	@echo "API: http://localhost:8000"
	@echo "Docs: http://localhost:8000/v1/docs"
	@echo "PgAdmin: http://localhost:5050"

docker-down:
	docker-compose down
	@echo "✅ Docker containers stopped"

docker-logs:
	docker-compose logs -f api

migrate:
	alembic upgrade head

migrate-create:
	@read -p "Enter migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

migrate-rollback:
	alembic downgrade -1

db-create:
	@echo "Creating database..."
	createdb zititex_db || echo "Database already exists"

db-drop:
	@echo "Dropping database..."
	dropdb zititex_db || echo "Database does not exist"

db-reset: db-drop db-create migrate
	@echo "✅ Database reset complete"

all: install-dev pre-commit format lint test
	@echo "✅ All checks passed!"

