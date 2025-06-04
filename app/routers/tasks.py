# app/routers/tasks.py

from ..database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Importaciones relativas: ahora también necesitamos `dependencies` y `models`
from .. import schemas, crud, database, models # Asegúrate de importar models si no lo estaba
from ..dependencies import get_current_user # NUEVO: Importa la dependencia de usuario actual

# Crea una instancia de APIRouter
router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    responses={404: {"description": "Not found"}},
)

# Operación: Crear Tarea (POST)
@router.post("/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task_route(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # ¡Añadido!
):
    """
    Crea una nueva tarea. Requiere autenticación.
    """
    # Opcional: Aquí podrías añadir lógica para asociar la tarea con el current_user,
    # por ejemplo, añadiendo un campo user_id a la tabla tasks.
    # Por ahora, solo lo usamos para verificar que el usuario está autenticado.
    print(f"Usuario autenticado creando tarea: {current_user.username}")
    return crud.create_task(db=db, task=task)

# Operación: Leer Todas las Tareas (GET)
@router.get("/", response_model=List[schemas.Task])
def read_tasks_route(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # ¡Añadido!
):
    """
    Obtiene la lista de todas las tareas existentes. Requiere autenticación.
    """
    print(f"Usuario autenticado listando tareas: {current_user.username}")
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks

# Operación: Leer Tarea por ID (GET)
@router.get("/{task_id}", response_model=schemas.Task)
def read_task_route(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # ¡Añadido!
):
    """
    Obtiene una tarea específica por su ID. Requiere autenticación.
    """
    print(f"Usuario autenticado leyendo tarea {task_id}: {current_user.username}")
    task = crud.get_task(db, task_id=task_id)
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
    Actualiza una tarea existente por su ID. Requiere autenticación.
    """
    print(f"Usuario autenticado actualizando tarea {task_id}: {current_user.username}")
    db_task = crud.update_task(db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
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
    deleted = crud.delete_task(db, task_id=task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return

# Operación: Actualizar Estado de Tarea (PATCH)
@router.patch("/{task_id}/complete", response_model=schemas.Task)
def complete_task_route(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # ¡Añadido!
):
    """
    Marca una tarea específica como completada. Requiere autenticación.
    """
    print(f"Usuario autenticado completando tarea {task_id}: {current_user.username}")
    db_task = crud.complete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return db_task