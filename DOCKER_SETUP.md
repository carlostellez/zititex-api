# 🐳 Configuración de Docker Hub para CI/CD

Esta guía te ayudará a configurar los secrets de Docker Hub para que GitHub Actions pueda construir y pushear imágenes automáticamente.

---

## 📋 Paso 1: Crear Cuenta en Docker Hub (si no tienes)

1. Ve a: https://hub.docker.com/signup
2. Crea tu cuenta o inicia sesión
3. Verifica tu email

---

## 🔑 Paso 2: Generar Access Token

### 2.1 Ir a Security Settings

1. **Inicia sesión** en Docker Hub
2. Ve a: https://hub.docker.com/settings/security
3. O navega: `Account Settings` → `Security`

### 2.2 Crear Access Token

1. Click en **"New Access Token"**
2. Configuración del token:
   ```
   Access Token Description: GitHub Actions - Zititex API
   Access permissions: Read, Write, Delete
   ```
3. Click **"Generate"**
4. **IMPORTANTE**: Copia el token INMEDIATAMENTE
   - Solo se muestra UNA vez
   - Guárdalo en un lugar seguro temporalmente

**Ejemplo del token:**
```
dckr_pat_1234567890abcdefghijklmnopqrstuvwxyz
```

---

## ⚙️ Paso 3: Configurar Secrets en GitHub

### 3.1 Ir a Settings del Repositorio

1. Ve a tu repositorio: https://github.com/carlostellez/zititex-api
2. Click en **"Settings"** (tab superior)
3. En el menú lateral, busca "Secrets and variables"
4. Click en **"Actions"**

O ve directo a:
🔗 https://github.com/carlostellez/zititex-api/settings/secrets/actions

### 3.2 Agregar DOCKER_USERNAME

1. Click en **"New repository secret"**
2. Configurar:
   ```
   Name: DOCKER_USERNAME
   Secret: tu_usuario_dockerhub
   ```
   
   **Ejemplo:**
   ```
   Name: DOCKER_USERNAME
   Secret: carlostellez
   ```

3. Click **"Add secret"**
4. ✅ Debería aparecer en la lista

### 3.3 Agregar DOCKER_PASSWORD

1. Click en **"New repository secret"** nuevamente
2. Configurar:
   ```
   Name: DOCKER_PASSWORD
   Secret: dckr_pat_tu_token_aqui
   ```
   
   **Ejemplo:**
   ```
   Name: DOCKER_PASSWORD
   Secret: dckr_pat_1234567890abcdefghijklmnopqrstuvwxyz
   ```

3. Click **"Add secret"**
4. ✅ Debería aparecer en la lista

### 3.4 Verificar Secrets

Deberías ver en la lista:
```
✅ DOCKER_USERNAME
✅ DOCKER_PASSWORD
```

**NOTA**: No podrás ver los valores, solo los nombres.

---

## 🔄 Paso 4: Trigger del Workflow

### Opción A: Push un Cambio

```bash
# Hacer un pequeño cambio
echo "Docker secrets configured" >> DOCKER_SETUP.md
git add DOCKER_SETUP.md
git commit -m "docs: add Docker Hub setup guide"
git push origin main
```

### Opción B: Re-run Workflow

1. Ve a: https://github.com/carlostellez/zititex-api/actions
2. Selecciona el workflow "CI" o "CD"
3. Click en "Re-run jobs"

---

## ✅ Paso 5: Verificar que Funcione

### 5.1 Ver Actions

1. Ve a: https://github.com/carlostellez/zititex-api/actions
2. Deberías ver el workflow ejecutándose
3. Espera a que termine

### 5.2 Verificar Build

El workflow de **CD** debería:
- ✅ Build de imagen Docker
- ✅ Login a Docker Hub (usando tus secrets)
- ✅ Push de imagen a Docker Hub
- ✅ Tag con SHA del commit

### 5.3 Verificar en Docker Hub

1. Ve a: https://hub.docker.com/r/TU_USUARIO/zititex-api
2. Deberías ver:
   - Repositorio creado
   - Tags de imágenes
   - Información del último push

**Ejemplo de tags que verás:**
```
main           - Latest from main branch
sha-03ca921    - Specific commit
latest         - Always points to newest
```

---

## 🐛 Troubleshooting

### Error: "denied: requested access to the resource is denied"

**Causa**: Token sin permisos suficientes

**Solución**:
1. Crear nuevo token con permisos: Read, Write, Delete
2. Actualizar el secret DOCKER_PASSWORD en GitHub
3. Re-run del workflow

### Error: "invalid username/password"

**Causa**: Username o password incorrectos

**Solución**:
1. Verificar DOCKER_USERNAME (debe ser tu username, no email)
2. Verificar DOCKER_PASSWORD (debe ser el token completo)
3. Regenerar token si es necesario

### Error: "repository does not exist"

**Causa**: Repositorio no existe en Docker Hub

**Solución**:
El repositorio se crea automáticamente en el primer push.
Si persiste:
1. Crear repositorio manualmente en Docker Hub
2. Nombre: `TU_USUARIO/zititex-api`
3. Re-run workflow

### Workflow no se ejecuta

**Causa**: Workflow disabled o branch protection

**Solución**:
1. Ve a Settings → Actions → General
2. Verificar "Allow all actions"
3. Verificar que workflows estén enabled

---

## 📊 Estado Esperado

Después de configurar correctamente:

### GitHub Actions
```
✅ CI Workflow
   ✅ Lint and Code Quality
   ✅ Tests
   ✅ Security Checks

✅ CD Workflow
   ✅ Build Docker Image
   ✅ Login to Docker Hub
   ✅ Push Image
   ✅ Tag Image
```

### Docker Hub
```
✅ Repository: carlostellez/zititex-api
✅ Images: Con tags apropiados
✅ Last pushed: Fecha reciente
✅ Size: ~500MB (aproximado)
```

---

## 🔒 Seguridad

### Mejores Prácticas

1. **Tokens de acceso, no passwords**
   - ✅ Usa Access Tokens
   - ❌ No uses tu password de Docker Hub

2. **Permisos mínimos**
   - Para CI/CD: Read, Write
   - Delete solo si es necesario

3. **Rotación de tokens**
   - Rota tokens cada 90-180 días
   - Revoca tokens no utilizados

4. **Secrets en GitHub**
   - Nunca commitees secrets en código
   - Usa GitHub Secrets
   - No compartas secrets

### Revocar Token

Si necesitas revocar un token:
1. Ve a: https://hub.docker.com/settings/security
2. Encuentra tu token
3. Click en "Delete"
4. Genera un nuevo token
5. Actualiza el secret en GitHub

---

## 🎯 Resumen de URLs

| Servicio | URL |
|----------|-----|
| Docker Hub Security | https://hub.docker.com/settings/security |
| GitHub Secrets | https://github.com/carlostellez/zititex-api/settings/secrets/actions |
| GitHub Actions | https://github.com/carlostellez/zititex-api/actions |
| Docker Hub Repo | https://hub.docker.com/r/carlostellez/zititex-api |

---

## ✅ Checklist Final

Antes de continuar, verifica:

- [ ] Cuenta en Docker Hub creada
- [ ] Access Token generado
- [ ] Token copiado y guardado
- [ ] Secret DOCKER_USERNAME agregado en GitHub
- [ ] Secret DOCKER_PASSWORD agregado en GitHub
- [ ] Workflow triggered (push o re-run)
- [ ] Workflow ejecutado exitosamente
- [ ] Imagen visible en Docker Hub

---

## 🎉 ¡Listo!

Una vez configurado, cada push a `main` o tag de versión (`v*`) automáticamente:

1. Construirá una imagen Docker
2. La pusheará a Docker Hub
3. La taggeará apropiadamente
4. Estará lista para deployment

**Próximo paso**: Desplegar la imagen en tu servidor!

```bash
# Pull y run de tu imagen
docker pull carlostellez/zititex-api:latest
docker run -d -p 8000:8000 carlostellez/zititex-api:latest
```

---

**¿Necesitas ayuda?** El asistente puede ayudarte con cualquier paso! 🚀

