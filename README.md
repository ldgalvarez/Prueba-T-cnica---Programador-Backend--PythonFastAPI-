# TODOs API – FastAPI + PostgreSQL

Backend técnico para gestión de tareas con **FastAPI**, **SQLAlchemy 2.0 (async)**, **JWT**, **Alembic**, **Docker Compose**, **tests** y **logging**.

## 🚀 Características

- **Autenticación JWT**: Registro e inicio de sesión de usuarios.
- **CRUD de Tareas**: Crear, listar, obtener, actualizar y eliminar tareas.
- **Aislamiento de Datos**: Cada usuario solo puede acceder a sus propias tareas.
- **Búsqueda y Filtros**: Filtrar tareas por estado y búsqueda de texto.
- **Paginación**: Listado de tareas con paginación.
- **Base de Datos PostgreSQL**: Con SQLAlchemy 2.0 en modo asíncrono.
- **Migraciones con Alembic**: Control de versiones de la base de datos.
- **Docker Compose**: Facilita el despliegue de la aplicación y PostgreSQL.
- **Manejo de Errores**: Respuestas de error consistentes y logging con Loguru.
- **Testing**: Tests con Pytest y httpx AsyncClient.
- **Validación de Datos**: Con Pydantic v2.

## 🏗️ Estructura del Proyecto

```
todos-fastapi/
├── alembic/                          # Migraciones de la base de datos
│   ├── versions/                     # Versiones de las migraciones
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── api/                          # Endpoints de la API
│   │   ├── routes/                   # Routers
│   │   │   ├── auth.py               # Autenticación
│   │   │   └── tasks.py              # Tareas
│   │   ├── deps.py                   # Dependencias (como la autenticación)
│   │   └── errors.py                 # Manejo de errores
│   ├── core/                         # Configuración y seguridad
│   │   ├── config.py                 # Variables de entorno
│   │   └── security.py               # Utilidades de seguridad (JWT, contraseñas)
│   ├── db/                           # Base de datos
│   │   ├── base.py                   # Clase base de los modelos
│   │   ├── session.py                # Sesión de la base de datos
│   │   └── base_class.py             # Clase base para modelos (opcional)
│   ├── models/                       # Modelos de la base de datos
│   │   ├── user.py                   # Modelo de usuario
│   │   └── task.py                   # Modelo de tarea
│   ├── schemas/                      # Esquemas de Pydantic
│   │   ├── user.py                   # Esquemas de usuario
│   │   ├── token.py                  # Esquemas de token
│   │   └── task.py                   # Esquemas de tarea
│   └── main.py                       # Aplicación FastAPI
├── tests/                            # Tests
│   ├── conftest.py                   # Configuración de tests
│   └── test_auth_and_tasks.py        # Tests de autenticación y tareas
├── .env.example                      # Variables de entorno de ejemplo
├── .env                              # Variables de entorno (no versionado)
├── alembic.ini                       # Configuración de Alembic
├── docker-compose.yml                # Docker Compose
├── Dockerfile                        # Dockerfile para la aplicación
├── pyproject.toml                    # Dependencias y configuración de proyecto
└── README.md                         # Este archivo
```

## ⚙️ Configuración Rápida (Docker)

### Prerrequisitos
- Docker y Docker Compose instalados.

### Pasos
1. Clona el repositorio.
2. Copia el archivo de entorno de ejemplo:
   ```bash
   cp .env.example .env
   ```
3. Ajusta las variables de entorno en `.env` si es necesario.
4. Construye y ejecuta los contenedores:
   ```bash
   docker compose up --build
   ```
5. La API estará disponible en `http://localhost:8000`.
6. La documentación interactiva (Swagger UI) estará en `http://localhost:8000/docs`.

## 🧪 Configuración Rápida (Local sin Docker)

### Prerrequisitos
- Python 3.11+ instalado.
- PostgreSQL ejecutándose localmente.

### Pasos
1. Clona el repositorio.
2. Crea un entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # o
   .venv\Scripts\activate     # Windows
   ```
3. Instala las dependencias:
   ```bash
   pip install -e .
   ```
4. Copia y configura las variables de entorno:
   ```bash
   cp .env.example .env
   # Edita .env con tus valores
   ```
5. Ejecuta las migraciones de la base de datos:
   ```bash
   alembic upgrade head
   ```
6. Inicia el servidor de desarrollo:
   ```bash
   uvicorn app.main:app --reload
   ```
7. La API estará disponible en `http://localhost:8000`.

## 🔐 Autenticación

### Registro de Usuario
- **Endpoint**: `POST /auth/signup`
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Respuesta**:
  ```json
  {
    "access_token": "jwt_token",
    "token_type": "bearer"
  }
  ```

### Inicio de Sesión
- **Endpoint**: `POST /auth/login`
- **Body**: mismo que el registro.
- **Respuesta**: mismo que el registro.

### Uso del Token
Incluye el token en las solicitudes protegidas:
```
Authorization: Bearer <token>
```

## 📚 Endpoints de Tareas

### Crear una Tarea
- **Endpoint**: `POST /tasks`
- **Headers**: `Authorization: Bearer <token>`
- **Body**:
  ```json
  {
    "title": "Mi tarea",
    "description": "Descripción de la tarea",
    "status": "pending"  // opcional, por defecto "pending"
  }
  ```
- **Respuesta**: Tarea creada.

### Listar Tareas
- **Endpoint**: `GET /tasks`
- **Headers**: `Authorization: Bearer <token>`
- **Query Parameters**:
  - `limit` (opcional, por defecto 50, máximo 200): Número de tareas por página.
  - `offset` (opcional, por defecto 0): Desplazamiento para paginación.
  - `status` (opcional): Filtrar por estado (`pending` o `completed`).
  - `search` (opcional): Búsqueda de texto en título y descripción.
- **Respuesta**: Lista de tareas.

### Obtener una Tarea
- **Endpoint**: `GET /tasks/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Respuesta**: Tarea solicitada.

### Actualizar una Tarea
- **Endpoint**: `PUT /tasks/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Body** (campos opcionales):
  ```json
  {
    "title": "Nuevo título",
    "description": "Nueva descripción",
    "status": "completed"
  }
  ```
- **Respuesta**: Tarea actualizada.

### Eliminar una Tarea
- **Endpoint**: `DELETE /tasks/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Respuesta**: 204 No Content.

## 🧱 Migraciones de Base de Datos

### Crear una Nueva Migración
```bash
alembic revision --autogenerate -m "descripción de los cambios"
```

### Aplicar Migraciones
```bash
alembic upgrade head
```

### Revertir Migración
```bash
alembic downgrade -1
```

## 🧰 Tests

Ejecuta los tests con:
```bash
pytest
```

## 🔧 Variables de Entorno

El archivo `.env` debe contener:

```bash
# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=app
POSTGRES_PASSWORD=secret
POSTGRES_DB=todos
DATABASE_URL=postgresql+asyncpg://app:secret@localhost:5432/todos

# JWT
JWT_SECRET=change-me-in-prod
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=60

# App
APP_ENV=dev
LOG_LEVEL=INFO
```

## 📝 Notas de Escalabilidad

- **Conexiones Asíncronas**: Uso de asyncpg y SQLAlchemy async para manejar múltiples conexiones eficientemente.
- **Índices**: Índices en `user_id`, `status` y `created_at` para optimizar consultas.
- **Paginación**: Obligatoria en listados para evitar sobrecarga.
- **Manejo de Errores**: Respuestas idempotentes y códigos de error adecuados (404, 403, etc.).
- **Producción**: Configurable para producción con Gunicorn y Uvicorn Workers.

## 🚀 Despliegue en Producción

Para producción, se recomienda:
- Usar un servidor ASGI como Gunicorn con Uvicorn Workers.
- Configurar variables de entorno seguras.
- Usar un reverse proxy como Nginx.
- Configurar SSL/TLS.

Ejemplo de comando para producción:
```bash
gunicorn -k uvicorn.workers.UvicornWorker -w 4 app.main:app
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.