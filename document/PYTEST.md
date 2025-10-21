# 🧪 Guía Completa de Testing con Pytest

## Estadísticas del Proyecto

```
📊 Cobertura de Tests
├── Total de tests: 85+ funciones
├── Líneas de código de tests: 1,460+
├── Cobertura objetivo: >99%
├── Archivos de test: 7
└── Fixtures compartidos: 10+
```

## Estructura de Tests

```
tests/
├── __init__.py
├── conftest.py              # ⭐ Fixtures y configuración compartida
├── test_models.py           # Tests de modelos SQLAlchemy
├── test_schemas.py          # Tests de validación Pydantic
├── test_repositories.py     # Tests de capa de datos
├── test_services.py         # Tests de servicios (Mailgun)
├── test_api_contact.py      # Tests de endpoints HTTP
├── test_config.py           # Tests de configuración
└── test_main.py             # Tests de aplicación FastAPI
```

## Configuración Pytest

### pytest.ini

```ini
[pytest]
# Descubrimiento de tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Opciones por defecto
addopts =
    -v                        # Verbose
    --strict-markers          # Markers estrictos
    --tb=short                # Traceback corto
    --cov=app                 # Cobertura del directorio app
    --cov-report=term-missing # Mostrar líneas sin cubrir
    --cov-report=html         # Reporte HTML
    --cov-fail-under=99       # ⚠️ Fallar si <99% cobertura
    --asyncio-mode=auto       # Modo async automático

# Markers disponibles
markers =
    unit: Tests unitarios
    integration: Tests de integración
    asyncio: Tests asíncronos
    slow: Tests lentos
```

## Tipos de Tests

### 1️⃣ Tests Unitarios

**Qué testean**: Componentes individuales aislados

**Ejemplo: test_models.py**
```python
async def test_create_client_with_all_fields(
    async_test_db: AsyncSession, 
    sample_client_data: dict
):
    """Test creating a client with all fields."""
    client = Client(**sample_client_data)
    async_test_db.add(client)
    await async_test_db.commit()
    await async_test_db.refresh(client)

    assert client.id is not None
    assert client.full_name == sample_client_data["full_name"]
    assert client.email == sample_client_data["email"]
    assert isinstance(client.created_at, datetime)
```

**Ejecutar:**
```bash
pytest tests/test_models.py -v
```

### 2️⃣ Tests de Validación

**Qué testean**: Schemas Pydantic y validación de datos

**Ejemplo: test_schemas.py**
```python
def test_invalid_email():
    """Test that invalid email raises validation error."""
    data = {
        "full_name": "Test User",
        "email": "invalid-email",  # ❌ Email inválido
        "phone": "1234567890",
        "message": "Test message",
    }

    with pytest.raises(ValidationError) as exc_info:
        ContactForm(**data)

    assert "email" in str(exc_info.value).lower()
```

**Ejecutar:**
```bash
pytest tests/test_schemas.py -v
```

### 3️⃣ Tests de Repositorio

**Qué testean**: Acceso a datos y operaciones CRUD

**Ejemplo: test_repositories.py**
```python
async def test_create_async(
    async_test_db: AsyncSession, 
    sample_client_data: dict
):
    """Test creating a client asynchronously."""
    repo = ClientRepository(async_test_db)
    client_create = ClientCreate(**sample_client_data)

    client = await repo.create_async(client_create)

    assert client.id is not None
    assert client.full_name == sample_client_data["full_name"]
```

**Ejecutar:**
```bash
pytest tests/test_repositories.py -v
```

### 4️⃣ Tests de Servicios

**Qué testean**: Lógica de negocio y servicios externos

**Ejemplo: test_services.py**
```python
@patch("app.services.mailgun.requests.post")
def test_send_email_success(mock_post, mailgun_service):
    """Test successful email sending."""
    # Mock la respuesta de Mailgun
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "test-message-id"}
    mock_post.return_value = mock_response

    # Ejecutar
    result = mailgun_service.send_email(
        to_emails=["test@example.com"],
        subject="Test Subject",
        text="Test message",
    )

    # Verificar
    assert result is not None
    assert result["id"] == "test-message-id"
    mock_post.assert_called_once()
```

**Ejecutar:**
```bash
pytest tests/test_services.py -v
```

### 5️⃣ Tests de API (Integration)

**Qué testean**: Endpoints HTTP completos

**Ejemplo: test_api_contact.py**
```python
async def test_submit_contact_form_success(
    async_client: AsyncClient,
    async_test_db: AsyncSession,
    mock_mailgun_service,
    mock_settings_with_email,
    sample_client_data: dict,
):
    """Test successful contact form submission."""
    response = await async_client.post(
        "/api/v1/contact/", 
        json=sample_client_data
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    
    # Verificar que se guardó en BD
    repo = ClientRepository(async_test_db)
    clients = await repo.get_all_async()
    assert len(clients) == 1
```

**Ejecutar:**
```bash
pytest tests/test_api_contact.py -v
```

## Fixtures Importantes

### Ubicación: `tests/conftest.py`

### 1. Base de Datos Test

```python
@pytest.fixture
async def async_test_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Base de datos SQLite en memoria para tests.
    Se crea nueva para cada test y se limpia después.
    """
    async with AsyncTestingSessionLocal() as session:
        yield session
```

**Uso:**
```python
async def test_something(async_test_db: AsyncSession):
    # async_test_db ya está configurado y listo
    repo = ClientRepository(async_test_db)
```

### 2. Cliente HTTP Test

```python
@pytest.fixture
async def async_client(async_test_db: AsyncSession):
    """
    Cliente HTTP async para hacer requests a la API.
    Tiene la BD inyectada automáticamente.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
```

**Uso:**
```python
async def test_endpoint(async_client: AsyncClient):
    response = await async_client.post("/api/v1/contact/", json={...})
    assert response.status_code == 200
```

### 3. Mock de Mailgun

```python
@pytest.fixture
def mock_mailgun_service(monkeypatch):
    """
    Mock del servicio de Mailgun para no enviar emails reales.
    """
    mock_service = MagicMock()
    mock_service.send_contact_form_email.return_value = True
    
    from app.services import mailgun
    monkeypatch.setattr(mailgun, "mailgun_service", mock_service)
    return mock_service
```

**Uso:**
```python
def test_email(mock_mailgun_service):
    # Los emails no se envían realmente
    # pero podemos verificar que se llamó al servicio
    mock_mailgun_service.send_contact_form_email.assert_called_once()
```

### 4. Datos de Prueba

```python
@pytest.fixture
def sample_client_data() -> dict:
    """Datos de ejemplo para tests."""
    return {
        "full_name": "Juan Pérez",
        "email": "juan.perez@example.com",
        "phone": "+52 123 456 7890",
        "company": "Test Company",
        "product_type": "Textiles",
        "quantity": 100,
        "message": "Test message",
    }
```

**Uso:**
```python
def test_something(sample_client_data: dict):
    # sample_client_data ya tiene datos válidos
    form = ContactForm(**sample_client_data)
```

## Comandos de Pytest

### Básicos

```bash
# Ejecutar todos los tests
pytest

# Verbose (más información)
pytest -v

# Muy verbose (aún más info)
pytest -vv

# Mostrar prints
pytest -s

# Ejecutar archivo específico
pytest tests/test_api_contact.py

# Ejecutar test específico
pytest tests/test_api_contact.py::TestContactAPI::test_submit_contact_form_success

# Ejecutar por clase
pytest tests/test_api_contact.py::TestContactAPI

# Ejecutar por patrón
pytest -k "test_create"
```

### Con Cobertura

```bash
# Reporte básico
pytest --cov=app

# Con líneas faltantes
pytest --cov=app --cov-report=term-missing

# Generar HTML
pytest --cov=app --cov-report=html

# Ver reporte HTML
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Por Markers

```bash
# Solo tests unitarios
pytest -m unit

# Solo tests de integración
pytest -m integration

# Solo tests async
pytest -m asyncio

# Excluir tests lentos
pytest -m "not slow"

# Combinar markers
pytest -m "unit and not slow"
```

### Modos Especiales

```bash
# Detener en primer fallo
pytest -x

# Detener después de N fallos
pytest --maxfail=3

# Ejecutar último test que falló
pytest --lf

# Ejecutar tests que fallaron y luego todos
pytest --ff

# Tests en paralelo (requiere pytest-xdist)
pytest -n auto

# Modo quiet (menos output)
pytest -q

# Solo mostrar resumen
pytest --tb=no
```

## Cobertura de Código

### Objetivo: >99%

```bash
# Ver cobertura actual
pytest --cov=app --cov-report=term

# Salida esperada:
----------- coverage: platform darwin, python 3.12.0 -----------
Name                                    Stmts   Miss  Cover   Missing
---------------------------------------------------------------------
app/__init__.py                             3      0   100%
app/api/__init__.py                         1      0   100%
app/api/v1/__init__.py                      1      0   100%
app/api/v1/contact.py                      45      0   100%
app/core/__init__.py                        6      0   100%
app/core/config.py                         28      0   100%
app/core/database.py                       42      0   100%
app/models/__init__.py                      2      0   100%
app/models/client.py                       25      0   100%
app/repositories/__init__.py                2      0   100%
app/repositories/client_repository.py     110      0   100%
app/schemas/__init__.py                     6      0   100%
app/schemas/client.py                      65      0   100%
app/services/__init__.py                    3      0   100%
app/services/mailgun.py                    89      0   100%
app/main.py                                38      0   100%
---------------------------------------------------------------------
TOTAL                                     466      0   100%
```

### Reporte HTML Detallado

```bash
# Generar reporte
pytest --cov=app --cov-report=html

# Abrir en navegador
open htmlcov/index.html
```

**El reporte HTML muestra:**
- ✅ Líneas cubiertas (verde)
- ❌ Líneas no cubiertas (rojo)
- ⚠️ Líneas parcialmente cubiertas (amarillo)
- Estadísticas por archivo
- Navegación interactiva

## Estrategia de Testing

### Pirámide de Tests

```
           /\
          /  \
         / E2E\       ← 10% (pocos, lentos, frágiles)
        /______\
       /        \
      /Integration\  ← 30% (algunos, medios)
     /____________\
    /              \
   /  Unit Tests    \ ← 60% (muchos, rápidos, confiables)
  /__________________\
```

### Qué Testear

#### ✅ Siempre Testear

- Lógica de negocio
- Validaciones de datos
- Casos edge
- Manejo de errores
- Operaciones de BD
- Integración con servicios externos (mock)

#### ❌ No Testear

- Frameworks (FastAPI ya está testeado)
- Librerías externas (SQLAlchemy ya está testeado)
- Configuración simple
- Getters/setters triviales

## Mocking

### ¿Cuándo Mockear?

✅ **Siempre mockear:**
- Servicios externos (Mailgun, AWS, etc.)
- Base de datos en algunos tests (usar SQLite para otros)
- Tiempo/fechas (para tests determinísticos)
- Llamadas HTTP externas

### Ejemplo de Mocking

```python
from unittest.mock import MagicMock, patch

# Mock de función
@patch("app.services.mailgun.requests.post")
def test_email(mock_post):
    mock_post.return_value.json.return_value = {"id": "123"}
    # test code...

# Mock de clase
@patch("app.services.mailgun.MailgunService")
def test_service(MockMailgunService):
    mock_instance = MockMailgunService.return_value
    mock_instance.send_email.return_value = True
    # test code...

# Mock con monkeypatch (fixture de pytest)
def test_setting(monkeypatch):
    monkeypatch.setattr(settings, "debug", True)
    # test code...
```

## Tests Async

### Decorador Automático

```python
# pytest.ini tiene asyncio_mode = auto
# No necesitas decorador @pytest.mark.asyncio

async def test_async_operation(async_test_db):
    # Funciona automáticamente
    result = await some_async_function()
    assert result is not None
```

### Fixtures Async

```python
@pytest.fixture
async def async_fixture():
    # Setup
    resource = await create_resource()
    yield resource
    # Teardown
    await cleanup_resource(resource)
```

## Debugging Tests

### Usando pdb

```bash
# Modo debug interactivo
pytest --pdb

# Debug en primer fallo
pytest -x --pdb

# En el código:
import pdb; pdb.set_trace()
```

### Usando VS Code

`.vscode/launch.json`:
```json
{
    "configurations": [
        {
            "name": "Python: Pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": [
                "tests/test_api_contact.py",
                "-v",
                "-s"
            ],
            "console": "integratedTerminal",
            "justMyCode": false
        }
    ]
}
```

## CI/CD Integration

### GitHub Actions

`.github/workflows/tests.yml`:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## Mejores Prácticas

### ✅ DO

```python
# Tests descriptivos
def test_user_can_submit_valid_contact_form():
    """Clear description of what is being tested."""
    # Arrange
    data = {...}
    
    # Act
    response = submit_form(data)
    
    # Assert
    assert response.success is True
```

### ❌ DON'T

```python
# Test poco claro
def test_1():
    data = {...}
    response = submit_form(data)
    assert response.success
```

### Patrón AAA (Arrange-Act-Assert)

```python
async def test_example():
    # Arrange - Preparar datos
    client_data = {"name": "Test"}
    repo = ClientRepository(db)
    
    # Act - Ejecutar acción
    client = await repo.create_async(client_data)
    
    # Assert - Verificar resultado
    assert client.id is not None
    assert client.name == "Test"
```

## Troubleshooting

### Error: Import Errors

```bash
# Problema: ModuleNotFoundError

# Solución: Asegurar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

### Error: Database Locked

```bash
# Problema: sqlite3.OperationalError: database is locked

# Solución: Limpiar archivos test
rm test.db
pytest
```

### Error: Async Warnings

```bash
# Problema: warnings about coroutines

# Solución: Verificar pytest-asyncio instalado
pip install pytest-asyncio

# Y que pytest.ini tenga:
# asyncio_mode = auto
```

## Comandos Útiles

```bash
# Ejecutar tests y generar todos los reportes
make test

# Tests en Docker
docker exec -it zititex-api-dev pytest

# Tests con logs completos
pytest -vv -s --log-cli-level=DEBUG

# Tests rápidos (sin coverage)
pytest --no-cov

# Tests en watch mode (requiere pytest-watch)
ptw

# Limpiar archivos de test
rm -rf .pytest_cache htmlcov .coverage test.db
```

## Resumen de Cobertura por Módulo

| Módulo | Tests | Cobertura |
|--------|-------|-----------|
| **Models** | 12 | 100% |
| **Schemas** | 15 | 100% |
| **Repositories** | 20 | 100% |
| **Services** | 18 | 100% |
| **API Endpoints** | 15 | 100% |
| **Config** | 8 | 100% |
| **Main** | 8 | 100% |
| **TOTAL** | **85+** | **>99%** |

---

**Para más información:**
- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

