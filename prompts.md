# Development Prompts

This document contains the prompts and guidelines used during the development of the Zititex API project. It serves as a reference for understanding the design decisions, development approach, and architectural patterns implemented.

## Table of Contents

- [Project Overview](#project-overview)
- [Initial Setup Prompt](#initial-setup-prompt)
- [Architecture Decisions](#architecture-decisions)
- [Design Patterns](#design-patterns)
- [Development Guidelines](#development-guidelines)
- [Testing Strategy](#testing-strategy)
- [CI/CD Configuration](#cicd-configuration)
- [Code Quality Standards](#code-quality-standards)

---

## Project Overview

**Project Name**: Zititex API

**Description**: A modern, production-ready REST API built with FastAPI following Clean Architecture principles, SOLID design patterns, and best practices for enterprise applications.

**Core Technologies**:
- Python 3.12+
- FastAPI (Web Framework)
- PostgreSQL (Database)
- Redis (Cache)
- SQLAlchemy 2.0 (ORM)
- Pytest (Testing)
- Docker (Containerization)

---

## Initial Setup Prompt

### Original Request

> "revisemos la conexion a git-hub action, creemos mcp de conexion, para tener el pre-commit, despliegues, pull, push"

Translation: "Let's review the GitHub Actions connection, create an MCP connection, to have pre-commit, deployments, pull, push"

### Interpretation

The request was to set up:
1. GitHub Actions workflows for CI/CD
2. Pre-commit hooks for code quality
3. Automated deployment pipeline
4. Git workflow integration

### Implementation Approach

Created a complete project structure from scratch with:
- Clean Architecture layers (Domain, Application, Infrastructure, Presentation)
- GitHub Actions workflows (CI, CD, PR checks)
- Pre-commit hooks configuration
- Comprehensive documentation
- Full test suite with >99% coverage target

---

## Architecture Decisions

### 1. Clean Architecture

**Prompt**: Develop with Clean Architecture

**Decision**: Implement a four-layer architecture:

```
Domain Layer (Business Logic)
    ↑
Application Layer (Use Cases)
    ↑
Infrastructure Layer (External Services)
    ↑
Presentation Layer (API Endpoints)
```

**Rationale**:
- **Separation of Concerns**: Each layer has a specific responsibility
- **Dependency Rule**: Dependencies point inward, domain is independent
- **Testability**: Easy to test each layer in isolation
- **Maintainability**: Changes in one layer don't affect others
- **Scalability**: Easy to add new features or modify existing ones

**Implementation**:
```python
# Domain Layer - Pure business logic
src/domain/
├── entities/        # Business entities
├── repositories/    # Repository interfaces
└── exceptions.py    # Domain exceptions

# Application Layer - Use cases
src/application/
├── use_cases/      # Business use cases
└── dto/            # Data transfer objects

# Infrastructure Layer - External services
src/infrastructure/
├── config/         # Configuration
├── database/       # Database implementation
└── repositories/   # Repository implementations

# Presentation Layer - API
src/presentation/
├── api/            # API endpoints
└── schemas/        # Pydantic schemas
```

### 2. SOLID Principles

**Prompt**: Keep SOLID principles in mind

**Implementation**:

#### S - Single Responsibility Principle
Each class has one reason to change.

```python
# ✅ Good: Each class has single responsibility
class UserRepository:
    """Handles user data persistence."""
    pass

class UserService:
    """Handles user business logic."""
    pass

class UserController:
    """Handles HTTP requests for users."""
    pass
```

#### O - Open/Closed Principle
Open for extension, closed for modification.

```python
# ✅ Good: Use abstract base classes
class BaseRepository(ABC):
    @abstractmethod
    async def create(self, entity: EntityType) -> EntityType:
        pass
```

#### L - Liskov Substitution Principle
Subtypes must be substitutable for their base types.

```python
# ✅ Good: Implementations follow contract
class UserRepository(BaseRepository[User]):
    async def create(self, entity: User) -> User:
        # Implementation
        pass
```

#### I - Interface Segregation Principle
Clients shouldn't depend on interfaces they don't use.

```python
# ✅ Good: Small, focused interfaces
class ReadRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[Entity]:
        pass

class WriteRepository(ABC):
    @abstractmethod
    async def create(self, entity: Entity) -> Entity:
        pass
```

#### D - Dependency Inversion Principle
Depend on abstractions, not concretions.

```python
# ✅ Good: Depend on interface, not implementation
class UserUseCase:
    def __init__(self, repository: BaseRepository):
        self.repository = repository  # Interface, not concrete class
```

### 3. Dependency Injection

**Pattern**: Constructor injection for dependencies

```python
# Repository depends on database session (injected)
class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

# Use case depends on repository (injected)
class CreateUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository
```

### 4. Repository Pattern

**Pattern**: Abstract data access behind repository interface

```python
# Interface (Domain Layer)
class BaseRepository(ABC, Generic[EntityType]):
    @abstractmethod
    async def create(self, entity: EntityType) -> EntityType:
        pass

# Implementation (Infrastructure Layer)
class SQLAlchemyRepository(BaseRepository[User]):
    async def create(self, entity: User) -> User:
        # Database-specific implementation
        pass
```

---

## Design Patterns

### 1. Factory Pattern

**Use Case**: Creating complex objects

```python
def create_application() -> FastAPI:
    """Factory for creating FastAPI application."""
    app = FastAPI(...)
    # Configure middleware, routes, etc.
    return app
```

### 2. Singleton Pattern

**Use Case**: Configuration management

```python
@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance (singleton)."""
    return Settings()
```

### 3. Strategy Pattern

**Use Case**: Different algorithms for same operation

```python
class AuthenticationStrategy(ABC):
    @abstractmethod
    async def authenticate(self, credentials: dict) -> User:
        pass

class JWTAuthentication(AuthenticationStrategy):
    async def authenticate(self, credentials: dict) -> User:
        # JWT implementation
        pass
```

---

## Development Guidelines

### 1. Code Quality

**Prompt**: Follow best practices pre-commit

**Implementation**:
- **Black**: Code formatting (line length: 88)
- **isort**: Import sorting
- **Flake8**: Linting
- **MyPy**: Static type checking
- **Pytest**: Automated tests before commit

**Pre-commit Hook Configuration**:
```yaml
repos:
  - repo: https://github.com/psf/black
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    hooks:
      - id: flake8
  - repo: https://github.com/pre-commit/mirrors-mypy
    hooks:
      - id: mypy
  - repo: local
    hooks:
      - id: pytest
```

### 2. Type Hints

**Prompt**: Program in English with clear documentation

**Implementation**: Full type hints on all functions

```python
async def create_user(
    user_data: UserCreateDTO,
    repository: UserRepository
) -> UserDTO:
    """
    Create a new user.

    Args:
        user_data: User creation data
        repository: User repository

    Returns:
        Created user DTO

    Raises:
        ValidationException: If validation fails
    """
    pass
```

### 3. Documentation

**Prompt**: Program in English. Be clearer in your documentation

**Implementation**:
- Docstrings for all modules, classes, and functions
- Type hints for all parameters and return values
- Comprehensive README.md
- Detailed run.md for execution instructions
- This prompts.md for development context

### 4. Test Coverage

**Prompt**: Keep pytest coverage above 99% in mind

**Implementation**:
```toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=term-missing --cov-fail-under=99"
```

**Testing Strategy**:
- Unit tests for domain logic
- Integration tests for API endpoints
- Fixtures for common test data
- Mocks for external dependencies

---

## Testing Strategy

### Test Structure

```
tests/
├── unit/              # Unit tests (fast, isolated)
│   └── domain/        # Domain logic tests
├── integration/       # Integration tests (slower, with DB)
│   └── test_api.py    # API endpoint tests
└── conftest.py        # Shared fixtures
```

### Test Fixtures

```python
@pytest.fixture
async def test_db() -> AsyncSession:
    """Test database session."""
    # Create in-memory database
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # ... setup and teardown
```

### Coverage Requirements

- **Minimum**: 99% code coverage
- **Excluded**: `__init__.py`, migrations, type stubs
- **Focus**: Business logic and API endpoints

---

## CI/CD Configuration

### GitHub Actions Workflows

#### 1. Continuous Integration (ci.yml)

**Triggers**: Push to main/develop, Pull Requests

**Jobs**:
1. **Lint**: Black, isort, Flake8, MyPy
2. **Test**: Pytest with coverage
3. **Security**: Safety, Bandit

**Services**: PostgreSQL, Redis (for integration tests)

#### 2. Continuous Deployment (cd.yml)

**Triggers**: 
- Push to main (staging)
- Tags v* (production)

**Jobs**:
1. **Build**: Docker image
2. **Push**: Docker Hub
3. **Deploy**: Staging/Production

#### 3. Pull Request Checks (pr.yml)

**Triggers**: Pull Request opened/updated

**Jobs**:
1. **Pre-commit**: Run all hooks
2. **Coverage**: Verify >99%
3. **Semantic PR**: Check commit message format

---

## Code Quality Standards

### 1. Formatting

- **Line Length**: 88 characters (Black default)
- **Quotes**: Double quotes for strings
- **Imports**: Sorted with isort, grouped by standard/third-party/local

### 2. Naming Conventions

- **Classes**: PascalCase (e.g., `UserRepository`)
- **Functions**: snake_case (e.g., `create_user`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_USERS`)
- **Private**: Prefix with underscore (e.g., `_internal_method`)

### 3. Error Handling

```python
# Domain exceptions
class DomainException(Exception):
    """Base domain exception."""
    pass

class EntityNotFoundException(DomainException):
    """Entity not found."""
    pass

# Usage
if not user:
    raise EntityNotFoundException("User", user_id)
```

### 4. Async/Await

- Use `async`/`await` for I/O operations
- Repository methods are async
- Use cases are async
- API endpoints are async

---

## Documentation Standards

### 1. README.md

**Prompt**: Always update README.md with API design, architecture, distribution, organization, and examples

**Contents**:
- Project overview
- Architecture diagrams
- Features list
- Installation instructions
- API examples
- Configuration guide
- Deployment instructions

### 2. run.md

**Prompt**: Always update run.md with detailed and implicit instructions on how to run the project

**Contents**:
- Prerequisites
- Step-by-step setup
- Running locally
- Running with Docker
- Database setup
- Troubleshooting
- Development tools

### 3. prompts.md (This File)

**Prompt**: Always update prompts.md with each prompt used for project development

**Contents**:
- Project overview
- Initial setup prompts
- Architecture decisions
- Design patterns
- Development guidelines
- Testing strategy
- CI/CD configuration

---

## Future Prompts and Considerations

### Authentication & Authorization

**Future Prompt**: "Implement JWT-based authentication with role-based access control"

**Considerations**:
- User registration and login endpoints
- JWT token generation and validation
- Role-based permissions
- Refresh token mechanism
- Password hashing with bcrypt

### Database Migrations

**Future Prompt**: "Set up Alembic for database migrations"

**Considerations**:
- Auto-generate migrations from models
- Version control for database schema
- Rollback capabilities
- Separate migrations for development/production

### Logging and Monitoring

**Future Prompt**: "Implement structured logging and monitoring"

**Considerations**:
- Structured JSON logging
- Request/response logging
- Error tracking (Sentry)
- Performance monitoring (Prometheus)
- Distributed tracing (OpenTelemetry)

### API Versioning

**Future Prompt**: "Implement API versioning strategy"

**Considerations**:
- URL-based versioning (v1, v2)
- Backward compatibility
- Deprecation warnings
- Version sunset policy

### Rate Limiting

**Future Prompt**: "Add rate limiting to API endpoints"

**Considerations**:
- Redis-based rate limiting
- Per-user/IP limits
- Different limits per endpoint
- Rate limit headers in response

---

## Lessons Learned

### What Worked Well

1. **Clean Architecture**: Easy to understand and maintain
2. **Pre-commit Hooks**: Caught issues before commit
3. **Comprehensive Tests**: High confidence in changes
4. **Type Hints**: Better IDE support and error catching
5. **Documentation**: Easy onboarding for new developers

### Areas for Improvement

1. **Initial Setup Time**: Consider project templates
2. **Test Data Management**: Need better fixture organization
3. **Migration Strategy**: Document database changes better
4. **Performance Benchmarks**: Add performance testing
5. **Security Audits**: Regular security reviews needed

---

## References

### Clean Architecture
- [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) by Robert C. Martin

### SOLID Principles
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID) - Wikipedia

### FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)

### Testing
- [Pytest Documentation](https://docs.pytest.org/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)

### CI/CD
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Last Updated**: October 17, 2025

**Maintained By**: Development Team

**Version**: 1.0.0

