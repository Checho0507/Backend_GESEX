from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión para SQLite (archivo local llamado database.db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

# Conectar con SQLite (check_same_thread=False es necesario para SQLite en modo multihilo)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crear una sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()
