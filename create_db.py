from database import Base, engine, get_db
import os
import importlib
import sys

# Directorio de modelos
models_dir = "models"

def create_tables():
    try:
        # Importar todos los modelos del directorio 'models'
        for file in os.listdir(models_dir):
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]  # Quitar la extensión .py
                importlib.import_module(f"models.{module_name}")
        
        # Crear las tablas
        Base.metadata.create_all(bind=engine)
        print("✅ Base de datos y tablas creadas correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al crear las tablas: {e}")
        return False

if __name__ == "__main__":
    create_tables()
