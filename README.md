# 🚀 API de Tareas con Autenticación JWT (FastAPI & SQLAlchemy)

¡Bienvenido al proyecto de la API de Tareas con Autenticación! Este proyecto es una aplicación web backend construida con **FastAPI**, **SQLAlchemy** (con un motor de base de datos **MariaDB/MySQL**), y un sistema de autenticación basado en **JSON Web Tokens (JWT)**. Su objetivo principal es proporcionar una API robusta para gestionar tareas (conocidas como "ToDos") y ofrecer un sistema de usuarios seguro.

Este proyecto ha sido diseñado pensando en la modularidad y las buenas prácticas, sirviendo como una excelente base para aprender y desarrollar aplicaciones web con Python.

## ✨ Características Principales

* **Gestión de Tareas (CRUD):**
    * Crear nuevas tareas.
    * Listar todas las tareas (o filtrar por usuario, una vez implementado).
    * Obtener detalles de una tarea específica por ID.
    * Actualizar una tarea existente.
    * Marcar una tarea como completada.
    * Eliminar una tarea.
* **Autenticación y Autorización JWT:**
    * **Registro de Usuarios:** Permite a nuevos usuarios crear una cuenta con un nombre de usuario y contraseña segura (hasheada con Bcrypt).
    * **Inicio de Sesión (Login):** Los usuarios pueden autenticarse para obtener un token de acceso JWT.
    * **Protección de Endpoints:** Los endpoints de gestión de tareas están protegidos, requiriendo un token JWT válido para su acceso.
    * **Manejo de Excepciones de Autenticación:** Proporciona mensajes de error específicos para tokens expirados y genéricos para otros fallos de validación, mejorando la experiencia del desarrollador y la seguridad.
* **Base de Datos Relacional:**
    * Utiliza **SQLAlchemy ORM** para interactuar con una base de datos **MariaDB/MySQL**.
    * Modelos de datos definidos para `User` (Usuario) y `Task` (Tarea).
    * Configuración de la base de datos modular y configurable mediante variables de entorno.
* **Diseño Modular:**
    * Código organizado en módulos lógicos (`database`, `models`, `schemas`, `crud`, `security`, `routers`).
    * Uso de `APIRouter` de FastAPI para modularizar las rutas de la API (autenticación y tareas).
* **Validación de Datos:**
    * Emplea **Pydantic** para una validación robusta de los datos de entrada y salida, asegurando la integridad de la información.
* **Documentación Interactiva (Swagger UI / ReDoc):**
    * FastAPI genera automáticamente documentación interactiva de la API (Swagger UI en `/docs` y ReDoc en `/redoc`), facilitando la prueba y el uso de los endpoints.

## 🛠️ Tecnologías Utilizadas

* **Backend Framework:** FastAPI
* **Base de Datos:** MariaDB / MySQL
* **ORM:** SQLAlchemy
* **Hashing de Contraseñas:** `passlib` (con Bcrypt)
* **JSON Web Tokens (JWT):** `python-jose`
* **Manejo de Variables de Entorno:** `python-dotenv`
* **Conector MySQL para Python:** `pymysql`
* **Servidor ASGI:** Uvicorn

## 🚀 Cómo Empezar

Sigue estos pasos para poner en marcha el proyecto en tu entorno local.

### 📋 Prerrequisitos

* **Python 3.8+:** Asegúrate de tener Python instalado.
* **pip:** El gestor de paquetes de Python.
* **MariaDB/MySQL:** Debes tener una instancia de MariaDB o MySQL en ejecución y accesible.

    * **Crear Base de Datos y Usuario (Ejemplo para MySQL/MariaDB):**
        Conéctate a tu servidor MySQL/MariaDB (ej. `mysql -u root -p`) y ejecuta los siguientes comandos para crear una base de datos y un usuario dedicado:
        ```sql
        CREATE DATABASE fastapi_tasks_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        CREATE USER 'fastapi_user'@'localhost' IDENTIFIED BY '123456';
        GRANT ALL PRIVILEGES ON fastapi_tasks_db.* TO 'fastapi_user'@'localhost';
        FLUSH PRIVILEGES;
        ```
        (Asegúrate de cambiar `123456` por una contraseña más segura en un entorno real y `localhost` si tu DB no está en la misma máquina).

### ⚙️ Configuración del Entorno

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/tu_usuario/tu_repositorio.git](https://github.com/tu_usuario/tu_repositorio.git)
    cd tu_repositorio
    ```

2.  **Crea y activa un entorno virtual:**
    Es una buena práctica aislar las dependencias de tu proyecto.
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt # Si tienes un requirements.txt
    # O instala manualmente:
    pip install fastapi "uvicorn[standard]" sqlalchemy "passlib[bcrypt]" "python-jose[cryptography]" python-dotenv pymysql
    ```
    *(**Nota:** Se recomienda crear un `requirements.txt` ejecutando `pip freeze > requirements.txt` después de instalar todas las dependencias.)*

4.  **Crea el archivo `.env`:**
    Crea un archivo llamado `.env` en la raíz de tu proyecto (al mismo nivel que `main.py` o la carpeta `app`). Este archivo contendrá tus variables de entorno sensibles.

    ```dotenv
    # .env
    SECRET_KEY="tu_clave_secreta_jwt_larga_y_aleatoria"
    DATABASE_URL="mysql+pymysql://fastapi_user:123456@localhost:3336/fastapi_tasks_db"
    SQLALCHEMY_ECHO=True # Cambia a False para producción
    ```
    * **`SECRET_KEY`**: Genera una cadena alfanumérica larga y aleatoria. Puedes usar `openssl rand -hex 32` en tu terminal o `import secrets; secrets.token_hex(32)` en Python.
    * **`DATABASE_URL`**: Asegúrate de que esta URL coincida con las credenciales y el puerto de tu base de datos MariaDB/MySQL. El puerto `3336` es solo un ejemplo; el puerto por defecto de MySQL/MariaDB es `3306`.
    * **`SQLALCHEMY_ECHO`**: `True` para ver las sentencias SQL en la consola durante el desarrollo; `False` para no verlas en producción.

    **⚠️ ¡Importante! Asegúrate de que tu `.gitignore` incluya `.env` para no subir este archivo sensible a tu repositorio público.**

5.  **Crea las tablas de la base de datos:**
    Ejecuta el script `create_db_tables.py` para generar las tablas `users` y `tasks` en tu base de datos.
    ```bash
    python create_db_tables.py
    ```
    Deberías ver mensajes en la consola indicando que las tablas se están creando.

### ▶️ Ejecutar la Aplicación

Una vez que tengas todas las dependencias instaladas y el `.env` configurado, puedes iniciar el servidor FastAPI:

```bash
uvicorn app.main:app --reload