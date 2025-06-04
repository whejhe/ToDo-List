# create_db_tables.py (en la raíz del proyecto)

from app.database import engine, Base
import app.models # Asegúrate de que este import esté presente para que Base.metadata "vea" todos los modelos

print("Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine) # Esto creará TODAS las tablas que heredan de Base
print("Tablas creadas exitosamente.")