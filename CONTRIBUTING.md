# Contributing to Zititex API

Thank you for considering contributing to Zititex API! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code Standards](#code-standards)
- [Testing Requirements](#testing-requirements)

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/zititex-api.git
   cd zititex-api
   ```
3. **Set up development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements-dev.txt
   pre-commit install
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Process

### 1. Make Your Changes

- Follow the [Clean Architecture](README.md#architecture) structure
- Apply [SOLID principles](README.md#solid-principles)
- Write clear, self-documenting code
- Add docstrings to all functions and classes
- Use type hints for all parameters and return values

### 2. Run Quality Checks

Before committing, ensure your code passes all checks:

```bash
# Format code
make format

# Run linters
make lint

# Run tests
make test
```

Or use pre-commit hooks (runs automatically on commit):
```bash
pre-commit run --all-files
```

### 3. Write Tests

All new features must include tests:

- **Unit tests** for business logic (domain layer)
- **Integration tests** for API endpoints
- Maintain **>99% code coverage**

```bash
# Run tests with coverage
pytest --cov=src --cov-report=term-missing

# Coverage must be >99%
```

### 4. Update Documentation

Update relevant documentation:

- **README.md**: For new features or architecture changes
- **run.md**: For setup or running instructions
- **prompts.md**: For development decisions and patterns
- **Docstrings**: For all new functions and classes

## Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, missing semicolons, etc.)
- **refactor**: Code refactoring (no functional changes)
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **build**: Changes to build system or dependencies
- **ci**: Changes to CI configuration
- **chore**: Other changes (maintenance, etc.)
- **revert**: Revert a previous commit

### Examples

```bash
# Feature
git commit -m "feat(auth): add JWT authentication"

# Bug fix
git commit -m "fix(api): resolve null pointer in user endpoint"

# Documentation
git commit -m "docs(readme): update installation instructions"

# Refactor
git commit -m "refactor(domain): simplify entity validation logic"

# Test
git commit -m "test(auth): add tests for login endpoint"
```

### Commit Message Guidelines

- Use present tense ("add feature" not "added feature")
- Use imperative mood ("move cursor to..." not "moves cursor to...")
- First line should be 50 characters or less
- Reference issues and pull requests after the first line
- Be clear and descriptive

## Pull Request Process

### 1. Prepare Your Pull Request

Before opening a PR:

- ✅ All tests pass locally
- ✅ Code is formatted (black, isort)
- ✅ Linters pass (flake8, mypy)
- ✅ Coverage is >99%
- ✅ Documentation is updated
- ✅ Commit messages follow convention

### 2. Open Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Open a Pull Request on GitHub

3. Fill out the PR template with:
   - Description of changes
   - Related issue number (if applicable)
   - Screenshots (if UI changes)
   - Testing steps

### 3. PR Title Format

Follow the same convention as commit messages:

```
feat(scope): description of changes
fix(scope): description of bug fix
docs(scope): description of documentation changes
```

### 4. Code Review Process

- At least one approval required
- All CI checks must pass
- Address review comments
- Keep PR focused and small (easier to review)

### 5. After Approval

Once approved:
- Squash commits if necessary
- Merge to main branch
- Delete feature branch

## Code Standards

### Python Style

- Follow **PEP 8** style guide
- Use **Black** for formatting (line length: 88)
- Use **isort** for import sorting
- Use **type hints** for all functions
- Write **docstrings** for all public functions

### Code Structure

```python
"""Module docstring explaining purpose."""

from typing import List, Optional

from fastapi import APIRouter

from src.domain.entities import User


class UserRepository:
    """Repository for user data access.
    
    This class handles all database operations related to users,
    following the repository pattern.
    """
    
    async def create(self, user: User) -> User:
        """
        Create a new user.
        
        Args:
            user: User entity to create
            
        Returns:
            Created user entity
            
        Raises:
            ValidationException: If user data is invalid
            EntityAlreadyExistsException: If user already exists
        """
        # Implementation
        pass
```

### Architecture Rules

1. **Domain Layer**:
   - No dependencies on other layers
   - Pure business logic
   - Framework-agnostic

2. **Application Layer**:
   - Depends only on domain layer
   - Implements use cases
   - Orchestrates domain objects

3. **Infrastructure Layer**:
   - Implements domain interfaces
   - Handles external services
   - Database, APIs, file system

4. **Presentation Layer**:
   - HTTP/API layer
   - Input validation with Pydantic
   - Error handling

## Testing Requirements

### Test Structure

```python
import pytest
from unittest.mock import Mock

class TestUserRepository:
    """Test user repository."""
    
    @pytest.fixture
    def repository(self, test_db):
        """Create repository instance."""
        return UserRepository(test_db)
    
    async def test_create_user_success(self, repository):
        """Test successful user creation."""
        # Arrange
        user = User(name="Test User", email="test@example.com")
        
        # Act
        result = await repository.create(user)
        
        # Assert
        assert result.id is not None
        assert result.name == "Test User"
```

### Coverage Requirements

- **Minimum**: 99% coverage
- **Focus**: Business logic and critical paths
- **Exclude**: `__init__.py`, migrations, type stubs

### Test Commands

```bash
# Run all tests
make test

# Run specific test file
pytest tests/unit/domain/test_entities.py -v

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/unit/test_file.py::TestClass::test_method
```

## Questions or Problems?

- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions
- **Security**: Email security@example.com

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Zititex API! 🎉

