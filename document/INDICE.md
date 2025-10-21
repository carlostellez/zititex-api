# 📚 Índice de Documentación - Zititex API

## Navegación Rápida

| Documento | Descripción | Para quién |
|-----------|-------------|------------|
| **[00-LEEME-PRIMERO.md](00-LEEME-PRIMERO.md)** ⭐ | 🚀 EMPIEZA AQUÍ - Guía rápida | NUEVOS DESARROLLADORES |
| **[README.md](README.md)** | 📖 Índice de documentación centralizado | Todos |
| **[REVISION_COMPLETA.md](REVISION_COMPLETA.md)** | 📋 Resumen ejecutivo del proyecto completo | Product Managers, Stakeholders |
| **[ESTRUCTURA.md](ESTRUCTURA.md)** | 🏗️ Detalles de arquitectura y organización | Arquitectos, Desarrolladores |
| **[API_CORREO.md](API_CORREO.md)** | 📧 Funcionamiento detallado del sistema de emails | Backend Developers |
| **[VERIFICACION_SERVERLESS.md](VERIFICACION_SERVERLESS.md)** ⭐ | ☁️ Serverless + Lambda + API Gateway | DevOps, Developers |
| **[DESPLIEGUE.md](DESPLIEGUE.md)** | 🚀 Guía completa de deployment (4 opciones) | DevOps, Developers |
| **[GIT_WORKFLOW.md](GIT_WORKFLOW.md)** ⭐ | 🔄 Git push + GitHub Actions + CI/CD | Developers, DevOps |
| **[PYTEST.md](PYTEST.md)** | 🧪 Guía de testing y cobertura | QA, Developers |
| **[run.md](run.md)** | 🏃 Instrucciones paso a paso para ejecutar | Developers, QA |
| **[prompts.md](prompts.md)** | 💡 Decisiones de diseño y desarrollo | Tech Leads, Architects |

---

## 🎯 ¿Qué Quieres Hacer?

### Para Empezar

<details>
<summary><b>👉 Quiero ejecutar el proyecto por primera vez</b></summary>

1. Lee **[run.md](run.md)** - Guía paso a paso
2. Elige tu método:
   - Local: Sección "Local Development Setup"
   - Docker: Sección "Docker Development"
3. Sigue los pasos exactos
4. Verifica con el health check

**Comando rápido (Docker)**:
```bash
docker-compose -f docker-compose.dev.yml up -d
curl http://localhost:8001/health
```
</details>

<details>
<summary><b>👉 Quiero entender la arquitectura</b></summary>

1. Lee **[ESTRUCTURA.md](ESTRUCTURA.md)** - Organización del código
2. Lee **[../README.md](../README.md)** - Sección "Architecture"
3. Lee **[prompts.md](prompts.md)** - Decisiones de diseño

**Conceptos clave**:
- Clean Architecture
- Repository Pattern
- SOLID Principles
- Dependency Injection
</details>

<details>
<summary><b>👉 Quiero entender cómo funciona el envío de emails</b></summary>

1. Lee **[API_CORREO.md](API_CORREO.md)** - Documentación completa
2. Revisa el diagrama de flujo
3. Ve la sección de configuración Mailgun
4. Prueba con los ejemplos de cURL

**Archivos importantes**:
- `app/api/v1/contact.py` - Endpoint
- `app/services/mailgun.py` - Servicio de email
</details>

<details>
<summary><b>👉 Quiero desplegar en producción</b></summary>

1. Lee **[DESPLIEGUE.md](DESPLIEGUE.md)** completo
2. Elige tu opción de deployment:
   - Docker Producción (sección 3)
   - AWS Lambda (sección 4)
3. Sigue el checklist pre-producción
4. Configura monitoreo

**Checklist crítico**:
- [ ] Variables de entorno configuradas
- [ ] DEBUG=false
- [ ] SSL configurado
- [ ] Backups configurados
</details>

<details>
<summary><b>👉 Quiero ejecutar o crear tests</b></summary>

1. Lee **[PYTEST.md](PYTEST.md)** - Guía completa
2. Ve la sección "Comandos de Pytest"
3. Revisa fixtures en `tests/conftest.py`
4. Sigue el patrón AAA (Arrange-Act-Assert)

**Comandos útiles**:
```bash
pytest                          # Todos los tests
pytest --cov=app               # Con cobertura
pytest -v                      # Verbose
pytest tests/test_api_contact.py  # Archivo específico
```
</details>

<details>
<summary><b>👉 Quiero hacer cambios al código</b></summary>

1. Lee **[ESTRUCTURA.md](ESTRUCTURA.md)** - Organización
2. Identifica la capa correcta:
   - API → `app/api/v1/`
   - Business Logic → `app/services/`
   - Data Access → `app/repositories/`
   - Models → `app/models/`
3. Sigue los patrones existentes
4. Escribe tests
5. Ejecuta `make format && make lint`

**Principios a seguir**:
- SOLID
- Clean Architecture
- Repository Pattern
- Type Hints
</details>

---

## 📂 Estructura de Archivos

### Código Fuente

```
app/
├── main.py                    # Entry point FastAPI
├── api/
│   └── v1/
│       └── contact.py         # ✅ Endpoint de contacto
├── core/
│   ├── config.py              # ✅ Configuración
│   └── database.py            # ✅ Setup MySQL
├── models/
│   └── client.py              # ✅ Modelo ORM
├── schemas/
│   └── client.py              # ✅ Pydantic schemas
├── repositories/
│   └── client_repository.py  # ✅ Repository Pattern
└── services/
    └── mailgun.py             # ✅ Servicio de email
```

### Tests

```
tests/
├── conftest.py                # ✅ Fixtures compartidos
├── test_api_contact.py        # ✅ Tests de endpoint
├── test_models.py             # ✅ Tests de modelos
├── test_repositories.py       # ✅ Tests de repositorio
├── test_schemas.py            # ✅ Tests de validación
├── test_services.py           # ✅ Tests de servicios
├── test_config.py             # ✅ Tests de configuración
└── test_main.py               # ✅ Tests de aplicación
```

### Deployment

```
├── Dockerfile                 # ✅ Producción
├── Dockerfile.dev             # ✅ Desarrollo
├── docker-compose.yml         # ✅ Prod compose
├── docker-compose.dev.yml     # ✅ Dev compose
├── serverless.yml             # ✅ AWS Lambda
├── Makefile                   # ✅ Comandos útiles
└── .env.example               # ✅ Template variables
```

### Documentación

```
document/
├── 00-LEEME-PRIMERO.md        # ⭐ START HERE
├── README.md                  # ✅ Índice centralizado
├── INDICE.md                  # ✅ Este archivo
├── REVISION_COMPLETA.md       # ✅ Resumen ejecutivo
├── ESTRUCTURA.md              # ✅ Arquitectura
├── VERIFICACION_ESTRUCTURA.md # ✅ Verificación estructura
├── RESUMEN_ORGANIZACION.md    # ✅ Resumen organización
├── API_CORREO.md              # ✅ Sistema de emails
├── VERIFICACION_SERVERLESS.md # ⭐ Serverless + Lambda
├── DESPLIEGUE.md              # ✅ Deployment
├── PYTEST.md                  # ✅ Testing
├── run.md                     # ✅ Guía de ejecución
└── prompts.md                 # ✅ Decisiones de diseño
```

---

## 🔍 Buscar Información Específica

### Por Tema

| Tema | Documento | Sección |
|------|-----------|---------|
| **Configurar MySQL** | [run.md](run.md) | "Step 4: Setup MySQL" |
| **Variables de entorno** | [DESPLIEGUE.md](DESPLIEGUE.md) | Cada opción tiene su sección |
| **Crear nuevo endpoint** | [ESTRUCTURA.md](ESTRUCTURA.md) | "Capa 1: API (Routes)" |
| **Agregar validación** | [PYTEST.md](PYTEST.md) | "Tests de Validación" |
| **Debugging** | [PYTEST.md](PYTEST.md) | "Debugging Tests" |
| **Docker troubleshooting** | [DESPLIEGUE.md](DESPLIEGUE.md) | "Troubleshooting" |
| **Mailgun setup** | [API_CORREO.md](API_CORREO.md) | "Configuración de Mailgun" |
| **Repository Pattern** | [prompts.md](prompts.md) | "Repository Pattern" |
| **CI/CD** | [PYTEST.md](PYTEST.md) | "CI/CD Integration" |
| **Health checks** | [REVISION_COMPLETA.md](REVISION_COMPLETA.md) | "Puntos de Verificación Críticos" |
| **Serverless Deploy** ⭐ | [VERIFICACION_SERVERLESS.md](VERIFICACION_SERVERLESS.md) | "Despliegue" |
| **AWS Lambda** ⭐ | [VERIFICACION_SERVERLESS.md](VERIFICACION_SERVERLESS.md) | "Serverless con Lambda" |
| **API Gateway** ⭐ | [VERIFICACION_SERVERLESS.md](VERIFICACION_SERVERLESS.md) | "Arquitectura Serverless" |

### Por Persona/Rol

#### Para Desarrolladores Nuevos
1. ⭐ [00-LEEME-PRIMERO.md](00-LEEME-PRIMERO.md) - START HERE
2. [ESTRUCTURA.md](ESTRUCTURA.md) - Organización del código
3. [run.md](run.md) - Cómo ejecutar
4. [PYTEST.md](PYTEST.md) - Cómo testear

#### Para DevOps
1. ⭐ [VERIFICACION_SERVERLESS.md](VERIFICACION_SERVERLESS.md) - Serverless + Lambda
2. [DESPLIEGUE.md](DESPLIEGUE.md) - Todas las opciones
3. [run.md](run.md) - Setup inicial
4. [REVISION_COMPLETA.md](REVISION_COMPLETA.md) - Checklist

#### Para QA/Testers
1. [PYTEST.md](PYTEST.md) - Guía completa de testing
2. [API_CORREO.md](API_CORREO.md) - Testing manual
3. [run.md](run.md) - Setup ambiente de pruebas

#### Para Product Managers
1. [REVISION_COMPLETA.md](REVISION_COMPLETA.md) - Resumen ejecutivo
2. [README.md](README.md) - Features y arquitectura
3. [API_CORREO.md](API_CORREO.md) - Funcionalidad principal

#### Para Arquitectos/Tech Leads
1. [ESTRUCTURA.md](ESTRUCTURA.md) - Arquitectura detallada
2. [prompts.md](prompts.md) - Decisiones de diseño
3. [README.md](README.md) - Patrones y principios

---

## ⚡ Comandos Más Usados

### Desarrollo

```bash
# Iniciar desarrollo (Docker)
docker-compose -f docker-compose.dev.yml up -d

# Ver logs
docker-compose -f docker-compose.dev.yml logs -f api

# Detener
docker-compose -f docker-compose.dev.yml down
```

### Testing

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html

# Ver reporte
open htmlcov/index.html
```

### Base de Datos

```bash
# Conectar a MySQL (Docker)
docker exec -it zititex-mysql-dev mysql -u dev_user -pdev_pass zititex_db

# Ver tablas
SHOW TABLES;

# Ver registros
SELECT * FROM client ORDER BY created_at DESC LIMIT 5;
```

### API Testing

```bash
# Health check
curl http://localhost:8001/health

# Submit form
curl -X POST http://localhost:8001/api/v1/contact/ \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Test","email":"test@example.com","phone":"1234567890","message":"Test"}'

# Swagger UI
open http://localhost:8001/docs
```

---

## 📊 Métricas del Proyecto

| Métrica | Valor |
|---------|-------|
| **Líneas de código** | ~1,500 |
| **Líneas de tests** | 1,460+ |
| **Número de tests** | 85+ |
| **Cobertura** | >99% |
| **Documentos** | 12 |
| **Endpoints** | 3 |
| **Design Patterns** | 4+ |
| **Deployment Options** | 5 |

---

## ✅ Estado del Proyecto

```
✅ PRODUCTION READY

├── ✅ Arquitectura - Clean Architecture + SOLID
├── ✅ Base de Datos - MySQL integrado
├── ✅ API - Endpoint completo con validación
├── ✅ Emails - Sistema dual (admin + usuario)
├── ✅ Tests - >99% cobertura
├── ✅ Docker - Dev + Prod configurados
├── ✅ Deployment - 4 opciones disponibles
└── ✅ Documentación - 8 documentos completos
```

---

## 🆘 Ayuda y Soporte

### Si tienes problemas...

1. **Revisa troubleshooting**:
   - [run.md](run.md) → Sección "Troubleshooting"
   - [DESPLIEGUE.md](DESPLIEGUE.md) → Sección "Troubleshooting"

2. **Revisa logs**:
   ```bash
   docker-compose logs -f
   ```

3. **Verifica configuración**:
   ```bash
   cat .env
   ```

4. **Limpia y reinicia**:
   ```bash
   docker-compose down -v
   docker-compose up -d --build
   ```

### Recursos Externos

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Docker Documentation](https://docs.docker.com/)
- [Mailgun API Docs](https://documentation.mailgun.com/)

---

## 🔄 Flujo de Trabajo Recomendado

### Para Nuevas Features

1. Lee [ESTRUCTURA.md](ESTRUCTURA.md) para entender dónde poner el código
2. Escribe el código siguiendo patrones existentes
3. Escribe tests (ver [PYTEST.md](PYTEST.md))
4. Ejecuta `make test`
5. Ejecuta `make format && make lint`
6. Commit y push

### Para Bugs

1. Reproduce el bug localmente
2. Escribe un test que falle (reproduce el bug)
3. Arregla el bug
4. Verifica que el test pasa
5. Ejecuta suite completa de tests
6. Commit y push

### Para Deployment

1. Lee [DESPLIEGUE.md](DESPLIEGUE.md)
2. Elige tu opción (Docker/Lambda)
3. Sigue el checklist pre-producción
4. Deploy a staging primero
5. Verifica funcionamiento
6. Deploy a producción

---

**Última actualización**: 2024  
**Versión del proyecto**: 1.0.0  
**Estado**: ✅ Production Ready

---

¿Necesitas agregar algo a esta documentación? ¡Siéntete libre de contribuir!

