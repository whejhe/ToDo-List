# app/schemas.py

from pydantic import BaseModel, Field
from typing import Optional

# --- Modelos de Tarea (ya existentes) ---
class TaskBase(BaseModel):
    title: str = Field(..., example="Aprender FastAPI")
    description: Optional[str] = Field(None, example="Estudiar los conceptos de FastAPI y CRUD")

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    completed: bool = False

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Comprar leche",
                "description": "Leche desnatada",
                "completed": False
            }
        }

# --- NUEVO: Modelos de Usuario ---

class UserBase(BaseModel):
    """
    Esquema base para un usuario.
    """
    username: str = Field(..., min_length=3, max_length=50, example="john_doe")

class UserCreate(UserBase):
    """
    Esquema para crear un nuevo usuario (registro).
    Incluye la contraseña.
    """
    password: str = Field(..., min_length=6) # Contraseña en texto plano para el registro

class User(UserBase):
    """
    Esquema para la representación completa de un usuario (salida de API).
    No incluye la contraseña, pero sí el ID y estado.
    """
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True # Necesario para convertir el modelo SQLAlchemy a Pydantic
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "jane_doe",
                "is_active": True
            }
        }

class Token(BaseModel):
    """
    Esquema para la respuesta del token JWT.
    """
    access_token: str
    token_type: str = "bearer" # Siempre "bearer" para tokens de portador

class TokenData(BaseModel):
    """
    Esquema para los datos decodificados del token JWT.
    """
    username: Optional[str] = None