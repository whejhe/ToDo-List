# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

# --- Hashing de Contraseñas ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# --- Funciones CRUD para Tareas (ya existentes) ---
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

# MODIFICACIÓN CLAVE AQUÍ: Aceptar owner_id
def create_task(db: Session, task: schemas.TaskCreate, owner_id: int): # <--- ¡Añadimos owner_id!
    """
    Crea una nueva tarea en la base de datos, asignándola al usuario especificado.
    """
    # Asignamos el owner_id al modelo de tarea
    db_task = models.Task(title=task.title, description=task.description, owner_id=owner_id) # <--- ¡Asignamos owner_id!
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: schemas.TaskCreate):
    db_task = get_task(db, task_id)
    if db_task:
        db_task.title = task.title
        db_task.description = task.description
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False

def complete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        db_task.completed = True
        db.commit()
        db.refresh(db_task)
    return db_task


# --- NUEVO: Funciones CRUD para Usuarios ---

def get_user_by_username(db: Session, username: str):
    """Obtiene un usuario por su nombre de usuario."""
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Crea un nuevo usuario con la contraseña hasheada."""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user