# init_db.py
from database import Base, engine
import importlib
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Inicializa la base de datos creando todas las tablas necesarias"""
    try:
        # Importar dinámicamente todos los modelos para que estén disponibles para el create_all
        model_files = []
        for root, dirs, files in os.walk("models"):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    module_path = os.path.join(root, file).replace(os.path.sep, ".")[:-3]
                    model_files.append(module_path)
        
        logger.info(f"Archivos de modelos encontrados: {model_files}")
        
        # Importar todos los módulos de modelos
        for module_path in model_files:
            try:
                importlib.import_module(module_path)
                logger.info(f"Módulo importado: {module_path}")
            except Exception as e:
                logger.error(f"Error al importar {module_path}: {e}")
        
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"❌ Error al inicializar la base de datos: {e}")
        raise

if __name__ == "__main__":
    init_database()
