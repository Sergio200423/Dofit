# Instrucciones para la configuración del archivo .env

1. Copia el archivo `.env.example` y renómbralo como `.env` en la raíz del proyecto.
2. Abre el nuevo archivo `.env` y reemplaza los valores de ejemplo por los datos reales de tu base de datos Supabase (o la que vayas a usar).
3. Guarda el archivo. ¡Listo! Ahora tu proyecto podrá conectarse a la base de datos correctamente.

Ejemplo:
```
DB_NAME=postgres
DB_USER=usuario_real
DB_PASSWORD=contraseña_real
DB_HOST=host_real.supabase.com
DB_PORT=6543
```

> **Nota:** El archivo `.env` nunca debe subirse al repositorio. Solo comparte `.env.example` para que otros sepan qué variables configurar.
