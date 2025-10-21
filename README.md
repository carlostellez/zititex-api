# Zititex API

A modern, production-ready FastAPI application with MySQL database integration, designed for handling contact form submissions with email notifications.

## 🏗️ Architecture

This project follows **Clean Architecture** principles with clear separation of concerns:

```
zititex-api/
├── app/
│   ├── api/              # API Routes & Endpoints
│   │   └── v1/
│   │       └── contact.py
│   ├── core/             # Core Configuration
│   │   ├── config.py     # Settings & Environment
│   │   └── database.py   # Database Setup
│   ├── models/           # SQLAlchemy Models
│   │   └── client.py
│   ├── schemas/          # Pydantic Schemas
│   │   └── client.py
│   ├── repositories/     # Data Access Layer
│   │   └── client_repository.py
│   ├── services/         # Business Logic
│   │   └── mailgun.py
│   └── main.py           # Application Entry Point
├── tests/                # Comprehensive Test Suite
├── docker/               # Docker Configuration
├── .github/              # CI/CD Workflows
└── docs/                 # Additional Documentation
```

### Design Patterns

- **Repository Pattern**: Abstracts data access logic
- **Dependency Injection**: Loosely coupled components
- **Factory Pattern**: Application initialization
- **Strategy Pattern**: Email service abstraction

### SOLID Principles

- ✅ **Single Responsibility**: Each module has one reason to change
- ✅ **Open/Closed**: Open for extension, closed for modification
- ✅ **Liskov Substitution**: Interfaces are properly abstracted
- ✅ **Interface Segregation**: Clients don't depend on unused interfaces
- ✅ **Dependency Inversion**: Depend on abstractions, not concretions

## 🚀 Features

- **RESTful API** with FastAPI
- **MySQL Database** integration with SQLAlchemy ORM
- **Async/Await** support for better performance
- **Email Notifications** via Mailgun
- **Repository Pattern** for clean data access
- **Comprehensive Testing** with >99% coverage
- **Docker Support** for containerization
- **AWS Lambda** ready with Serverless Framework
- **Type Hints** throughout the codebase
- **API Documentation** with Swagger/OpenAPI
- **Pre-commit Hooks** for code quality

## 📋 Prerequisites

- Python 3.12+
- MySQL 8.0+
- Docker & Docker Compose (optional)
- Mailgun account (for email functionality)

## 🔧 Installation & Setup

### Option 1: Local Development (without Docker)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd zititex-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup MySQL Database**
   ```bash
   mysql -u root -p
   CREATE DATABASE zititex_db;
   CREATE USER 'zititex_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON zititex_db.* TO 'zititex_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Option 2: Docker Development

1. **Start all services**
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

2. **View logs**
   ```bash
   docker-compose -f docker-compose.dev.yml logs -f
   ```

3. **Access services**
   - API: http://localhost:8001
   - PhpMyAdmin: http://localhost:8081
   - MySQL: localhost:3307

4. **Stop services**
   ```bash
   docker-compose -f docker-compose.dev.yml down
   ```

### Option 3: Production Docker

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop
docker-compose down
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api_contact.py

# Run with verbose output
pytest -vv
```

### Test Coverage

The project maintains **>99% test coverage** including:

- ✅ Unit tests for models, schemas, and repositories
- ✅ Integration tests for API endpoints
- ✅ Service layer tests with mocking
- ✅ Database integration tests
- ✅ Error handling and edge cases

## 📚 Documentación Completa

**📍 Empieza aquí:** [document/00-LEEME-PRIMERO.md](document/00-LEEME-PRIMERO.md) ⭐ - Guía rápida de inicio

### Documentos Disponibles

| Documento | Descripción |
|-----------|-------------|
| **[00-LEEME-PRIMERO.md](document/00-LEEME-PRIMERO.md)** ⭐ | 🚀 START HERE - Guía rápida |
| **[document/README.md](document/README.md)** | 📖 Hub de documentación |
| **[INDICE.md](document/INDICE.md)** | 📍 Índice y navegación completa |
| **[REVISION_COMPLETA.md](document/REVISION_COMPLETA.md)** | 📋 Resumen ejecutivo del proyecto |
| **[ESTRUCTURA.md](document/ESTRUCTURA.md)** | 🏗️ Arquitectura y organización |
| **[API_CORREO.md](document/API_CORREO.md)** | 📧 Sistema de emails detallado |
| **[VERIFICACION_SERVERLESS.md](document/VERIFICACION_SERVERLESS.md)** ⭐ | ☁️ Serverless + Lambda + API Gateway |
| **[DESPLIEGUE.md](document/DESPLIEGUE.md)** | 🚀 Guía de deployment |
| **[PYTEST.md](document/PYTEST.md)** | 🧪 Guía de testing |
| **[run.md](document/run.md)** | 🏃 Cómo ejecutar el proyecto |
| **[prompts.md](document/prompts.md)** | 💡 Decisiones de diseño |

## 📚 API Documentation

### Endpoints

#### POST `/api/v1/contact/`

Submit a contact form with optional fields.

**Request Body:**
```json
{
  "full_name": "Juan Pérez",
  "email": "juan@example.com",
  "phone": "+52 123 456 7890",
  "company": "Example Corp",
  "product_type": "Textiles",
  "quantity": 100,
  "message": "I would like more information about your products."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Mensaje enviado exitosamente. Te responderemos pronto.",
  "data": {
    "id": 1,
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "timestamp": "2024-01-15T10:30:00"
  }
}
```

#### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Zititex API",
  "version": "0.1.0"
}
```

#### GET `/`

Root endpoint with API information.

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🗄️ Database Schema

### Client Table

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key (auto-increment) |
| full_name | VARCHAR(100) | Client's full name |
| email | VARCHAR(255) | Client's email address |
| phone | VARCHAR(20) | Client's phone number |
| company | VARCHAR(255) | Company name (optional) |
| product_type | VARCHAR(100) | Product type (optional) |
| quantity | INT | Quantity requested (optional) |
| message | TEXT | Client's message |
| created_at | DATETIME | Record creation timestamp |
| updated_at | DATETIME | Last update timestamp |

## 🔐 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `APP_NAME` | Application name | Zititex API | No |
| `DEBUG` | Debug mode | false | No |
| `MYSQL_HOST` | MySQL host | localhost | Yes |
| `MYSQL_PORT` | MySQL port | 3306 | No |
| `MYSQL_USER` | MySQL username | root | Yes |
| `MYSQL_PASSWORD` | MySQL password | - | Yes |
| `MYSQL_DATABASE` | Database name | zititex_db | Yes |
| `MAILGUN_API_KEY` | Mailgun API key | - | Yes |
| `MAILGUN_DOMAIN` | Mailgun domain | - | Yes |
| `ADMIN_EMAIL` | Admin notification email | - | Yes |

## 🚢 Deployment

### AWS Lambda (Serverless)

```bash
# Install Serverless Framework
npm install -g serverless
npm install

# Deploy to production
serverless deploy --stage prod

# Deploy to development
serverless deploy --stage dev

# View logs
serverless logs -f api --tail
```

### Docker Production

```bash
# Build image
docker build -t zititex-api:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  -e MYSQL_HOST=your-db-host \
  -e MYSQL_PASSWORD=your-password \
  --name zititex-api \
  zititex-api:latest
```

## 🛠️ Development Workflow

### Code Quality

```bash
# Format code
make format

# Run linters
make lint

# Run pre-commit hooks
make pre-commit
```

### Git Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -m "feat: your feature"`
3. Run tests: `make test`
4. Push changes: `git push origin feature/your-feature`
5. Create pull request

### Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Run tests

Install hooks:
```bash
pre-commit install
```

## 📊 Monitoring & Logging

### Health Checks

- Application: `GET /health`
- Database: Automatic connection health checks
- Docker: Built-in healthcheck configuration

### Logging

The application uses Python's standard logging:

```python
import logging
logger = logging.getLogger(__name__)
logger.info("Application started")
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

[Specify your license here]

## 👥 Team

[Add team members and contact information]

## 🔗 Related Projects

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 📚 Más Información

Para más detalles, consulta la documentación completa en la carpeta [`document/`](document/):

- **Comenzar**: [document/run.md](document/run.md)
- **Arquitectura**: [document/ESTRUCTURA.md](document/ESTRUCTURA.md)
- **Testing**: [document/PYTEST.md](document/PYTEST.md)
- **Deployment**: [document/DESPLIEGUE.md](document/DESPLIEGUE.md)
- **Decisiones de diseño**: [document/prompts.md](document/prompts.md)

## 📞 Support

For support, email [your-email] or open an issue in the repository.

