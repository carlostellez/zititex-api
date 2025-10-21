# 🔄 Git Workflow con GitHub Actions

**Guía completa de cómo hacer push y activar CI/CD**

---

## 🚀 Flujo Completo

### 1️⃣ Preparar Cambios

```bash
# Ver estado actual
git status

# Ver qué cambios tienes
git diff

# Ver archivos modificados
git diff --name-only
```

### 2️⃣ Agregar Archivos

```bash
# Agregar todos los cambios
git add .

# O selectivamente
git add app/main.py
git add requirements.txt
git add document/
```

### 3️⃣ Hacer Commit

```bash
# Commit simple
git commit -m "fix: enable /docs and /redoc permanently"

# Commit con mensaje detallado
git commit -m "fix: enable API documentation endpoints

- Enable /docs and /redoc regardless of DEBUG mode
- Update root endpoint to show documentation links
- Add missing dependencies (greenlet, email-validator)
- Create serverless verification documentation"
```

### 4️⃣ Push a GitHub

```bash
# Push a main (esto activará GitHub Actions)
git push origin main

# O si tu rama principal es master:
git push origin master
```

---

## 🤖 Qué Sucede Después del Push

### Workflow de GitHub Actions

Cuando haces push a `main` o `master`, se activa automáticamente el workflow definido en `.github/workflows/deploy.yml`:

```
Push a GitHub
    ↓
GitHub Actions detecta el push
    ↓
┌─────────────────────────────────────┐
│  JOB 1: TEST                        │
│  ─────────────────────────────────  │
│  ✅ Checkout code                   │
│  ✅ Setup Python 3.12               │
│  ✅ Install dependencies            │
│  ✅ Run pytest                      │
│  ✅ Upload coverage                 │
└─────────────────────────────────────┘
    ↓ (Si los tests pasan)
┌─────────────────────────────────────┐
│  JOB 2: DEPLOY                      │
│  ─────────────────────────────────  │
│  ✅ Checkout code                   │
│  ✅ Setup Node.js 20                │
│  ✅ Setup Python 3.12               │
│  ✅ Install dependencies            │
│  ✅ Configure AWS credentials       │
│  ✅ Deploy to AWS Lambda            │
└─────────────────────────────────────┘
    ↓
🎉 API disponible en AWS Lambda
```

---

## 📋 Convenciones de Commits

Usa [Conventional Commits](https://www.conventionalcommits.org/):

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| `feat:` | Nueva funcionalidad | `feat: add user authentication` |
| `fix:` | Corrección de bug | `fix: resolve database connection issue` |
| `docs:` | Cambios en documentación | `docs: update API documentation` |
| `style:` | Formato, espacios, etc. | `style: format code with black` |
| `refactor:` | Refactorización de código | `refactor: simplify email service` |
| `test:` | Agregar o modificar tests | `test: add integration tests` |
| `chore:` | Tareas de mantenimiento | `chore: update dependencies` |
| `perf:` | Mejoras de rendimiento | `perf: optimize database queries` |
| `ci:` | Cambios en CI/CD | `ci: update GitHub Actions workflow` |

### Ejemplos

```bash
# Nueva funcionalidad
git commit -m "feat: add password reset endpoint"

# Corrección de bug
git commit -m "fix: resolve CORS issue in production"

# Documentación
git commit -m "docs: add deployment guide"

# Tests
git commit -m "test: add unit tests for email service"

# Con scope (opcional)
git commit -m "feat(api): add user profile endpoint"
git commit -m "fix(auth): resolve token expiration bug"
```

---

## 🌿 Estrategia de Branches

### Branches Principales

```
main/master  → Producción (protegida)
develop      → Desarrollo (opcional)
```

### Flujo de Trabajo

#### Opción 1: Flujo Simple (Recomendado para proyectos pequeños)

```bash
# 1. Trabajar directamente en main
git checkout main
git pull origin main

# 2. Hacer cambios
# ... editar archivos ...

# 3. Commit y push
git add .
git commit -m "feat: add new feature"
git push origin main
```

#### Opción 2: Flujo con Feature Branches (Recomendado para equipos)

```bash
# 1. Crear rama de feature
git checkout -b feature/user-auth

# 2. Hacer cambios
# ... editar archivos ...

# 3. Commit
git add .
git commit -m "feat: implement user authentication"

# 4. Push de la rama
git push origin feature/user-auth

# 5. Crear Pull Request en GitHub
# (desde la interfaz web)

# 6. Después de merge, actualizar main local
git checkout main
git pull origin main

# 7. Eliminar rama local (opcional)
git branch -d feature/user-auth
```

---

## 🔒 Configurar Secrets en GitHub

**Antes del primer push que ejecute deploy**, configura los secrets:

### Paso 1: Ir a GitHub

1. Abre tu repositorio en GitHub
2. Ve a **Settings** > **Secrets and variables** > **Actions**
3. Click en **New repository secret**

### Paso 2: Agregar Secrets

Agrega los siguientes secrets:

| Secret Name | Descripción | Ejemplo |
|-------------|-------------|---------|
| `AWS_ACCESS_KEY_ID` | AWS Access Key | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | AWS Secret Key | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `MAILGUN_API_KEY` | Mailgun API Key | `key-xxxxxxxxxxxxxxxxx` |
| `MAILGUN_DOMAIN` | Mailgun Domain | `mg.yourdomain.com` |
| `ADMIN_EMAIL` | Email del administrador | `admin@yourdomain.com` |

### Paso 3: Verificar

```bash
# Después de configurar secrets, haz push
git push origin main

# Ve a la pestaña "Actions" en GitHub para ver el progreso
```

---

## 📊 Monitorear GitHub Actions

### Ver Workflows

1. **En GitHub**: Ve a la pestaña **Actions**
2. Verás una lista de workflows ejecutándose o completados
3. Click en uno para ver detalles

### Estados Posibles

| Estado | Icono | Descripción |
|--------|-------|-------------|
| ✅ Success | 🟢 | Workflow completado exitosamente |
| ❌ Failure | 🔴 | Workflow falló |
| 🟡 In Progress | 🟡 | Workflow ejecutándose |
| ⚠️ Cancelled | ⚪ | Workflow cancelado |

### Ver Logs

```bash
# Desde la terminal (requiere GitHub CLI)
gh run list
gh run view <run-id>
gh run watch
```

---

## 🐛 Troubleshooting

### Problema 1: Tests Fallan

```bash
# Ejecutar tests localmente antes de push
source venv/bin/activate
pytest

# Ver cobertura
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

### Problema 2: Deploy Falla

```bash
# Verificar secrets en GitHub
# Settings > Secrets and variables > Actions

# Verificar AWS credentials localmente
aws sts get-caller-identity

# Deploy manual para debug
npx serverless deploy --stage dev --verbose
```

### Problema 3: Merge Conflicts

```bash
# Actualizar tu rama con main
git checkout main
git pull origin main
git checkout tu-rama
git merge main

# Resolver conflictos
# ... editar archivos con conflictos ...

git add .
git commit -m "fix: resolve merge conflicts"
git push origin tu-rama
```

---

## 🎯 Comandos Rápidos

```bash
# Flujo completo rápido
git add .
git commit -m "feat: add new feature"
git push origin main

# Ver último commit
git log -1

# Ver commits recientes
git log --oneline -5

# Deshacer último commit (mantener cambios)
git reset --soft HEAD~1

# Deshacer último commit (descartar cambios)
git reset --hard HEAD~1

# Ver ramas
git branch -a

# Cambiar de rama
git checkout nombre-rama

# Crear y cambiar a nueva rama
git checkout -b nueva-rama

# Eliminar rama local
git branch -d nombre-rama

# Actualizar desde remoto
git pull origin main
```

---

## 📝 Checklist Pre-Push

Antes de hacer push, verifica:

- [ ] ✅ Tests pasan localmente: `pytest`
- [ ] ✅ Código formateado: `make format` o `black .`
- [ ] ✅ Linter pasa: `make lint` o `flake8 .`
- [ ] ✅ Type hints correctos: `mypy app/`
- [ ] ✅ Documentación actualizada
- [ ] ✅ Commit message claro y descriptivo
- [ ] ✅ .env no incluido (verificar .gitignore)
- [ ] ✅ Secrets configurados en GitHub (para deploy)

```bash
# Ejecutar checklist rápido
make test
make lint
make format
git status
```

---

## 🔐 Proteger Rama Main

### Configurar Branch Protection en GitHub

1. **Settings** > **Branches** > **Add rule**
2. Branch name pattern: `main`
3. Marcar:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Include administrators

---

## 🚀 Ejemplo Completo

```bash
# 1. Ver qué cambios tengo
git status
git diff

# 2. Ejecutar tests localmente
source venv/bin/activate
pytest
make lint

# 3. Agregar cambios
git add .

# 4. Commit con mensaje descriptivo
git commit -m "fix: enable /docs and /redoc permanently

- Enable documentation endpoints regardless of DEBUG mode
- Update root endpoint to show docs links
- Add missing dependencies
- Update documentation"

# 5. Push (esto activa GitHub Actions)
git push origin main

# 6. Monitorear en GitHub
# Ve a: https://github.com/tu-usuario/tu-repo/actions
```

---

## 📚 Recursos Adicionales

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

---

**Última actualización**: 20 de Octubre, 2024  
**Versión**: 1.0.0

