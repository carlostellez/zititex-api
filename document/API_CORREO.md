# 📧 Funcionamiento de la API de Correo

## Diagrama de Flujo Completo

```
┌─────────────────────────────────────────────────────────────┐
│                    Usuario Envía Formulario                  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  POST /api/v1/contact/                                       │
│  {                                                           │
│    "full_name": "Juan Pérez",                               │
│    "email": "juan@example.com",                             │
│    "phone": "+52 123 456 7890",                             │
│    "company": "Empresa S.A." (opcional),                    │
│    "product_type": "Textiles" (opcional),                   │
│    "quantity": "Más de 10,000 unidades" (opcional),                              │
│    "message": "Necesito información..."                     │
│  }                                                           │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  1. VALIDACIÓN DE DATOS (Pydantic)                          │
│     ✅ Formato de email correcto                            │
│     ✅ Longitud de campos                                   │
│     ✅ Teléfono contiene dígitos                            │
│     ✅ Campos requeridos presentes                          │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  2. VERIFICACIÓN DE CONFIGURACIÓN                           │
│     ✅ Mailgun API Key configurada                          │
│     ✅ Mailgun Domain configurado                           │
│     ✅ Admin Email configurado                              │
│     ❌ Si falla → Error 500                                 │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  3. GUARDAR EN BASE DE DATOS (MySQL)                        │
│     📝 Crear registro en tabla 'client'                     │
│     📝 Generar ID auto-incremental                          │
│     📝 Timestamps created_at, updated_at                    │
│     ✅ Confirmar transacción                                │
│     🎯 ID retornado: client.id                              │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  4. ENVIAR EMAIL AL ADMINISTRADOR                           │
│     📧 Destinatario: admin@example.com                      │
│     📋 Asunto: "Nuevo mensaje de contacto de Juan Pérez"   │
│     📄 Contenido HTML con todos los datos                   │
│     🔄 Reply-To: juan@example.com (para responder directo) │
│     ✅ Email enviado vía Mailgun API                        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  5. ENVIAR EMAIL DE CONFIRMACIÓN AL USUARIO                 │
│     📧 Destinatario: juan@example.com                       │
│     📋 Asunto: "Gracias por contactarnos - Zititex"        │
│     📄 Contenido HTML con resumen de su mensaje             │
│     ✅ Email enviado vía Mailgun API                        │
│     ⚠️  Si falla, no se considera error crítico             │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  6. RESPUESTA AL CLIENTE                                     │
│  {                                                           │
│    "success": true,                                          │
│    "message": "Mensaje enviado exitosamente...",            │
│    "data": {                                                 │
│      "id": 1,                                                │
│      "name": "Juan Pérez",                                   │
│      "email": "juan@example.com",                            │
│      "timestamp": "2024-01-15T10:30:00"                      │
│    }                                                         │
│  }                                                           │
└─────────────────────────────────────────────────────────────┘
```

## Código del Endpoint

### Ubicación: `app/api/v1/contact.py`

```python
@router.post("/", response_model=ContactResponse)
async def submit_contact_form(
    contact_data: ContactForm,
    db: AsyncSession = Depends(get_async_db),
) -> ContactResponse:
    """
    Procesa formulario de contacto:
    1. Valida datos
    2. Verifica configuración
    3. Guarda en BD
    4. Envía emails
    5. Retorna respuesta
    """
```

## Flujo Detallado por Paso

### Paso 1: Recepción y Validación

**Schema Pydantic (ContactForm)**:
```python
class ContactForm(BaseModel):
    full_name: str        # Requerido, 2-100 caracteres
    email: EmailStr       # Requerido, formato email válido
    phone: str            # Requerido, 10-20 caracteres, debe tener dígitos
    company: Optional[str] = None       # Opcional, max 255
    product_type: Optional[str] = None  # Opcional, max 100
    quantity: Optional[int] = None      # Opcional, >= 1
    message: str          # Requerido, 10-2000 caracteres
```

**Validaciones Automáticas**:
- ✅ Formato de email válido
- ✅ Longitudes min/max
- ✅ Tipos de datos correctos
- ✅ Campos requeridos presentes

### Paso 2: Verificación de Configuración

```python
# Verifica que las credenciales de Mailgun estén configuradas
if not settings.mailgun_api_key or not settings.mailgun_domain:
    raise HTTPException(500, "Email service not configured")

# Verifica que el email del admin esté configurado
if not settings.admin_email:
    raise HTTPException(500, "Admin email not configured")
```

**Variables Requeridas en .env**:
```bash
MAILGUN_API_KEY=key-xxxxxxxxxxxxxxxxx
MAILGUN_DOMAIN=mg.tudominio.com
ADMIN_EMAIL=admin@tudominio.com
```

### Paso 3: Guardar en Base de Datos

```python
# Usar Repository Pattern para acceso a datos
client_repo = ClientRepository(db)

# Crear objeto ClientCreate
client_create = ClientCreate(
    full_name=contact_data.full_name,
    email=contact_data.email,
    phone=contact_data.phone,
    company=contact_data.company,
    product_type=contact_data.product_type,
    quantity=contact_data.quantity,
    message=contact_data.message,
)

# Guardar en base de datos (operación async)
client = await client_repo.create_async(client_create)

# client.id contiene el ID generado automáticamente
print(f"✅ Client saved with ID: {client.id}")
```

**Registro en MySQL**:
```sql
INSERT INTO client (
    full_name, email, phone, company, 
    product_type, quantity, message,
    created_at, updated_at
) VALUES (
    'Juan Pérez', 'juan@example.com', '+52 123 456 7890',
    'Empresa S.A.', 'Textiles', 100,
    'Necesito información sobre...',
    NOW(), NOW()
);
```

### Paso 4: Email al Administrador

**Función**: `mailgun_service.send_contact_form_email()`

**Email 1 - Notificación al Admin**:

```html
Asunto: "Nuevo mensaje de contacto de Juan Pérez"
Destinatario: admin@tudominio.com
Reply-To: juan@example.com

HTML:
<h1>Nuevo Mensaje de Contacto</h1>
<p>Has recibido un nuevo mensaje desde la landing page:</p>

<div>
  <h2>Información del Contacto:</h2>
  <p><strong>Nombre completo:</strong> Juan Pérez</p>
  <p><strong>Empresa:</strong> Empresa S.A.</p>
  <p><strong>Email:</strong> juan@example.com</p>
  <p><strong>Teléfono:</strong> +52 123 456 7890</p>
  <p><strong>Tipo de producto:</strong> Textiles</p>
  <p><strong>Cantidad:</strong> 100</p>
  <p><strong>Mensaje:</strong></p>
  <div>Necesito información sobre sus productos...</div>
</div>

<p><strong>Fecha:</strong> 15/01/2024 10:30:00</p>
```

**Características**:
- ✅ Reply-To configura para responder directamente al usuario
- ✅ Incluye TODOS los datos del formulario
- ✅ Formato HTML profesional
- ✅ Timestamp de recepción
- ✅ Campos opcionales solo aparecen si tienen valor

### Paso 5: Email de Confirmación al Usuario

**Email 2 - Confirmación al Usuario**:

```html
Asunto: "Gracias por contactarnos - Zititex"
Destinatario: juan@example.com

HTML:
<h1>¡Gracias por contactarnos!</h1>
<p>Hola Juan Pérez,</p>
<p>Hemos recibido tu mensaje y nos pondremos en contacto contigo pronto.</p>

<div>
  <h3>Resumen de tu mensaje:</h3>
  <p><strong>Email:</strong> juan@example.com</p>
  <p><strong>Teléfono:</strong> +52 123 456 7890</p>
  <p><strong>Empresa:</strong> Empresa S.A.</p>
  <p><strong>Mensaje:</strong></p>
  <div>Necesito información sobre... (primeros 200 caracteres)</div>
</div>

<p>Te responderemos en las próximas 24 horas.</p>
<p>Saludos,<br>El equipo de Zititex</p>
```

**Características**:
- ✅ Confirmación automática inmediata
- ✅ Resumen de lo enviado
- ✅ Mensaje personalizado con el nombre
- ✅ Si falla, NO es error crítico (datos ya guardados)

### Paso 6: Respuesta al Cliente

```json
HTTP 200 OK

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

## Manejo de Errores

### Error 1: Validación de Datos

```json
HTTP 422 Unprocessable Entity

{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

### Error 2: Servicio de Email No Configurado

```json
HTTP 500 Internal Server Error

{
  "detail": "Email service not configured"
}
```

### Error 3: Error de Base de Datos

```json
HTTP 500 Internal Server Error

{
  "detail": "Error processing contact form: [detalles del error]"
}
```

## Configuración de Mailgun

### 1. Obtener Credenciales

1. Ir a https://app.mailgun.com/
2. Crear cuenta o iniciar sesión
3. Ir a "Sending" → "Domain Settings"
4. Copiar:
   - **API Key**: En "API Keys"
   - **Domain**: Tu dominio verificado (ej: mg.tudominio.com)

### 2. Configurar en .env

```bash
MAILGUN_API_KEY=key-1234567890abcdef1234567890abcdef
MAILGUN_DOMAIN=mg.tudominio.com
MAILGUN_BASE_URL=https://api.mailgun.net/v3
ADMIN_EMAIL=admin@tudominio.com
```

### 3. Verificar Dominio

En Mailgun dashboard:
1. Agregar dominio
2. Configurar DNS records:
   - TXT record para SPF
   - TXT record para DKIM
   - CNAME para tracking
3. Esperar verificación (puede tardar 24-48h)

## Testing Manual

### Usando cURL:

```bash
curl -X POST http://localhost:8000/api/v1/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "email": "test@example.com",
    "phone": "1234567890",
    "message": "Este es un mensaje de prueba"
  }'
```

### Usando Swagger UI:

1. Abrir http://localhost:8000/docs
2. Expandir `POST /api/v1/contact/`
3. Click en "Try it out"
4. Llenar el JSON de ejemplo
5. Click en "Execute"
6. Ver respuesta

### Usando Postman:

```
POST http://localhost:8000/api/v1/contact/
Content-Type: application/json

Body (raw JSON):
{
  "full_name": "Juan Pérez",
  "email": "juan@example.com",
  "phone": "+52 123 456 7890",
  "company": "Test Corp",
  "product_type": "Textiles",
  "quantity": "Más de 10,000 unidades",
  "message": "Necesito información sobre sus productos textiles."
}
```

## Monitoreo

### Logs de la Aplicación

```bash
# Ver logs en tiempo real
docker-compose logs -f api

# Buscar logs específicos
docker-compose logs api | grep "Contact data received"
docker-compose logs api | grep "Client saved"
```

### Logs de Mailgun

1. Ir a Mailgun Dashboard
2. "Sending" → "Logs"
3. Ver emails enviados, entregados, abiertos, clicks

### Verificar en Base de Datos

```sql
-- Ver últimos registros
SELECT * FROM client ORDER BY created_at DESC LIMIT 10;

-- Contar registros por día
SELECT DATE(created_at) as fecha, COUNT(*) as total
FROM client
GROUP BY DATE(created_at)
ORDER BY fecha DESC;

-- Buscar por email
SELECT * FROM client WHERE email = 'juan@example.com';
```

## Rendimiento

### Tiempos Esperados

- **Validación**: < 10ms
- **Guardar en BD**: < 50ms
- **Envío de emails**: 200-500ms (depende de Mailgun)
- **Total**: < 1 segundo

### Optimizaciones Implementadas

✅ **Async/Await**: Operaciones no bloqueantes
✅ **Connection Pooling**: Reutilizar conexiones BD
✅ **Índices en BD**: Búsquedas rápidas por email, fecha
✅ **Error Handling**: No falla si email confirmación falla

## Seguridad

### Protecciones Implementadas

✅ **Input Validation**: Pydantic valida todos los campos
✅ **SQL Injection**: SQLAlchemy ORM previene
✅ **XSS Prevention**: Email HTML sanitizado
✅ **CORS**: Configurable por ambiente
✅ **Rate Limiting**: (Pendiente implementar)
✅ **API Keys**: Credenciales en variables de entorno

## Próximas Mejoras

1. **Rate Limiting**: Limitar requests por IP
2. **CAPTCHA**: Prevenir spam
3. **Webhooks Mailgun**: Tracking de emails abiertos
4. **Cola de Mensajes**: RabbitMQ para procesar async
5. **Templates Mailgun**: Usar templates de Mailgun
6. **Attachments**: Permitir adjuntar archivos
7. **Notificaciones SMS**: Vía Twilio
8. **Auto-respuestas**: Respuestas automáticas inteligentes

