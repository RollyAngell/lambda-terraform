
## ¿Qué hace este proyecto?

- Crea un rol IAM para Lambda con permisos de acceso total a S3.
- Despliega una función Lambda en Python 3.11 que:
  - Lee un archivo CSV de ventas desde S3.
  - Calcula el promedio de ventas por región.
  - Guarda el resumen en otro archivo CSV en el mismo bucket.

## Código de la función Lambda

El código fuente está en `lambda/lambda_function.py`.  
Empaqueta este archivo como `lambda.zip` para desplegarlo.

## Despliegue con Terraform

1. **Inicializa Terraform:**
   ```sh
   terraform init
   ```

2. **Aplica la infraestructura:**
   ```sh
   terraform apply
   ```

## Automatización con GitHub Actions

Cada vez que hagas un push a la rama `main`, el workflow `.github/workflows/terraform.yml` ejecutará automáticamente los comandos de Terraform para desplegar los cambios.

### Configuración de secretos

Debes agregar los siguientes secretos en tu repositorio de GitHub:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

Desde **Settings > Secrets and variables > Actions**.

## Notas importantes

- **No subas los archivos `.tfstate` ni `lambda.zip` a GitHub.** Ya están en el `.gitignore`.
- El archivo `variables.tf` está vacío, pero puedes usarlo para definir variables personalizadas.
- El bucket S3 y los nombres de archivos se configuran en las variables de entorno de la Lambda (ver `main.tf`).

## Autor

Rolly Angell