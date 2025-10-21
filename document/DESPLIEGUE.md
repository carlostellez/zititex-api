# 🚀 Guía Completa de Despliegue

## Opciones de Despliegue

Este proyecto soporta 3 formas de despliegue:

1. **🔧 Local (Desarrollo)** - Sin Docker
2. **🐳 Docker (Desarrollo)** - Con hot-reload
3. **☁️ Producción** - Docker Compose o AWS Lambda

---

## 1️⃣ Despliegue Local (Sin Docker)

### Requisitos Previos

```bash
# Python 3.12+
python --version

# MySQL 8.0+
mysql --version

# pip actualizado
pip --version
```

### Paso a Paso

#### 1. Clonar y Preparar Entorno

```bash
# Clonar repositorio
git clone <repo-url>
cd zititex-api

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

#### 2. Configurar MySQL

```bash
# Conectar a MySQL
mysql -u root -p

# Ejecutar SQL
CREATE DATABASE zititex_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'zititex_user'@'localhost' IDENTIFIED BY 'tu_password_seguro';
GRANT ALL PRIVILEGES ON zititex_db.* TO 'zititex_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 3. Configurar Variables de Entorno

```bash
# Copiar ejemplo
cp .env.example .env

# Editar .env
nano .env
```

**.env mínimo requerido:**
```bash
# Aplicación
APP_NAME=Zititex API
DEBUG=true

# Base de Datos
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=zititex_user
MYSQL_PASSWORD=tu_password_seguro
MYSQL_DATABASE=zititex_db

# Mailgun (obtener de https://app.mailgun.com/)
MAILGUN_API_KEY=key-tu_mailgun_api_key
MAILGUN_DOMAIN=mg.tudominio.com
ADMIN_EMAIL=admin@tudominio.com
```

#### 4. Ejecutar Aplicación

```bash
# Opción 1: Uvicorn directamente
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Opción 2: Usando Makefile
make dev

# Opción 3: Python módulo
python -m uvicorn app.main:app --reload
```

#### 5. Verificar

```bash
# Health check
curl http://localhost:8000/health

# Swagger docs
open http://localhost:8000/docs  # macOS
xdg-open http://localhost:8000/docs  # Linux
```

**Salida esperada:**
```json
{
  "status": "healthy",
  "service": "Zititex API",
  "version": "0.1.0"
}
```

---

## 2️⃣ Despliegue Docker Desarrollo

### Ventajas

✅ Entorno idéntico para todos los desarrolladores
✅ MySQL incluido (no requiere instalación local)
✅ PhpMyAdmin para gestionar BD
✅ Hot-reload automático
✅ Un solo comando para iniciar todo

### Arquitectura Docker Dev

```
┌─────────────────────────────────────────────┐
│  Host Machine (tu computadora)              │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │  Docker Network: zititex-dev-network │  │
│  │                                       │  │
│  │  ┌─────────────────────────────────┐ │  │
│  │  │  Container: zititex-api-dev     │ │  │
│  │  │  - Python 3.12                  │ │  │
│  │  │  - FastAPI con hot-reload       │ │  │
│  │  │  - Port: 8001 → 8000            │ │  │
│  │  │  - Volumes: código sincronizado │ │  │
│  │  └─────────────────────────────────┘ │  │
│  │             ↕                         │  │
│  │  ┌─────────────────────────────────┐ │  │
│  │  │  Container: zititex-mysql-dev   │ │  │
│  │  │  - MySQL 8.0                    │ │  │
│  │  │  - Port: 3307 → 3306            │ │  │
│  │  │  - Volume: mysql_dev_data       │ │  │
│  │  └─────────────────────────────────┘ │  │
│  │             ↕                         │  │
│  │  ┌─────────────────────────────────┐ │  │
│  │  │  Container: zititex-phpmyadmin  │ │  │
│  │  │  - PhpMyAdmin latest            │ │  │
│  │  │  - Port: 8081 → 80              │ │  │
│  │  └─────────────────────────────────┘ │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### Paso a Paso

#### 1. Instalar Docker

```bash
# Verificar instalación
docker --version
docker-compose --version

# Asegurar que Docker está corriendo
docker ps
```

#### 2. Configurar Variables

```bash
# Crear .env para Docker
cp .env.example .env

# Editar con credenciales
nano .env
```

**.env para Docker:**
```bash
# MySQL (Docker creará automáticamente)
MYSQL_ROOT_PASSWORD=rootpass_dev
MYSQL_USER=dev_user
MYSQL_PASSWORD=dev_pass
MYSQL_DATABASE=zititex_db
MYSQL_PORT=3307  # Puerto en host (evita conflicto con MySQL local)

# Mailgun
MAILGUN_API_KEY=key-tu_api_key
MAILGUN_DOMAIN=mg.tudominio.com
ADMIN_EMAIL=admin@tudominio.com

# Puertos
API_PORT=8001
PHPMYADMIN_PORT=8081
```

#### 3. Construir y Ejecutar

```bash
# Opción 1: Usar Makefile
make docker-up-dev

# Opción 2: Docker Compose directamente
docker-compose -f docker-compose.dev.yml up -d

# Ver logs en tiempo real
docker-compose -f docker-compose.dev.yml logs -f

# Ver solo logs de API
docker-compose -f docker-compose.dev.yml logs -f api
```

#### 4. Acceder a Servicios

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| **API** | http://localhost:8001 | - |
| **API Docs** | http://localhost:8001/docs | - |
| **PhpMyAdmin** | http://localhost:8081 | User: root<br>Pass: rootpass_dev |
| **MySQL** | localhost:3307 | User: dev_user<br>Pass: dev_pass |

#### 5. Comandos Útiles

```bash
# Ver estado de contenedores
docker-compose -f docker-compose.dev.yml ps

# Reiniciar servicios
docker-compose -f docker-compose.dev.yml restart

# Reiniciar solo API
docker-compose -f docker-compose.dev.yml restart api

# Detener servicios
docker-compose -f docker-compose.dev.yml down

# Detener y eliminar volúmenes (limpieza completa)
docker-compose -f docker-compose.dev.yml down -v

# Entrar al contenedor de API
docker exec -it zititex-api-dev bash

# Entrar a MySQL
docker exec -it zititex-mysql-dev mysql -u root -p

# Ver logs históricos
docker-compose -f docker-compose.dev.yml logs --tail=100
```

#### 6. Hot-Reload

El hot-reload está activado automáticamente:

```bash
# Edita cualquier archivo .py en app/
# Los cambios se reflejan automáticamente
# Verifica en los logs:
docker-compose -f docker-compose.dev.yml logs -f api

# Deberías ver:
# INFO:     Detected file change in 'app/api/v1/contact.py'
# INFO:     Reloading...
```

#### 7. Ejecutar Tests en Docker

```bash
# Método 1: Desde contenedor
docker exec -it zititex-api-dev pytest

# Método 2: Con coverage
docker exec -it zititex-api-dev pytest --cov=app --cov-report=html

# Método 3: Tests específicos
docker exec -it zititex-api-dev pytest tests/test_api_contact.py -v
```

---

## 3️⃣ Despliegue Producción - Docker

### Diferencias con Desarrollo

| Aspecto | Desarrollo | Producción |
|---------|-----------|------------|
| Hot-reload | ✅ Sí | ❌ No |
| Debug | ✅ true | ❌ false |
| Docs | ✅ /docs | ❌ Deshabilitado |
| Logs | ✅ Verbose | ⚠️ Mínimos |
| Usuario | root | appuser (non-root) |
| Healthcheck | ✅ Sí | ✅ Sí |
| Volumes | Código sincronizado | Solo datos |

### Paso a Paso

#### 1. Configurar .env Producción

```bash
# Crear .env para producción
cp .env.example .env.prod

# Editar con valores de producción
nano .env.prod
```

**.env.prod:**
```bash
# Aplicación
APP_NAME=Zititex API
APP_VERSION=1.0.0
DEBUG=false

# Base de Datos (usar servidor MySQL real, no Docker para prod)
MYSQL_HOST=tu-servidor-mysql.com
MYSQL_PORT=3306
MYSQL_USER=zititex_prod
MYSQL_PASSWORD=password_muy_seguro_aqui
MYSQL_DATABASE=zititex_prod_db

# Mailgun
MAILGUN_API_KEY=key-produccion_api_key
MAILGUN_DOMAIN=mg.tudominio.com
ADMIN_EMAIL=admin@tudominio.com

# CORS (solo dominios permitidos)
ALLOWED_ORIGINS=https://tudominio.com,https://www.tudominio.com

# Puertos
API_PORT=8000
```

#### 2. Construir Imagen

```bash
# Opción 1: Con Makefile
make docker-build

# Opción 2: Docker Compose
docker-compose build

# Opción 3: Docker directamente
docker build -t zititex-api:latest -f Dockerfile .
```

#### 3. Ejecutar en Producción

```bash
# Con docker-compose
docker-compose --env-file .env.prod up -d

# Ver logs
docker-compose logs -f

# Verificar salud
curl http://localhost:8000/health
```

#### 4. Configurar Reverse Proxy (Nginx)

**nginx.conf:**
```nginx
server {
    listen 80;
    server_name api.tudominio.com;

    # Redirigir a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.tudominio.com;

    # Certificados SSL
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # Proxy a FastAPI
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Logs
    access_log /var/log/nginx/zititex-api-access.log;
    error_log /var/log/nginx/zititex-api-error.log;
}
```

#### 5. Monitoreo y Logs

```bash
# Ver logs en tiempo real
docker-compose logs -f api

# Ver últimas 100 líneas
docker-compose logs --tail=100 api

# Exportar logs
docker-compose logs api > logs_$(date +%Y%m%d).txt

# Estadísticas de contenedor
docker stats zititex-api

# Health check manual
curl http://localhost:8000/health
```

---

## 4️⃣ Despliegue AWS Lambda (Serverless)

### Ventajas

✅ Auto-scaling automático
✅ Pay-per-use (solo pagas por requests)
✅ No gestión de servidores
✅ Alta disponibilidad
✅ Integración con AWS

### Arquitectura Serverless

```
Internet
   ↓
API Gateway (AWS)
   ↓
Lambda Function (Python 3.12)
   ↓
┌─────────────────────────────┐
│ FastAPI + Mangum Handler   │
│ - app.main:handler          │
│ - Dependencies empaquetadas │
└─────────────────────────────┘
   ↓
RDS MySQL (AWS)
   ↓
External Services (Mailgun)
```

### Requisitos

```bash
# Node.js y npm
node --version  # v14+
npm --version

# Serverless Framework
npm install -g serverless

# AWS CLI
aws --version

# Configurar AWS
aws configure
# AWS Access Key ID: [tu-access-key]
# AWS Secret Access Key: [tu-secret-key]
# Default region: us-east-2
# Default output format: json
```

### Configuración

**serverless.yml** ya está configurado:

```yaml
service: zititex-api

provider:
  name: aws
  runtime: python3.12
  region: us-east-2
  
functions:
  api:
    handler: app.main.handler
    events:
      - http:
          path: /api/v1/contact
          method: POST
          cors: true
          private: true  # Requiere API Key
```

### Paso a Paso

#### 1. Configurar Variables en AWS

```bash
# Crear parámetros en AWS Systems Manager
aws ssm put-parameter \
    --name /zititex/mysql/host \
    --value "tu-rds-endpoint.rds.amazonaws.com" \
    --type String

aws ssm put-parameter \
    --name /zititex/mysql/user \
    --value "zititex_prod" \
    --type String

aws ssm put-parameter \
    --name /zititex/mysql/password \
    --value "password_seguro" \
    --type SecureString

aws ssm put-parameter \
    --name /zititex/mailgun/api_key \
    --value "key-tu_api_key" \
    --type SecureString
```

#### 2. Desplegar

```bash
# Desarrollo
serverless deploy --stage dev

# Producción
serverless deploy --stage prod

# Verificar deployment
serverless info --stage prod
```

**Salida esperada:**
```
Service Information
service: zititex-api
stage: prod
region: us-east-2
stack: zititex-api-prod
endpoints:
  POST - https://abc123.execute-api.us-east-2.amazonaws.com/prod/api/v1/contact
functions:
  api: zititex-api-prod-api
```

#### 3. Obtener API Key

```bash
# Listar API Keys
serverless info --stage prod

# En la salida verás:
# api keys:
#   zititex-api-key-prod: xxxxxxxxxxxxxxx

# Para hacer requests:
curl -X POST https://abc123.execute-api.us-east-2.amazonaws.com/prod/api/v1/contact \
  -H "x-api-key: xxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{"full_name": "Test", "email": "test@example.com", ...}'
```

#### 4. Ver Logs

```bash
# Logs en tiempo real
serverless logs -f api --tail --stage prod

# Ver últimos logs
serverless logs -f api --stage prod

# CloudWatch Logs
aws logs tail /aws/lambda/zititex-api-prod-api --follow
```

#### 5. Actualizar

```bash
# Re-desplegar después de cambios
serverless deploy --stage prod

# Desplegar solo función (más rápido)
serverless deploy function -f api --stage prod
```

#### 6. Eliminar

```bash
# Eliminar todo (cuidado!)
serverless remove --stage dev
```

---

## 5️⃣ Monitoreo y Mantenimiento

### Health Checks

```bash
# Local/Docker
curl http://localhost:8000/health

# Producción
curl https://api.tudominio.com/health

# AWS Lambda
curl https://abc123.execute-api.us-east-2.amazonaws.com/prod/health
```

### Logs por Ambiente

| Ambiente | Ubicación | Comando |
|----------|-----------|---------|
| **Local** | Terminal | Ver en consola donde corre uvicorn |
| **Docker Dev** | Container logs | `docker-compose logs -f api` |
| **Docker Prod** | Container logs | `docker logs zititex-api` |
| **AWS Lambda** | CloudWatch | `serverless logs -f api --tail` |

### Respaldos

```bash
# Respaldar base de datos
docker exec zititex-mysql-dev mysqldump \
    -u root -prootpass_dev zititex_db > backup_$(date +%Y%m%d).sql

# Restaurar
docker exec -i zititex-mysql-dev mysql \
    -u root -prootpass_dev zititex_db < backup_20240115.sql
```

---

## 6️⃣ Troubleshooting

### Problema: Puerto en uso

```bash
# Error: Address already in use

# Solución: Matar proceso
lsof -ti:8000 | xargs kill -9

# O usar otro puerto
uvicorn app.main:app --port 8001
```

### Problema: No conecta a MySQL

```bash
# Verificar que MySQL está corriendo
docker ps | grep mysql

# Ver logs de MySQL
docker-compose logs mysql

# Probar conexión
mysql -h localhost -P 3307 -u dev_user -p
```

### Problema: Contenedor no inicia

```bash
# Ver logs detallados
docker-compose logs api

# Reconstruir sin caché
docker-compose build --no-cache

# Limpiar todo y empezar de nuevo
docker-compose down -v
docker system prune -a
docker-compose up -d --build
```

---

## 7️⃣ Checklist Pre-Producción

Antes de desplegar a producción, verificar:

- [ ] Variables de entorno configuradas
- [ ] DEBUG=false
- [ ] Contraseñas seguras
- [ ] CORS configurado correctamente
- [ ] Certificados SSL instalados
- [ ] Backups configurados
- [ ] Monitoreo activo
- [ ] Logs configurados
- [ ] Tests passing
- [ ] Documentación actualizada
- [ ] API Keys rotadas
- [ ] Límites de rate configurados

---

**Resumen de Comandos por Ambiente:**

| Acción | Local | Docker Dev | Docker Prod | AWS Lambda |
|--------|-------|------------|-------------|------------|
| **Iniciar** | `make dev` | `make docker-up-dev` | `docker-compose up -d` | `serverless deploy` |
| **Logs** | Terminal | `docker-compose logs -f` | `docker logs -f` | `serverless logs -f api --tail` |
| **Tests** | `pytest` | `docker exec -it zititex-api-dev pytest` | N/A | N/A |
| **Detener** | Ctrl+C | `make docker-down-dev` | `docker-compose down` | N/A |

