# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://fastapi_user:123456@localhost:3336/fastapi_tasks_db_dev"
)

# Obtener el valor para 'echo' de las variables de entorno
# Se convierte a booleano. Por ejemplo, "True" se convierte a True.
# Cualquier otra cosa (incluyendo None) se considera False.
SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False").lower() in ('true', '1', 't')


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=SQLALCHEMY_ECHO # Ahora lee de la variable de entorno
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()