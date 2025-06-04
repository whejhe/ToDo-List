# app/main.py

from fastapi import FastAPI
# Importa ambos routers
from .routers import tasks, auth # ¡Ahora importa 'auth' también!

# Crea la instancia de la aplicación FastAPI
app = FastAPI(
    title="API de Tareas con Autenticación (FastAPI)",
    description="Una API simple para gestionar tareas con operaciones CRUD y autenticación JWT.",
    version="0.1.0",
)

# Incluye ambos routers en la aplicación principal
app.include_router(tasks.router)
app.include_router(auth.router) # ¡Nuevo! Incluye el router de autenticación

# Endpoint raíz (opcional, puedes mantenerlo o eliminarlo)
@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de Tareas con Autenticación JWT!"}