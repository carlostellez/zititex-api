# Zititex API

[![CI](https://github.com/yourusername/zititex-api/workflows/CI/badge.svg)](https://github.com/yourusername/zititex-api/actions)
[![codecov](https://codecov.io/gh/yourusername/zititex-api/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/zititex-api)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A modern, production-ready REST API built with FastAPI following Clean Architecture principles, SOLID design patterns, and best practices for enterprise applications.

## 🏗️ Architecture

This project follows **Clean Architecture** principles, ensuring:

- ✅ **Separation of Concerns**: Clear boundaries between layers
- ✅ **Dependency Rule**: Dependencies point inward
- ✅ **Testability**: Easy to test each layer independently
- ✅ **Maintainability**: Easy to modify and extend
- ✅ **Scalability**: Ready for enterprise-level growth

### Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│              (FastAPI Routes & Schemas)                  │
├─────────────────────────────────────────────────────────┤
│                   Application Layer                      │
│           (Use Cases & Business Logic)                   │
├─────────────────────────────────────────────────────────┤
│                     Domain Layer                         │
│        (Entities, Value Objects, Interfaces)             │
├─────────────────────────────────────────────────────────┤
│                 Infrastructure Layer                     │
│  (Database, External APIs, File System, Cache)           │
└─────────────────────────────────────────────────────────┘
```

### Project Structure

```
zititex-api/
├── src/
│   ├── domain/                    # Domain Layer (Business Rules)
│   │   ├── entities/              # Business entities
│   │   │   └── base.py            # Base entity
│   │   ├── repositories/          # Repository interfaces
│   │   │   └── base.py            # Base repository interface
│   │   └── exceptions.py          # Domain exceptions
│   │
│   ├── application/               # Application Layer (Use Cases)
│   │   ├── use_cases/             # Business use cases
│   │   │   └── base.py            # Base use case
│   │   └── dto/                   # Data Transfer Objects
│   │
│   ├── infrastructure/            # Infrastructure Layer (External)
│   │   ├── config/                # Configuration
│   │   │   └── settings.py        # Application settings
│   │   ├── database/              # Database implementation
│   │   │   ├── base.py            # Base models
│   │   │   └── session.py         # Database session
│   │   └── repositories/          # Repository implementations
│   │
│   ├── presentation/              # Presentation Layer (API)
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/     # API endpoints
│   │   │       └── router.py      # API router
│   │   └── schemas/               # Pydantic schemas
│   │
│   └── main.py                    # Application entry point
│
├── tests/                         # Test suite
│   ├── unit/                      # Unit tests
│   │   └── domain/                # Domain tests
│   ├── integration/               # Integration tests
│   └── conftest.py                # Pytest fixtures
│
├── .github/                       # GitHub Actions
│   └── workflows/
│       ├── ci.yml                 # Continuous Integration
│       ├── cd.yml                 # Continuous Deployment
│       └── pr.yml                 # Pull Request checks
│
├── .pre-commit-config.yaml        # Pre-commit hooks
├── pyproject.toml                 # Project configuration
├── requirements.txt               # Production dependencies
├── requirements-dev.txt           # Development dependencies
├── Dockerfile                     # Docker image
├── docker-compose.yml             # Docker Compose setup
└── README.md                      # This file
```

## 🚀 Features

- ✅ **FastAPI** - Modern, high-performance web framework
- ✅ **Clean Architecture** - Maintainable and scalable structure
- ✅ **SOLID Principles** - Design patterns for robust code
- ✅ **SQLAlchemy 2.0** - Async ORM for database operations
- ✅ **PostgreSQL** - Production-grade database
- ✅ **Redis** - Caching and session management
- ✅ **JWT Authentication** - Secure token-based auth
- ✅ **Docker** - Containerized deployment
- ✅ **GitHub Actions** - CI/CD pipeline
- ✅ **Pre-commit Hooks** - Code quality enforcement
- ✅ **Pytest** - Comprehensive test coverage (>99%)
- ✅ **Type Hints** - Full static type checking with mypy
- ✅ **OpenAPI/Swagger** - Auto-generated API documentation

## 📋 Prerequisites

- Python 3.12+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

## 🛠️ Installation

### Local Development

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/zititex-api.git
cd zititex-api
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements-dev.txt
```

4. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Install pre-commit hooks**

```bash
pre-commit install
```

6. **Run database migrations**

```bash
alembic upgrade head
```

7. **Run the application**

```bash
uvicorn src.main:app --reload
```

### Docker Development

```bash
# Build and run all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

## 🧪 Testing

### Run all tests with coverage

```bash
pytest -v --cov=src --cov-report=term-missing --cov-report=html
```

### Run specific test types

```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# With coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html  # View coverage report
```

### Run linting and formatting

```bash
# Black (code formatting)
black src tests

# isort (import sorting)
isort src tests

# Flake8 (linting)
flake8 src tests

# MyPy (type checking)
mypy src

# Run all pre-commit hooks
pre-commit run --all-files
```

## 📚 API Documentation

Once the application is running, access the documentation at:

- **Swagger UI**: http://localhost:8000/v1/docs
- **ReDoc**: http://localhost:8000/v1/redoc
- **OpenAPI JSON**: http://localhost:8000/v1/openapi.json

## 🔌 API Examples

### Health Check

```bash
curl -X GET http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "v1"
}
```

### Detailed Health Endpoints

```bash
# Liveness probe
curl -X GET http://localhost:8000/v1/health/liveness

# Readiness probe
curl -X GET http://localhost:8000/v1/health/readiness
```

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Example Authentication Flow

1. **Register/Login** (to be implemented)

```bash
curl -X POST http://localhost:8000/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

2. **Use Access Token**

```bash
curl -X GET http://localhost:8000/v1/protected-resource \
  -H "Authorization: Bearer <your-access-token>"
```

## 🔧 Configuration

All configuration is managed through environment variables. See `.env.example` for available options:

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | Zititex API |
| `APP_ENV` | Environment (development/staging/production) | development |
| `DEBUG` | Debug mode | True |
| `DATABASE_URL` | PostgreSQL connection string | postgresql://... |
| `REDIS_URL` | Redis connection string | redis://localhost:6379/0 |
| `JWT_SECRET_KEY` | JWT secret key | change-me-in-production |
| `CORS_ORIGINS` | Allowed CORS origins | ["http://localhost:3000"] |

## 🚢 Deployment

### Docker

```bash
# Build image
docker build -t zititex-api:latest .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e REDIS_URL=redis://... \
  zititex-api:latest
```

### Kubernetes

```bash
# Apply Kubernetes manifests (to be created)
kubectl apply -f k8s/
```

### GitHub Actions

The project includes automated CI/CD pipelines:

- **CI (Continuous Integration)**: Runs on every push and PR
  - Code quality checks (black, isort, flake8, mypy)
  - Test suite with coverage
  - Security scans (bandit, safety)

- **CD (Continuous Deployment)**: Runs on main branch and tags
  - Build and push Docker image
  - Deploy to staging (main branch)
  - Deploy to production (version tags)

- **PR Checks**: Runs on pull requests
  - Enforces commit message conventions
  - Verifies test coverage (>99%)
  - Comments coverage report on PR

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Test updates
- `chore:` Maintenance tasks

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - [your.email@example.com](mailto:your.email@example.com)

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Amazing web framework
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) - Architecture principles
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID) - Design patterns

## 📊 Project Status

- 🟢 **Active Development**: Actively maintained and developed
- ✅ **Test Coverage**: >99%
- 🔒 **Security**: Following security best practices
- 📚 **Documentation**: Comprehensive and up-to-date

---

For detailed instructions on running the project, see [run.md](run.md).

For information about prompts used in development, see [prompts.md](prompts.md).

