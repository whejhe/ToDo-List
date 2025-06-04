# app/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from . import crud, schemas, database, security # Importa todos los módulos necesarios

# Define el esquema de seguridad OAuth2 con un punto de token
# Esto le dice a FastAPI dónde esperar el token y cómo se llama el endpoint de login.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Dependencia para obtener la sesión de base de datos (copia)
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependencia que verifica el token JWT, decodifica el usuario y lo retorna.
    Si el token es inválido o el usuario no existe, lanza HTTPException.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica el token usando la función de seguridad
        payload = security.decode_access_token(token)
        if payload is None: # Si el token no pudo ser decodificado (ej. JWTError)
            raise credentials_exception

        username: str = payload.get("sub") # Obtiene el username del payload
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError: # Atrapa errores específicos de JWT
        raise credentials_exception

    # Busca el usuario en la base de datos
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user