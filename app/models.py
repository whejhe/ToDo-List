# app/models.py

from sqlalchemy import Column, Integer, String, Boolean
# from sqlalchemy.orm import relationship 
# Si no se usa, se puede quitar

from .database import Base

# --- Modelo de Tarea (ya existente) ---
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(1000), nullable=True)
    completed = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"

# --- NUEVO: Modelo de Usuario ---
class User(Base):
    __tablename__ = "users" # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True) # Nombre de usuario único e indexado
    hashed_password = Column(String(255)) # Contraseña hasheada (nunca en texto plano)
    is_active = Column(Boolean, default=True) # Para activar/desactivar usuarios

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', is_active={self.is_active})>"