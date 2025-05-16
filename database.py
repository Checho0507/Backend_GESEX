from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging

# Configurar logging
logger = logging.getLogger(__name__)

# Configuración para PostgreSQL
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "RDQrUJGkYUnuJfasWZIaCaJQSgbJXLMw")
DB_HOST = os.getenv("DB_HOST", "postgres-2foj.railway.internal")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "railway")

# Crear la URL de la base de datos PostgreSQL
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

logger.info("Usando PostgreSQL con la URL: %s", SQLALCHEMY_DATABASE_URL)

try:
    # Usar PostgreSQL con opciones de conexión optimizadas
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
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
