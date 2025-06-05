# 🚀 API de Tareas con Autenticación JWT (FastAPI & SQLAlchemy)

¡Bienvenido al proyecto de la API de Tareas con Autenticación! Este proyecto es una aplicación web backend construida con **FastAPI**, **SQLAlchemy** (con un motor de base de datos **MariaDB/MySQL**), y un sistema de autenticación basado en **JSON Web Tokens (JWT)**. Su objetivo principal es proporcionar una API robusta para gestionar tareas (conocidas como "ToDos") y ofrecer un sistema de usuarios seguro.

Este proyecto ha sido diseñado pensando en la modularidad y las buenas prácticas, sirviendo como una excelente base para aprender y desarrollar aplicaciones web con Python.

## ✨ Características Principales

* **Gestión de Tareas (CRUD):**
    * Crear nuevas tareas.
    * Listar todas las tareas.
    * Obtener detalles de una tarea específica por ID.
    * Actualizar una tarea existente.
    * Marcar una tarea como completada.
    * Eliminar una tarea.
* **Autenticación y Autorización JWT:**
    * **Registro de Usuarios:** Permite a nuevos usuarios crear una cuenta con un nombre de usuario y contraseña segura (hasheada con Bcrypt).
    * **Inicio de Sesión (Login):** Los usuarios pueden autenticarse para obtener un token de acceso JWT.
    * **Protección de Endpoints:** Los endpoints de gestión de tareas están protegidos, requiriendo un token JWT válido para su acceso.
    * **Manejo de Excepciones de Autenticación:** Proporciona mensajes de error claros para credenciales inválidas o tokens ausentes/expirados.
    * **Autorización por Propietario (Owner-based Authorization):** Cada tarea está vinculada a un usuario (`owner_id`). Solo el usuario propietario de una tarea puede verla, actualizarla o eliminarla, garantizando la privacidad y seguridad de los datos.

## 🛠️ Tecnologías Utilizadas

* **Python 3.x**
* **FastAPI:** Framework web moderno y rápido para construir APIs.
* **SQLAlchemy:** ORM (Object Relational Mapper) para interactuar con la base de datos.
* **Pydantic:** Para la validación de datos y la definición de esquemas.
* **PyJWT:** Para la creación y verificación de JSON Web Tokens.
* **Passlib:** Para el hashing seguro de contraseñas (Bcrypt).
* **Uvicorn:** Servidor ASGI para ejecutar la aplicación FastAPI.
* **PyMySQL:** Conector de MySQL/MariaDB para SQLAlchemy.
* **MariaDB/MySQL:** Sistema de gestión de base de datos relacional.

## 🚀 Pasos para Ejecutar el Proyecto

Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local.

1.  **Clonar el Repositorio (o crear la estructura de archivos):**
    Si no tienes un repositorio, asegúrate de tener la siguiente estructura de carpetas:

    ```
    .
    ├── app/
    │   ├── __init__.py
    │   ├── crud.py
    │   ├── database.py
    │   ├── dependencies.py
    │   ├── main.py
    │   ├── models.py
    │   ├── schemas.py
    │   └── security.py
    ├── create_db_tables.py
    ├── .env
    └── .gitignore
    ```

2.  **Crear y Activar un Entorno Virtual:**
    Es una buena práctica usar entornos virtuales para aislar las dependencias del proyecto.

    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instalar las Dependencias:**
    Instala todas las librerías necesarias.

    ```bash
    pip install fastapi uvicorn sqlalchemy pymysql python-jose[cryptography] passlib[bcrypt] python-dotenv
    ```

4.  **Configurar la Base de Datos y Variables de Entorno:**
    * **Crear una base de datos MariaDB/MySQL:** Asegúrate de tener una base de datos vacía llamada `fastapi_tasks_db` y un usuario con permisos para ella (ej. `fastapi_user` con contraseña `123456`).
    * **Archivo `.env`:** Crea un archivo `.env` en la raíz de tu proyecto (al mismo nivel que `main.py` o la carpeta `app`). Este archivo contendrá tus variables de entorno sensibles.

    ```dotenv
    # .env
    SECRET_KEY="tu_clave_secreta_jwt_larga_y_aleatoria"
    DATABASE_URL="mysql+pymysql://fastapi_user:123456@localhost:3336/fastapi_tasks_db"
    SQLALCHEMY_ECHO=False # Cambia a True para ver las sentencias SQL en consola (útil para depuración)
    ```
    * **`SECRET_KEY`**: Genera una cadena alfanumérica larga y aleatoria. Puedes usar `openssl rand -hex 32` en tu terminal o `import secrets; secrets.token_hex(32)` en Python.
    * **`DATABASE_URL`**: Asegúrate de que esta URL coincida con las credenciales y el puerto de tu base de datos MariaDB/MySQL. El puerto `3336` es solo un ejemplo; el puerto por defecto de MySQL/MariaDB es `3306`.
    * **`SQLALCHEMY_ECHO`**: `True` para ver las sentencias SQL en la consola durante el desarrollo; `False` para no verlas en producción.

    **⚠️ ¡Importante! Asegúrate de que tu `.gitignore` incluya `.env` para no subir este archivo sensible a tu repositorio público.**

5.  **Crear/Actualizar las tablas de la base de datos:**
    Ejecuta el script `create_db_tables.py` para generar o actualizar las tablas `users` y `tasks` en tu base de datos.
    **Si ya tenías tablas y has añadido nuevas columnas (como `owner_id`), es crucial que antes de este paso, elimines las tablas `users` y `tasks` de tu base de datos manualmente (ej. `DROP TABLE users; DROP TABLE tasks;` en tu cliente SQL) para que SQLAlchemy las cree con el esquema actualizado.**

    ```bash
    python create_db_tables.py
    ```

6.  **Ejecutar la Aplicación FastAPI:**
    Inicia el servidor Uvicorn. El flag `--reload` es útil para el desarrollo, ya que el servidor se reiniciará automáticamente con cada cambio de código.

    ```bash
    uvicorn app.main:app --reload
    ```
    La API estará disponible en `http://127.0.0.1:8000`. La documentación interactiva de Swagger UI estará en `http://127.0.0.1:8000/docs`.

## 🧪 Pruebas de Funcionalidad y Seguridad

Una vez que la API está en funcionamiento, puedes probarla utilizando la interfaz de Swagger UI (`/docs`).

1.  **Registrar un Usuario:**
    * Ve a `http://127.0.0.1:8000/docs`.
    * Expande el endpoint `POST /auth/register`.
    * Haz clic en "Try it out" e introduce un `username` y `password`.
    * Haz clic en "Execute". Deberías ver un `201 Created` y los datos del nuevo usuario.

2.  **Iniciar Sesión y Obtener un Token:**
    * Expande el endpoint `POST /auth/token`.
    * Haz clic en "Try it out".
    * Introduce el `username` y `password` del usuario registrado.
    * Haz clic en "Execute". Deberías recibir un `200 OK` y un `access_token` en la respuesta.

3.  **Autorizar Solicitudes en Swagger UI:**
    * Copia el `access_token` (sin la parte "Bearer ").
    * Haz clic en el botón verde "Authorize" en la parte superior derecha de la página.
    * Pega tu token en el campo `Value` (debe ser `Bearer <tu_token>`).
    * Haz clic en "Authorize" y luego en "Close".

4.  **Crear Tareas (con el Usuario Autenticado):**
    * Expande el endpoint `POST /tasks/`.
    * Haz clic en "Try it out" e introduce un `title` y `description` para tu tarea.
    * Haz clic en "Execute". Deberías ver un `201 Created` y la tarea creada, con un `owner_id` que coincide con el ID de tu usuario.
    * **(Verificación en DB):** Puedes conectar a tu base de datos (`SELECT * FROM tasks;`) para confirmar que el `owner_id` se ha asignado correctamente a la tarea.

5.  **Obtener Tareas del Usuario Actual:**
    * Expande el endpoint `GET /tasks/`.
    * Haz clic en "Try it out" y luego en "Execute".
    * Deberías ver solo las tareas que ha creado el usuario cuyo token está actualmente autorizado.

6.  **Probar la Autorización por Propietario (CRUCIAL):**
    * **Crea un SEGUNDO USUARIO** y repite los pasos 1, 2 y 3 para obtener su token y autorizarlo en Swagger UI.
    * **Con el token del SEGUNDO USUARIO activo:**
        * Intenta hacer un `GET /tasks/{task_id}` usando el `id` de una tarea creada por el **PRIMER USUARIO** (ej. `task_id=1`).
        * **Resultado esperado:** Deberías recibir un `404 Not Found` (o `403 Forbidden` si la lógica fuera más estricta), confirmando que `user2` no puede ver la tarea de `user1`.
        * Intenta hacer un `PUT /tasks/{task_id}` o `DELETE /tasks/{task_id}` con el `id` de una tarea del **PRIMER USUARIO**.
        * **Resultado esperado:** Deberías recibir un `404 Not Found` (o `403 Forbidden`), confirmando que `user2` no puede modificar/eliminar la tarea de `user1`.
    * **Crea tareas con el SEGUNDO USUARIO:** Ahora, con el token del segundo usuario, crea nuevas tareas.
    * **Obtén tareas del SEGUNDO USUARIO:** Haz `GET /tasks/` con el token del segundo usuario y deberías ver solo las tareas que él creó.

Si todas estas pruebas son exitosas, significa que tu API es robusta y segura, con una correcta gestión de usuarios, autenticación y autorización de recursos.