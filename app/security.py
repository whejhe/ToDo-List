# app/security.py

from datetime import datetime, timedelta, timezone
from typing import Optional

# Importamos las excepciones específicas de jose y el módulo jwt
# Modificamos la importación de jose.exceptions
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError # Esta suele ser suficiente y estable

# ¡ESTO ES LO QUE FALTABA! Importar HTTPException y status de FastAPI
from fastapi import HTTPException, status 

from passlib.context import CryptContext 
import os
from dotenv import load_dotenv 

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# --- Configuración de Hashing de Contraseñas ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key_if_not_set_in_env")
ALGORITHM = "HS256" # Algoritmo de hashing para JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # El token expirará en 30 minutos


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña plana coincide con una contraseña hasheada."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashea una contraseña."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crea un token de acceso JWT.
    data: Diccionario con la información a codificar (ej. {"sub": "username"}).
    expires_delta: Opcional, timedelta para la duración del token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """
    Decodifica un token JWT y maneja errores específicos.
    Lanza HTTPException si el token ha expirado,
    de lo contrario devuelve el payload o None si hay otro error JWT.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        # Si el token ha expirado, lanzamos una excepción HTTP con un detalle específico
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Cambiamos la captura de errores. JWTError ya es bastante amplio.
    # Si ExpiredSignatureError no la captura, JWTError general lo hará.
    except JWTError as e: 
        # Para errores de firma o formato, o cualquier otro error JWT
        print(f"DEBUG: Error JWT genérico inesperado: {e}") # Útil para depuración interna
        return None