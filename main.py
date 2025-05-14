from fastapi import FastAPI, Depends
from routers import Usuario, Administrador, Test, Respuestas, Estadisticas, TestEstadistica, Segmentacion, Auth
from fastapi.middleware.cors import CORSMiddleware
import os
from database import Base, engine, get_db
from sqlalchemy.orm import Session
import logging
import sys

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Obtener las URLs permitidas desde variables de entorno o usar valores por defecto
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://frontend-gesex-production.up.railway.app")
DEVELOPMENT_URL = os.getenv("DEVELOPMENT_URL", "http://localhost:5173")
PORT = os.getenv("PORT", "8000")

# Informar sobre la configuración
logger.info(f"FRONTEND_URL: {FRONTEND_URL}")
logger.info(f"DEVELOPMENT_URL: {DEVELOPMENT_URL}")
logger.info(f"PORT: {PORT}")
logger.info(f"DATABASE_URL existe: {os.getenv('DATABASE_URL') is not None}")

@app.on_event("startup")
async def startup_db_client():
    try:
        # Crear las tablas si no existen
        logger.info("Iniciando creación de tablas...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas creadas correctamente")
    except Exception as e:
        logger.error(f"Error al crear las tablas: {e}")
        sys.exit(1)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporalmente permitir todas para diagnóstico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers con manejo de errores
try:
    app.include_router(Usuario.router)
    app.include_router(Administrador.router)
    app.include_router(Test.router)
    app.include_router(Respuestas.router)
    app.include_router(Estadisticas.router)
    app.include_router(TestEstadistica.router)
    app.include_router(Segmentacion.router)
    app.include_router(Auth.router, prefix="/api", tags=["Auth"])
    logger.info("Todos los routers incluidos correctamente")
except Exception as e:
    logger.error(f"Error al incluir los routers: {e}")

@app.get("/")
async def root():
    return {"message": "API de GESEX funcionando correctamente"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/debug")
async def debug_info(db: Session = Depends(get_db)):
    """Endpoint para depuración"""
    try:
        # Obtener información de la conexión a la BD
        db_info = {
            "connected": True,
            "tables": [str(table) for table in Base.metadata.tables]
        }
        return {
            "database": db_info,
            "environment": {k: v for k, v in os.environ.items() if not k.startswith('_')}
        }
    except Exception as e:
        return {"error": str(e)}
