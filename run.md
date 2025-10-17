# Running Zititex API

This document provides detailed instructions on how to run the Zititex API project in different environments and scenarios.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Running Locally](#running-locally)
- [Running with Docker](#running-with-docker)
- [Database Setup](#database-setup)
- [Development Tools](#development-tools)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before running the application, ensure you have the following installed:

### Required Software

- **Python 3.12 or higher**
  ```bash
  python --version  # Should be 3.12 or higher
  ```

- **PostgreSQL 15 or higher**
  ```bash
  psql --version  # Should be 15 or higher
  ```

- **Redis 7 or higher**
  ```bash
  redis-server --version  # Should be 7 or higher
  ```

- **Git**
  ```bash
  git --version
  ```

### Optional Software

- **Docker and Docker Compose** (for containerized development)
  ```bash
  docker --version
  docker-compose --version
  ```

- **Poetry** (alternative to pip for dependency management)
  ```bash
  poetry --version
  ```

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/zititex-api.git
cd zititex-api
```

### 2. Create Python Virtual Environment

Using venv (built-in):
```bash
python -m venv venv
```

Activate the virtual environment:

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

**For development (recommended):**
```bash
pip install --upgrade pip
pip install -r requirements-dev.txt
```

**For production only:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` file with your configuration:
```bash
# Use your preferred editor
nano .env
# or
vim .env
# or
code .env  # VSCode
```

**Minimum required configuration:**
```env
APP_NAME=Zititex API
APP_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production

DATABASE_URL=postgresql://zititex:zititex@localhost:5432/zititex_db
REDIS_URL=redis://localhost:6379/0

JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
```

### 5. Install Pre-commit Hooks

```bash
pre-commit install
```

This ensures code quality checks run before each commit.

## Running Locally

### 1. Start PostgreSQL

**Using Homebrew (Mac):**
```bash
brew services start postgresql@15
```

**Using systemd (Linux):**
```bash
sudo systemctl start postgresql
```

**Using pg_ctl:**
```bash
pg_ctl -D /usr/local/var/postgres start
```

### 2. Create Database

```bash
# Connect to PostgreSQL
psql postgres

# Create database and user
CREATE DATABASE zititex_db;
CREATE USER zititex WITH PASSWORD 'zititex';
GRANT ALL PRIVILEGES ON DATABASE zititex_db TO zititex;

# Exit psql
\q
```

### 3. Start Redis

**Using Homebrew (Mac):**
```bash
brew services start redis
```

**Using systemd (Linux):**
```bash
sudo systemctl start redis
```

**Direct command:**
```bash
redis-server
```

Verify Redis is running:
```bash
redis-cli ping
# Should return: PONG
```

### 4. Run Database Migrations

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 5. Start the Application

**Development mode (with auto-reload):**
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode:**
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**With Gunicorn (production):**
```bash
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 6. Verify Application is Running

Open your browser and navigate to:

- **API Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/v1/docs
- **Alternative Docs**: http://localhost:8000/v1/redoc

Or use curl:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "v1"
}
```

## Running with Docker

### 1. Using Docker Compose (Recommended)

**Start all services:**
```bash
docker-compose up --build
```

**Run in detached mode (background):**
```bash
docker-compose up -d
```

**View logs:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
```

**Stop services:**
```bash
docker-compose down
```

**Stop and remove volumes:**
```bash
docker-compose down -v
```

### 2. Using Docker Directly

**Build the image:**
```bash
docker build -t zititex-api:latest .
```

**Run the container:**
```bash
docker run -d \
  --name zititex-api \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://zititex:zititex@postgres:5432/zititex_db \
  -e REDIS_URL=redis://redis:6379/0 \
  zititex-api:latest
```

**View logs:**
```bash
docker logs -f zititex-api
```

**Stop and remove container:**
```bash
docker stop zititex-api
docker rm zititex-api
```

### 3. Access Services

When running with Docker Compose, you can access:

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/v1/docs
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **PgAdmin**: http://localhost:5050 (admin@zititex.com / admin)

## Database Setup

### Manual Database Setup

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE zititex_db;

# Create user
CREATE USER zititex WITH PASSWORD 'zititex';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE zititex_db TO zititex;

# Connect to the new database
\c zititex_db

# Grant schema privileges
GRANT ALL ON SCHEMA public TO zititex;

# Exit
\q
```

### Verify Database Connection

```bash
# Test connection
psql -U zititex -d zititex_db -h localhost

# Or using Python
python -c "from sqlalchemy import create_engine; engine = create_engine('postgresql://zititex:zititex@localhost:5432/zititex_db'); print(engine.connect())"
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# View current version
alembic current
```

## Development Tools

### Code Formatting

```bash
# Format code with Black
black src tests

# Sort imports with isort
isort src tests

# Run both
black src tests && isort src tests
```

### Linting

```bash
# Run Flake8
flake8 src tests

# Run MyPy (type checking)
mypy src

# Run all linters
flake8 src tests && mypy src
```

### Pre-commit Hooks

```bash
# Run pre-commit on all files
pre-commit run --all-files

# Run pre-commit on staged files
pre-commit run

# Update pre-commit hooks
pre-commit autoupdate
```

## Testing

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=src --cov-report=term-missing --cov-report=html
```

View HTML coverage report:
```bash
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Run Specific Tests

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test file
pytest tests/unit/domain/test_entities.py

# Specific test function
pytest tests/unit/domain/test_entities.py::TestBaseEntity::test_base_entity_creation

# With verbose output
pytest -v

# Stop on first failure
pytest -x

# Show print statements
pytest -s
```

### Run Tests in Parallel

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests in parallel
pytest -n auto
```

## Troubleshooting

### Common Issues and Solutions

#### Issue: Port 8000 already in use

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process
kill -9 <PID>  # Mac/Linux
taskkill /PID <PID> /F  # Windows

# Or use a different port
uvicorn src.main:app --port 8001
```

#### Issue: Cannot connect to PostgreSQL

**Solution:**
```bash
# Check if PostgreSQL is running
pg_isready

# Check PostgreSQL logs
tail -f /usr/local/var/log/postgres.log  # Mac
sudo journalctl -u postgresql -f  # Linux

# Restart PostgreSQL
brew services restart postgresql@15  # Mac
sudo systemctl restart postgresql  # Linux
```

#### Issue: Cannot connect to Redis

**Solution:**
```bash
# Check if Redis is running
redis-cli ping

# Start Redis
redis-server

# Check Redis logs
tail -f /usr/local/var/log/redis.log  # Mac
```

#### Issue: Import errors

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements-dev.txt

# Check PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### Issue: Database migration errors

**Solution:**
```bash
# Drop all tables and restart
alembic downgrade base
alembic upgrade head

# Or recreate database
dropdb zititex_db
createdb zititex_db
alembic upgrade head
```

#### Issue: Tests failing

**Solution:**
```bash
# Clear pytest cache
pytest --cache-clear

# Reinstall test dependencies
pip install -r requirements-dev.txt

# Check for import errors
python -c "import src; import tests"
```

### Environment-Specific Issues

#### Mac-specific

```bash
# Install PostgreSQL and Redis with Homebrew
brew install postgresql@15 redis

# Start services
brew services start postgresql@15
brew services start redis
```

#### Linux-specific

```bash
# Install PostgreSQL and Redis (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql-15 redis-server

# Start services
sudo systemctl start postgresql
sudo systemctl start redis
```

#### Windows-specific

- Download PostgreSQL from: https://www.postgresql.org/download/windows/
- Download Redis from: https://redis.io/download (or use WSL)
- Use WSL for better compatibility with development tools

## Performance Optimization

### Running with Optimizations

```bash
# Use multiple workers
uvicorn src.main:app --workers 4

# Enable reload only in development
uvicorn src.main:app --reload  # Development
uvicorn src.main:app  # Production

# Optimize PostgreSQL connection pool
# Edit DATABASE_URL to include pool settings
DATABASE_URL=postgresql://user:pass@localhost/db?pool_size=10&max_overflow=20
```

### Monitoring

```bash
# Monitor application logs
tail -f logs/app.log

# Monitor system resources
htop  # Linux/Mac
```

## Next Steps

After successfully running the application:

1. Read the [API Documentation](http://localhost:8000/v1/docs)
2. Explore the codebase and architecture
3. Run the test suite to ensure everything works
4. Start implementing your features
5. Follow the [Contributing Guidelines](README.md#contributing)

For more information, see:
- [README.md](README.md) - Project overview and features
- [prompts.md](prompts.md) - Development prompts and guidelines

