from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Determinar si estamos en entorno de producción
# Railway establece automáticamente DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", None)

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    # Railway usa postgres://, pero SQLAlchemy requiere postgresql://
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Si no hay DATABASE_URL, usar SQLite local
if not DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
    # Conectar con SQLite (check_same_thread=False es necesario para SQLite en modo multihilo)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # Usar PostgreSQL en producción
    engine = create_engine(DATABASE_URL)

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
