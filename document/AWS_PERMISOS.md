# 🔐 Configuración de Permisos AWS para Serverless

**Fecha**: 20 de Octubre, 2024

---

## ❌ Error Actual

```
User: arn:aws:iam::910162731648:user/front-end is not authorized to perform: 
cloudformation:DescribeStacks because no identity-based policy allows the 
cloudformation:DescribeStacks action
```

**Causa**: El usuario IAM `front-end` no tiene permisos suficientes para desplegar con Serverless Framework.

---

## ✅ Solución: Agregar Permisos IAM

### Opción 1: Usar Políticas Administradas de AWS (Recomendado para desarrollo)

Ve a **AWS Console > IAM > Users > front-end > Add permissions**

Agregar estas políticas administradas:
- ✅ `AWSLambdaFullAccess`
- ✅ `AmazonAPIGatewayAdministrator`
- ✅ `AWSCloudFormationFullAccess`
- ✅ `IAMFullAccess` (o `IAMReadOnlyAccess` + permisos específicos)
- ✅ `CloudWatchLogsFullAccess`

### Opción 2: Política Personalizada Mínima (Recomendado para producción)

Crear una política personalizada con permisos mínimos necesarios:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:*"
      ],
      "Resource": [
        "arn:aws:cloudformation:us-east-2:910162731648:stack/zititex-api-*/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "lambda:*"
      ],
      "Resource": [
        "arn:aws:lambda:us-east-2:910162731648:function:zititex-api-*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "apigateway:*"
      ],
      "Resource": [
        "arn:aws:apigateway:us-east-2::/restapis",
        "arn:aws:apigateway:us-east-2::/restapis/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iam:GetRole",
        "iam:CreateRole",
        "iam:DeleteRole",
        "iam:PutRolePolicy",
        "iam:DeleteRolePolicy",
        "iam:AttachRolePolicy",
        "iam:DetachRolePolicy",
        "iam:PassRole"
      ],
      "Resource": [
        "arn:aws:iam::910162731648:role/zititex-api-*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams"
      ],
      "Resource": [
        "arn:aws:logs:us-east-2:910162731648:log-group:/aws/lambda/zititex-api-*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": [
        "arn:aws:s3:::zititex-api-*/*"
      ]
    }
  ]
}
```

### Opción 3: Crear Nuevo Usuario IAM Específico (Más seguro)

```bash
# 1. Crear nuevo usuario para serverless
aws iam create-user --user-name zititex-serverless-deploy

# 2. Crear access key
aws iam create-access-key --user-name zititex-serverless-deploy

# 3. Adjuntar políticas necesarias
aws iam attach-user-policy \
  --user-name zititex-serverless-deploy \
  --policy-arn arn:aws:iam::aws:policy/AWSLambdaFullAccess

aws iam attach-user-policy \
  --user-name zititex-serverless-deploy \
  --policy-arn arn:aws:iam::aws:policy/AmazonAPIGatewayAdministrator

aws iam attach-user-policy \
  --user-name zititex-serverless-deploy \
  --policy-arn arn:aws:iam::aws:policy/AWSCloudFormationFullAccess
```

---

## 🔧 Pasos para Aplicar (Opción 1 - Rápido)

### 1. Ir a AWS Console

```
https://console.aws.amazon.com/iam/
```

### 2. Navegar al Usuario

```
IAM > Users > front-end > Permissions
```

### 3. Agregar Permisos

Click en **"Add permissions"** > **"Attach policies directly"**

Buscar y seleccionar:
- [x] AWSLambdaFullAccess
- [x] AmazonAPIGatewayAdministrator  
- [x] AWSCloudFormationFullAccess
- [x] IAMFullAccess
- [x] CloudWatchLogsFullAccess

Click en **"Add permissions"**

### 4. Verificar Permisos

Volver a ejecutar el deploy desde GitHub Actions:
```
GitHub > Actions > Re-run jobs
```

O hacer un nuevo push:
```bash
git commit --allow-empty -m "trigger: test deploy with new permissions"
git push origin master
```

---

## 🎯 Permisos Específicos Necesarios por Serverless

| Servicio | Acciones | Para qué |
|----------|----------|----------|
| **CloudFormation** | DescribeStacks, CreateStack, UpdateStack, DeleteStack | Gestionar el stack de infraestructura |
| **Lambda** | CreateFunction, UpdateFunctionCode, GetFunction, DeleteFunction | Crear y actualizar funciones Lambda |
| **API Gateway** | CreateRestApi, CreateResource, CreateMethod, PutIntegration | Crear y configurar API Gateway |
| **IAM** | CreateRole, AttachRolePolicy, PassRole | Crear roles para Lambda |
| **CloudWatch Logs** | CreateLogGroup, PutLogEvents | Logs de Lambda |
| **S3** | CreateBucket, PutObject | Almacenar artifacts de deploy |

---

## ⚠️ Consideraciones de Seguridad

### Para Desarrollo
✅ Usar políticas administradas (más simple)
✅ Permisos amplios están OK

### Para Producción
✅ Usar política personalizada mínima
✅ Restringir por recursos específicos (ARNs)
✅ Usar diferentes usuarios para dev/prod
✅ Habilitar MFA en usuarios con permisos amplios
✅ Rotar Access Keys regularmente

---

## 🔍 Verificar Permisos Actuales

```bash
# Ver políticas del usuario
aws iam list-attached-user-policies --user-name front-end

# Ver permisos inline
aws iam list-user-policies --user-name front-end

# Simular acción específica
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::910162731648:user/front-end \
  --action-names cloudformation:DescribeStacks \
  --resource-arns "arn:aws:cloudformation:us-east-2:910162731648:stack/zititex-api-prod/*"
```

---

## 📝 Checklist Post-Configuración

Después de agregar permisos:

- [ ] Permisos IAM actualizados en AWS Console
- [ ] Re-ejecutar GitHub Actions workflow
- [ ] Verificar que el deploy complete sin errores
- [ ] Verificar que el API Gateway se creó
- [ ] Verificar que la función Lambda se desplegó
- [ ] Probar el endpoint del API

---

## 🚀 Próximos Pasos

1. **Agregar permisos al usuario `front-end`** (Opción 1 arriba)
2. **Re-ejecutar el workflow** en GitHub Actions
3. **Si funciona**: El API se desplegará exitosamente
4. **Obtener URL del API**: Estará en los logs del deploy

---

## 📚 Referencias

- [Serverless Framework AWS Credentials](https://www.serverless.com/framework/docs/providers/aws/guide/credentials/)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Lambda Execution Role](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html)

---

**Última actualización**: 20 de Octubre, 2024  
**Estado**: ⚠️ Pendiente configuración de permisos IAM

