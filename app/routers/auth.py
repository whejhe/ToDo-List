# app/routers/auth.py

from datetime import timedelta

from ..database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # Para el formulario de login (username y password)
from sqlalchemy.orm import Session

from .. import schemas, crud, database, security # Importa los nuevos módulos
from ..security import create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES

# Crea una instancia de APIRouter para la autenticación
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"], # Etiqueta para la documentación
)


# --- Endpoint de Registro ---
@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario en la base de datos.
    Verifica si el nombre de usuario ya existe.
    """
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        # Si el usuario ya existe, devuelve un error 400 Bad Request
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado"
        )
    # Crea el usuario usando la función CRUD
    return crud.create_user(db=db, user=user)

# --- Endpoint de Login y Obtención de Token ---
# Usa OAuth2PasswordRequestForm para manejar la entrada de username y password del formulario
@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Inicia sesión y obtiene un token de acceso JWT.
    Recibe el nombre de usuario y la contraseña en un formulario.
    """
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        # Si las credenciales son incorrectas, devuelve un error 401 Unauthorized
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}, # Indica que se espera un token Bearer
        )
    # Crea el token de acceso JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, # "sub" (subject) es la convención para el identificador del usuario
        expires_delta=access_token_expires
    )
    # Retorna el token y su tipo
    return {"access_token": access_token, "token_type": "bearer"}