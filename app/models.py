# app/models.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey # Asegúrate de importar ForeignKey
from sqlalchemy.orm import relationship # Asegúrate de importar relationship

from .database import Base

# --- Modelo de Tarea (ya existente) ---
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(1000), nullable=True)
    completed = Column(Boolean, default=False)
    # --- NUEVO: Columna para la clave foránea ---
    owner_id = Column(Integer, ForeignKey("users.id")) # Esto enlaza con la tabla 'users' y la columna 'id'

    # --- NUEVO: Relación ORM ---
    # Esto permite acceder al usuario asociado a una tarea (ej. task.owner)
    owner = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"

# --- NUEVO: Modelo de Usuario ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

    # --- NUEVO: Relación ORM ---
    # Esto permite acceder a las tareas de un usuario (ej. user.tasks)
    tasks = relationship("Task", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', is_active={self.is_active})>"