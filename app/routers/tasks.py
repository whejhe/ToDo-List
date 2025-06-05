# app/routers/tasks.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud, database, models
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    responses={404: {"description": "Not found"}},
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints de Tareas ---

# Operación: Crear Tarea (POST)
@router.post("/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task_route(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # ¡Aquí obtenemos el usuario autenticado!
):
    """
    Crea una nueva tarea asignada al usuario autenticado. Requiere autenticación.
    """
    print(f"Usuario autenticado creando tarea: {current_user.username}")
    # MODIFICACIÓN CLAVE AQUÍ: Pasar el ID del usuario activo
    return crud.create_task(db=db, task=task, owner_id=current_user.id) # <--- ¡Pasamos current_user.id!

# Operación: Obtener Todas las Tareas del Usuario (GET)
@router.get("/", response_model=List[schemas.Task])
def get_tasks_route(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # ¡Añadido!
):
    """
    Obtiene todas las tareas del usuario autenticado. Requiere autenticación.
    """
    print(f"Usuario autenticado obteniendo tareas: {current_user.username}")
    # Filtrar tareas por owner_id
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).offset(skip).limit(limit).all()
    return tasks

# Operación: Obtener Tarea por ID (GET)
@router.get("/{task_id}", response_model=schemas.Task)
def get_task_by_id_route(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # ¡Añadido!
):
    """
    Obtiene una tarea específica por su ID, asegurándose de que pertenezca al usuario autenticado.
    Requiere autenticación.
    """
    print(f"Usuario autenticado obteniendo tarea {task_id}: {current_user.username}")
    # Filtrar por ID de tarea Y owner_id
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return task

# Operación: Actualizar Tarea (PUT)
@router.put("/{task_id}", response_model=schemas.Task)
def update_task_route(
    task_id: int,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # ¡Añadido!
):
    """
    Actualiza una tarea específica por su ID. Requiere autenticación.
    """
    print(f"Usuario autenticado actualizando tarea {task_id}: {current_user.username}")
    # Asegúrate de que la tarea pertenece al usuario actual antes de actualizar
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada o no pertenece a este usuario")
    
    # Actualiza los campos
    db_task.title = task.title
    db_task.description = task.description
    db.commit()
    db.refresh(db_task)
    return db_task

# Operación: Eliminar Tarea (DELETE)
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_route(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # ¡Añadido!
):
    """
    Elimina una tarea específica por su ID. Requiere autenticación.
    """
    print(f"Usuario autenticado eliminando tarea {task_id}: {current_user.username}")
    # Asegúrate de que la tarea pertenece al usuario actual antes de eliminar
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada o no pertenece a este usuario")
    
    db.delete(db_task)
    db.commit()
    return

# Operación: Actualizar Estado de Tarea (PATCH)
@router.patch("/{task_id}/complete", response_model=schemas.Task)
def complete_task_route(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # ¡Añadido!
):
    """
    Marca una tarea como completada por su ID. Requiere autenticación.
    """
    print(f"Usuario autenticado completando tarea {task_id}: {current_user.username}")
    # Asegúrate de que la tarea pertenece al usuario actual antes de marcar como completada
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada o no pertenece a este usuario")
    
    db_task.completed = True
    db.commit()
    db.refresh(db_task)
    return db_task