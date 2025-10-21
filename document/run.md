# How to Run Zititex API

This document provides detailed, step-by-step instructions for running the Zititex API in different environments.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Development](#docker-development)
4. [Production Deployment](#production-deployment)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **Python**: 3.12 or higher
- **MySQL**: 8.0 or higher
- **Docker**: 20.10+ (optional, for containerized deployment)
- **Docker Compose**: 1.29+ (optional)
- **Git**: Latest version

### Account Requirements

- **Mailgun Account**: For email functionality
  - Sign up at https://www.mailgun.com/
  - Obtain API key and domain

---

## Local Development Setup

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone <repository-url>
cd zititex-api

# Verify Python version
python --version  # Should be 3.12+
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Verify activation (you should see (venv) in your prompt)
which python  # Should point to venv/bin/python
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

### Step 4: Setup MySQL Database

#### Option A: Using MySQL Command Line

```bash
# Login to MySQL
mysql -u root -p

# Create database and user
CREATE DATABASE zititex_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'zititex_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON zititex_db.* TO 'zititex_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Verify database creation
mysql -u zititex_user -p zititex_db
SHOW TABLES;
EXIT;
```

#### Option B: Using MySQL Workbench

1. Open MySQL Workbench
2. Connect to your MySQL server
3. Create new schema: `zititex_db`
4. Create user: `zititex_user` with password
5. Grant privileges to the user

### Step 5: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your configuration
nano .env  # or use your preferred editor
```

**Required Configuration in .env:**

```env
# Application
APP_NAME=Zititex API
DEBUG=true

# MySQL Database
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=zititex_user
MYSQL_PASSWORD=your_secure_password
MYSQL_DATABASE=zititex_db
DATABASE_ECHO=true

# Mailgun
MAILGUN_API_KEY=your_mailgun_api_key_here
MAILGUN_DOMAIN=your_mailgun_domain_here
ADMIN_EMAIL=your_admin_email@example.com

# CORS (Allow all for development)
ALLOWED_ORIGINS=*
```

### Step 6: Run the Application

```bash
# Method 1: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Method 2: Using Makefile
make dev

# Method 3: Using Python module
python -m uvicorn app.main:app --reload
```

### Step 7: Verify Installation

Open your browser and visit:

- **API Root**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **ReDoc**: http://localhost:8000/redoc

Expected health check response:
```json
{
  "status": "healthy",
  "service": "Zititex API",
  "version": "0.1.0"
}
```

### Step 8: Test the Contact API

```bash
# Using curl
curl -X POST http://localhost:8000/api/v1/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "email": "test@example.com",
    "phone": "1234567890",
    "message": "This is a test message"
  }'

# Using httpie (if installed)
http POST http://localhost:8000/api/v1/contact/ \
  full_name="Test User" \
  email="test@example.com" \
  phone="1234567890" \
  message="This is a test message"
```

---

## Docker Development

### Step 1: Prerequisites

```bash
# Verify Docker installation
docker --version
docker-compose --version

# Ensure Docker daemon is running
docker ps
```

### Step 2: Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env for Docker environment
nano .env
```

**Docker Environment Configuration:**

```env
# MySQL (will be created by Docker)
MYSQL_HOST=mysql  # This is the Docker service name
MYSQL_PORT=3306
MYSQL_USER=dev_user
MYSQL_PASSWORD=dev_pass
MYSQL_DATABASE=zititex_db
MYSQL_ROOT_PASSWORD=rootpass

# Mailgun
MAILGUN_API_KEY=your_mailgun_api_key
MAILGUN_DOMAIN=your_mailgun_domain
ADMIN_EMAIL=admin@example.com

# Ports
API_PORT=8001
PHPMYADMIN_PORT=8081
```

### Step 3: Build and Start Services

```bash
# Build Docker images
docker-compose -f docker-compose.dev.yml build

# Start all services (API + MySQL + PhpMyAdmin)
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Check running containers
docker ps
```

You should see three containers running:
- `zititex-api-dev` (FastAPI application)
- `zititex-mysql-dev` (MySQL database)
- `zititex-phpmyadmin-dev` (PhpMyAdmin)

### Step 4: Access Services

- **API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs
- **PhpMyAdmin**: http://localhost:8081
  - Server: mysql
  - Username: root
  - Password: (from MYSQL_ROOT_PASSWORD in .env)

### Step 5: Useful Docker Commands

```bash
# View logs from specific service
docker-compose -f docker-compose.dev.yml logs -f api

# Execute commands in running container
docker exec -it zititex-api-dev bash

# Restart services
docker-compose -f docker-compose.dev.yml restart

# Stop services
docker-compose -f docker-compose.dev.yml down

# Stop and remove volumes (clean slate)
docker-compose -f docker-compose.dev.yml down -v

# Rebuild and restart after code changes
docker-compose -f docker-compose.dev.yml up -d --build
```

### Step 6: Database Management

```bash
# Connect to MySQL container
docker exec -it zititex-mysql-dev mysql -u root -p

# View database tables
SHOW DATABASES;
USE zititex_db;
SHOW TABLES;
SELECT * FROM client;
```

---

## Production Deployment

### Docker Production

```bash
# Build production image
docker-compose build

# Start production services
docker-compose up -d

# View logs
docker-compose logs -f api

# Access API
curl http://localhost:8000/health
```

### AWS Lambda (Serverless)

#### Prerequisites

```bash
# Install Node.js and npm
node --version  # v14+ required
npm --version

# Install Serverless Framework
npm install -g serverless

# Configure AWS credentials
aws configure
```

#### Deployment Steps

```bash
# Install serverless plugins
npm install

# Deploy to development
serverless deploy --stage dev

# Deploy to production
serverless deploy --stage prod

# View deployment info
serverless info --stage prod

# View logs
serverless logs -f api --tail --stage prod

# Remove deployment
serverless remove --stage dev
```

#### Environment Variables for Lambda

Add these to AWS Systems Manager Parameter Store or serverless.yml:

```yaml
environment:
  MYSQL_HOST: your-rds-endpoint
  MYSQL_USER: ${ssm:/zititex/mysql/user}
  MYSQL_PASSWORD: ${ssm:/zititex/mysql/password}
  MAILGUN_API_KEY: ${ssm:/zititex/mailgun/api_key}
  MAILGUN_DOMAIN: ${ssm:/zititex/mailgun/domain}
  ADMIN_EMAIL: ${ssm:/zititex/admin_email}
```

---

## Testing

### Run All Tests

```bash
# Activate virtual environment first
source venv/bin/activate

# Run tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html --cov-report=term

# View HTML coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Run Specific Tests

```bash
# Test specific file
pytest tests/test_api_contact.py

# Test specific function
pytest tests/test_api_contact.py::TestContactAPI::test_submit_contact_form_success

# Run with verbose output
pytest -vv

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

### Code Quality Checks

```bash
# Format code
black app tests
isort app tests

# Run linters
flake8 app tests
mypy app

# Run all checks using Makefile
make format
make lint
make test
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Database Connection Error

**Problem**: `sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (2003, "Can't connect to MySQL server")`

**Solutions**:
```bash
# Check MySQL is running
sudo systemctl status mysql  # Linux
brew services list  # macOS

# Verify credentials in .env
cat .env | grep MYSQL

# Test MySQL connection
mysql -h localhost -u zititex_user -p

# Check if port 3306 is in use
sudo lsof -i :3306  # macOS/Linux
netstat -ano | findstr :3306  # Windows
```

#### 2. Import Errors

**Problem**: `ModuleNotFoundError: No module named 'app'`

**Solutions**:
```bash
# Ensure virtual environment is activated
which python  # Should point to venv

# Reinstall dependencies
pip install -r requirements.txt

# Run from project root directory
pwd  # Should be .../zititex-api
```

#### 3. Port Already in Use

**Problem**: `ERROR: [Errno 48] Address already in use`

**Solutions**:
```bash
# Find process using port 8000
lsof -ti:8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process
kill -9 <PID>  # macOS/Linux

# Use different port
uvicorn app.main:app --port 8001
```

#### 4. Docker Container Won't Start

**Problem**: Container exits immediately or won't start

**Solutions**:
```bash
# Check logs
docker-compose -f docker-compose.dev.yml logs api

# Check container status
docker ps -a

# Rebuild without cache
docker-compose -f docker-compose.dev.yml build --no-cache

# Remove all containers and volumes
docker-compose -f docker-compose.dev.yml down -v
docker system prune -a
```

#### 5. Test Failures

**Problem**: Tests fail with database errors

**Solutions**:
```bash
# Clean test database
rm -f test.db

# Reinstall test dependencies
pip install -r requirements.txt

# Run tests with verbose output
pytest -vv

# Check specific failing test
pytest tests/test_api_contact.py -vv -s
```

#### 6. Email Not Sending

**Problem**: Contact form submits but no email received

**Solutions**:
```bash
# Verify Mailgun credentials
echo $MAILGUN_API_KEY
echo $MAILGUN_DOMAIN

# Check Mailgun logs at https://app.mailgun.com/

# Test with mock email service
# Set in .env:
MAILGUN_API_KEY=test-key
MAILGUN_DOMAIN=test.mailgun.org
```

### Getting Help

If you encounter issues not covered here:

1. Check application logs: `docker-compose logs -f`
2. Check database logs: `docker-compose logs -f mysql`
3. Review `.env` configuration
4. Check GitHub Issues
5. Contact the development team

---

## Quick Reference Commands

```bash
# Development
make dev                    # Run development server
make test                   # Run tests
make format                 # Format code
make lint                   # Run linters

# Docker
make docker-up-dev          # Start dev containers
make docker-down-dev        # Stop dev containers
make docker-logs-dev        # View logs
make docker-clean           # Clean everything

# Database
make db-migrate             # Create migration
make db-upgrade             # Apply migrations
make db-reset               # Reset database

# Deployment
make deploy-dev             # Deploy to dev
make deploy-prod            # Deploy to production
```

---

## Next Steps

After successfully running the application:

1. ✅ Explore API documentation at `/docs`
2. ✅ Test the contact endpoint
3. ✅ Check database records in PhpMyAdmin
4. ✅ Review email notifications in Mailgun
5. ✅ Run the test suite
6. ✅ Read the architecture documentation in README.md
7. ✅ Set up pre-commit hooks: `pre-commit install`

---

For more information, refer to [README.md](README.md) and [prompts.md](prompts.md).

