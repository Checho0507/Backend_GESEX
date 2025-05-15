from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging

# Configurar logging
logger = logging.getLogger(__name__)

# Determinar si estamos en entorno de producción
# Railway establece automáticamente DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", None)
RAILWAY_ENVIRONMENT = os.getenv("RAILWAY_ENVIRONMENT", None)

logger.info(f"Configurando base de datos. En Railway: {RAILWAY_ENVIRONMENT is not None}")

# Si DATABASE_URL está disponible, usaremos PostgreSQL
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    # Railway usa postgres://, pero SQLAlchemy requiere postgresql://
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    logger.info("URL de base de datos convertida de postgres:// a postgresql://")

# Si no hay DATABASE_URL, usar SQLite local
if not DATABASE_URL:
    logger.warning("No se encontró DATABASE_URL. Usando SQLite local.")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
    # Conectar con SQLite (check_same_thread=False es necesario para SQLite en modo multihilo)
    try:
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        )
        logger.info("Motor de base de datos SQLite inicializado correctamente.")
    except Exception as e:
        logger.error(f"Error al configurar el motor de base de datos SQLite: {e}")
        raise
else:
    logger.info("Usando PostgreSQL con la URL proporcionada.")
    try:
        # Usar PostgreSQL en producción con opciones de conexión optimizadas
        engine = create_engine(
            DATABASE_URL,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=300,
        )
        logger.info("Motor de base de datos PostgreSQL inicializado correctamente.")
    except Exception as e:
        logger.error(f"Error al configurar el motor de base de datos PostgreSQL: {e}")
        raise

# Crear una sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Función para obtener DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
