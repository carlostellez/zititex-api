# 🚀 Setup Local - Zititex API

**Guía completa para configurar y ejecutar el proyecto localmente**

---

## 📋 Prerequisitos

- ✅ Python 3.12+
- ✅ MySQL 8.0+ (o usar Docker)
- ✅ Git
- ✅ Cuenta de Mailgun (para emails)

---

## 🔧 Instalación Paso a Paso

### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/carlostellez/zititex-api.git
cd zititex-api
```

### 2️⃣ Crear Entorno Virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate  # En Mac/Linux
# venv\Scripts\activate   # En Windows
```

### 3️⃣ Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4️⃣ Configurar Base de Datos MySQL

#### Opción A: MySQL Local

```bash
# Conectar a MySQL
mysql -u root -p

# Crear base de datos y usuario
CREATE DATABASE zititex_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'zititex_user'@'localhost' IDENTIFIED BY 'tu_password_seguro';
GRANT ALL PRIVILEGES ON zititex_db.* TO 'zititex_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### Opción B: MySQL con Docker

```bash
docker run -d \
  --name mysql-zititex \
  -e MYSQL_ROOT_PASSWORD=root_password \
  -e MYSQL_DATABASE=zititex_db \
  -e MYSQL_USER=zititex_user \
  -e MYSQL_PASSWORD=user_password \
  -p 3306:3306 \
  mysql:8.0
```

### 5️⃣ Configurar Variables de Entorno

#### Crear archivo .env

```bash
# Copiar el ejemplo
cp .env.example .env

# Editar con tu editor favorito
nano .env
# o
code .env
```

#### Configurar .env

```bash
# ===========================================
# CONFIGURACIÓN BÁSICA
# ===========================================

APP_NAME=Zititex API
DEBUG=true
APP_VERSION=0.1.0

# ===========================================
# MYSQL DATABASE
# ===========================================

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=zititex_user
MYSQL_PASSWORD=tu_password_aqui
MYSQL_DATABASE=zititex_db
DATABASE_ECHO=false

# ===========================================
# MAILGUN (para envío de emails)
# ===========================================

MAILGUN_API_KEY=key-xxxxxxxxxxxxxxxxxxxxxxxxx
MAILGUN_DOMAIN=mg.tudominio.com
MAILGUN_BASE_URL=https://api.mailgun.net/v3
ADMIN_EMAIL=admin@tudominio.com

# ===========================================
# CORS (ajusta según tu frontend)
# ===========================================

ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
ALLOWED_METHODS=GET,POST,PUT,DELETE,OPTIONS
ALLOWED_HEADERS=*
```

### 6️⃣ Obtener Credenciales de Mailgun

1. **Crear cuenta en Mailgun**:
   - Ve a: https://www.mailgun.com/
   - Regístrate gratis (5,000 emails/mes)

2. **Obtener API Key**:
   - Dashboard > Settings > API Keys
   - Copia tu "Private API key"

3. **Configurar Dominio**:
   - Dashboard > Sending > Domains
   - Usa el dominio sandbox para pruebas: `sandboxxxxxxxxxx.mailgun.org`
   - O configura tu propio dominio

4. **Actualizar .env**:
   ```bash
   MAILGUN_API_KEY=key-tu-api-key-aqui
   MAILGUN_DOMAIN=sandboxxxxxxxxxx.mailgun.org
   ADMIN_EMAIL=tu-email@gmail.com
   ```

---

## ▶️ Ejecutar la Aplicación

### Iniciar el Servidor

```bash
# Asegúrate de estar en el entorno virtual
source venv/bin/activate

# Ejecutar con uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Output esperado**:
```
INFO:     Will watch for changes in these directories: ['/Users/.../zititex-api']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
🚀 Starting Zititex API...
✅ Application started successfully
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Verificar que Funciona

```bash
# Health check
curl http://localhost:8000/health

# Root endpoint
curl http://localhost:8000/

# Documentación interactiva
open http://localhost:8000/docs
```

---

## 🧪 Ejecutar Tests

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html

# Ver reporte de cobertura
open htmlcov/index.html
```

---

## 🐳 Alternativa: Docker Compose (Todo en uno)

Si prefieres no instalar MySQL localmente:

```bash
# Iniciar todo con Docker
docker-compose -f docker-compose.dev.yml up -d

# Ver logs
docker-compose -f docker-compose.dev.yml logs -f api

# Detener
docker-compose -f docker-compose.dev.yml down
```

**Servicios incluidos**:
- API: http://localhost:8001
- MySQL: localhost:3307
- PhpMyAdmin: http://localhost:8081

---

## 📝 Endpoints Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Root - Info de la API |
| `/health` | GET | Health check |
| `/docs` | GET | Documentación Swagger UI |
| `/redoc` | GET | Documentación ReDoc |
| `/api/v1/contact/` | POST | Enviar formulario de contacto |

---

## 🔍 Probar el API Manualmente

### Usando cURL

```bash
# Enviar formulario de contacto
curl -X POST http://localhost:8000/api/v1/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Juan Pérez",
    "email": "juan@example.com",
    "phone": "+52 123 456 7890",
    "company": "Test Company",
    "product_type": "Textiles",
    "quantity": 100,
    "message": "Estoy interesado en sus productos"
  }'
```

### Usando Swagger UI

1. Abre: http://localhost:8000/docs
2. Expande el endpoint `/api/v1/contact/`
3. Click en "Try it out"
4. Edita el JSON con tus datos
5. Click en "Execute"

### Usando Postman

1. Importar colección (crear archivo `postman_collection.json`)
2. O configurar manualmente:
   - Method: POST
   - URL: http://localhost:8000/api/v1/contact/
   - Headers: Content-Type: application/json
   - Body (raw JSON):
   ```json
   {
     "full_name": "Test User",
     "email": "test@example.com",
     "phone": "1234567890",
     "message": "Test message"
   }
   ```

---

## 🗄️ Gestionar Base de Datos

### Conectar a MySQL

```bash
# MySQL local
mysql -u zititex_user -p zititex_db

# MySQL en Docker
docker exec -it mysql-zititex mysql -u zititex_user -p zititex_db
```

### Comandos Útiles

```sql
-- Ver tablas
SHOW TABLES;

-- Ver estructura de tabla client
DESCRIBE client;

-- Ver registros recientes
SELECT * FROM client ORDER BY created_at DESC LIMIT 10;

-- Contar registros
SELECT COUNT(*) FROM client;

-- Limpiar tabla (testing)
TRUNCATE TABLE client;
```

### Crear Tablas Manualmente

Las tablas se crean automáticamente al iniciar la app en modo DEBUG, pero también puedes:

```python
# Ejecutar en Python
from app.core.database import create_tables
import asyncio

async def setup_db():
    await create_tables()

asyncio.run(setup_db())
```

---

## 🔧 Troubleshooting

### Problema: "ModuleNotFoundError"

```bash
# Asegúrate de estar en el entorno virtual
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### Problema: "Can't connect to MySQL server"

```bash
# Verificar que MySQL está corriendo
# Mac:
brew services list

# Linux:
sudo systemctl status mysql

# Docker:
docker ps | grep mysql

# Verificar credenciales en .env
cat .env | grep MYSQL
```

### Problema: "Mailgun API error"

```bash
# Verificar API key
curl -v --user 'api:YOUR_API_KEY' \
  https://api.mailgun.net/v3/YOUR_DOMAIN/messages \
  -F from='sender@example.com' \
  -F to='recipient@example.com' \
  -F subject='Test' \
  -F text='Testing'
```

### Problema: "Port 8000 already in use"

```bash
# Matar proceso en puerto 8000
# Mac/Linux:
lsof -ti:8000 | xargs kill -9

# O usar otro puerto
uvicorn app.main:app --reload --port 8001
```

---

## 📚 Siguientes Pasos

1. ✅ **Leer documentación**:
   - [document/00-LEEME-PRIMERO.md](./00-LEEME-PRIMERO.md)
   - [document/ESTRUCTURA.md](./ESTRUCTURA.md)
   - [document/API_CORREO.md](./API_CORREO.md)

2. ✅ **Explorar el código**:
   ```bash
   tree app/  # Ver estructura
   ```

3. ✅ **Hacer cambios**:
   - El servidor se recarga automáticamente (--reload)
   - Los cambios se reflejan inmediatamente

4. ✅ **Ejecutar tests**:
   ```bash
   pytest -v
   ```

---

## 🆘 Ayuda Adicional

- **Documentación**: [document/INDICE.md](./INDICE.md)
- **GitHub Issues**: https://github.com/carlostellez/zititex-api/issues
- **Mailgun Docs**: https://documentation.mailgun.com/
- **FastAPI Docs**: https://fastapi.tiangolo.com/

---

**Última actualización**: 20 de Octubre, 2024  
**Versión**: 1.0.0

