# 📁 Estructura del Proyecto Zititex API

## Visión General

```
zititex-api/
│
├── 📂 app/                          # Código fuente de la aplicación
│   ├── __init__.py
│   ├── main.py                      # ✅ Punto de entrada FastAPI
│   │
│   ├── 📂 api/                      # Endpoints de la API
│   │   ├── __init__.py
│   │   └── 📂 v1/                   # API versión 1
│   │       ├── __init__.py
│   │       └── contact.py           # ✅ Endpoint de formulario de contacto
│   │
│   ├── 📂 core/                     # Configuración y núcleo
│   │   ├── __init__.py
│   │   ├── config.py                # ✅ Configuración y Settings
│   │   └── database.py              # ✅ Configuración de base de datos
│   │
│   ├── 📂 models/                   # Modelos SQLAlchemy (ORM)
│   │   ├── __init__.py
│   │   └── client.py                # ✅ Modelo de tabla 'client'
│   │
│   ├── 📂 schemas/                  # Esquemas Pydantic (validación)
│   │   ├── __init__.py
│   │   └── client.py                # ✅ Schemas de request/response
│   │
│   ├── 📂 repositories/             # Patrón Repository (acceso a datos)
│   │   ├── __init__.py
│   │   └── client_repository.py    # ✅ CRUD operations para Client
│   │
│   └── 📂 services/                 # Lógica de negocio
│       ├── __init__.py
│       └── mailgun.py               # ✅ Servicio de email Mailgun
│
├── 📂 tests/                        # Suite de pruebas (>99% coverage)
│   ├── __init__.py
│   ├── conftest.py                  # ✅ Fixtures y configuración pytest
│   ├── test_api_contact.py          # ✅ Tests del endpoint contact
│   ├── test_config.py               # ✅ Tests de configuración
│   ├── test_main.py                 # ✅ Tests de aplicación principal
│   ├── test_models.py               # ✅ Tests de modelos
│   ├── test_repositories.py         # ✅ Tests de repositorios
│   ├── test_schemas.py              # ✅ Tests de schemas
│   └── test_services.py             # ✅ Tests de servicios
│
├── 📂 docker/                       # Configuración Docker
│   └── 📂 mysql/
│       └── 📂 init/
│           └── 01-create-tables.sql # ✅ Script inicial de BD
│
├── 📂 .github/                      # CI/CD workflows
│   └── workflows/
│       └── ci.yml                   # Pipeline de integración continua
│
├── 📄 Dockerfile                    # ✅ Docker imagen producción
├── 📄 Dockerfile.dev                # ✅ Docker imagen desarrollo
├── 📄 docker-compose.yml            # ✅ Orquestación producción
├── 📄 docker-compose.dev.yml        # ✅ Orquestación desarrollo
├── 📄 requirements.txt              # ✅ Dependencias Python
├── 📄 pytest.ini                    # ✅ Configuración pytest
├── 📄 serverless.yml                # ✅ Configuración AWS Lambda
├── 📄 Makefile                      # ✅ Comandos útiles
├── 📄 .dockerignore                 # ✅ Exclusiones Docker
├── 📄 .env.example                  # ✅ Template variables entorno
├── 📄 .env.local                    # ✅ Configuración local
├── 📄 .pre-commit-config.yaml       # ✅ Hooks pre-commit
├── 📄 README.md                     # ✅ Documentación principal
├── 📄 run.md                        # ✅ Guía de ejecución
└── 📄 prompts.md                    # ✅ Decisiones de diseño
```

## Arquitectura en Capas

### 🎯 Capa 1: API (Routes)
**Responsabilidad**: Manejar HTTP requests/responses

```
app/api/v1/contact.py
│
├── Recibe HTTP Request
├── Valida datos con Pydantic
├── Llama a Repository
└── Retorna HTTP Response
```

### 🔧 Capa 2: Servicios (Business Logic)
**Responsabilidad**: Lógica de negocio y orquestación

```
app/services/mailgun.py
│
├── Envía emails
├── Gestiona templates
└── Maneja errores de email
```

### 📦 Capa 3: Repositorios (Data Access)
**Responsabilidad**: Acceso y manipulación de datos

```
app/repositories/client_repository.py
│
├── Create (insert)
├── Read (select)
├── Update (update)
├── Delete (delete)
└── Custom queries
```

### 🗄️ Capa 4: Modelos (Database)
**Responsabilidad**: Definición de estructura de datos

```
app/models/client.py
│
├── Define tabla 'client'
├── Campos y tipos
├── Relaciones
└── Índices
```

## Flujo de Datos

```
1. Usuario POST /api/v1/contact/
              ↓
2. contact.py (API Layer)
   - Valida con ContactForm schema
              ↓
3. ClientRepository (Data Layer)
   - Guarda en MySQL
              ↓
4. MailgunService (Service Layer)
   - Envía email a admin
   - Envía email a usuario
              ↓
5. Return ContactResponse
   - success: true
   - data: {id, name, email, timestamp}
```

## Patrones de Diseño Implementados

### 1. Repository Pattern
```python
# Abstrae acceso a datos
repo = ClientRepository(db)
client = await repo.create_async(data)
```

### 2. Dependency Injection
```python
# FastAPI inyecta dependencias
async def endpoint(db: AsyncSession = Depends(get_async_db)):
    pass
```

### 3. Factory Pattern
```python
# Crea instancias de aplicación
app = create_app()
```

### 4. Strategy Pattern
```python
# Múltiples estrategias de email
mailgun_service.send_email(...)
```

## Principios SOLID

✅ **S**ingle Responsibility - Cada módulo una responsabilidad
✅ **O**pen/Closed - Abierto a extensión, cerrado a modificación
✅ **L**iskov Substitution - Interfaces sustituibles
✅ **I**nterface Segregation - Interfaces específicas
✅ **D**ependency Inversion - Depende de abstracciones

## Archivos Clave

| Archivo | Propósito | Importancia |
|---------|-----------|-------------|
| `app/main.py` | Entry point de FastAPI | ⭐⭐⭐⭐⭐ |
| `app/api/v1/contact.py` | Endpoint de contacto | ⭐⭐⭐⭐⭐ |
| `app/core/database.py` | Configuración MySQL | ⭐⭐⭐⭐⭐ |
| `app/models/client.py` | Modelo de datos | ⭐⭐⭐⭐⭐ |
| `app/repositories/client_repository.py` | CRUD operations | ⭐⭐⭐⭐⭐ |
| `docker-compose.yml` | Orquestación containers | ⭐⭐⭐⭐ |
| `requirements.txt` | Dependencias | ⭐⭐⭐⭐ |
| `pytest.ini` | Config tests | ⭐⭐⭐⭐ |

## Tecnologías Utilizadas

### Backend
- **FastAPI** 0.104.1 - Framework web moderno
- **SQLAlchemy** 2.0.23 - ORM para MySQL
- **Pydantic** - Validación de datos
- **Uvicorn** - ASGI server

### Database
- **MySQL** 8.0 - Base de datos relacional
- **aiomysql** 0.2.0 - Driver async MySQL
- **pymysql** 1.1.0 - Driver sync MySQL

### Testing
- **pytest** 7.4.3 - Framework de testing
- **pytest-asyncio** 0.21.1 - Tests async
- **pytest-cov** 4.1.0 - Cobertura de código
- **httpx** 0.25.2 - Cliente HTTP async

### DevOps
- **Docker** - Containerización
- **Docker Compose** - Orquestación
- **AWS Lambda/Serverless** - Deployment serverless

### Email
- **Mailgun** - Servicio de email transaccional
- **requests** 2.31.0 - Cliente HTTP

## Variables de Entorno

```bash
# Aplicación
APP_NAME=Zititex API
DEBUG=true/false

# Base de datos
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=usuario
MYSQL_PASSWORD=contraseña
MYSQL_DATABASE=zititex_db

# Email
MAILGUN_API_KEY=tu-api-key
MAILGUN_DOMAIN=tu-dominio.com
ADMIN_EMAIL=admin@dominio.com

# CORS
ALLOWED_ORIGINS=*
```

## Siguientes Pasos

Para trabajar con el proyecto:

1. **Setup inicial**: `make install`
2. **Desarrollo local**: `make dev`
3. **Ejecutar tests**: `make test`
4. **Docker development**: `make docker-up-dev`
5. **Formatear código**: `make format`
6. **Linting**: `make lint`

## Documentación Adicional

- 📖 [README.md](README.md) - Documentación completa
- 🏃 [run.md](run.md) - Guía de ejecución detallada
- 💡 [prompts.md](prompts.md) - Decisiones de diseño

