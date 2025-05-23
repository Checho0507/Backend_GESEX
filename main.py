from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import logging
import sys

from database import Base, engine, get_db
from routers import (
    Usuario, Administrador, Test, Respuestas,
    Estadisticas, TestEstadistica, Segmentacion, Auth
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI()

# Variables de entorno para CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://frontendgesex-production.up.railway.app")
DEVELOPMENT_URL = os.getenv("DEVELOPMENT_URL", "http://localhost:5173")

# Mostrar configuración cargada
logger.info(f"FRONTEND_URL: {FRONTEND_URL}")
logger.info(f"DEVELOPMENT_URL: {DEVELOPMENT_URL}")
logger.info(f"DATABASE_URL exists: {os.getenv('DATABASE_URL') is not None}")
logger.info(f"Entorno de Railway: {os.getenv('RAILWAY_ENVIRONMENT', 'no definido')}")
logger.info(f"Puerto asignado: {os.getenv('PORT', '8000')}")

# Middleware de CORS - configuración más segura para producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, DEVELOPMENT_URL, "https://*.railway.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Crear tablas al iniciar
@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Creando tablas de la base de datos...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas creadas exitosamente.")
    except Exception as e:
        logger.error(f"Error al crear las tablas: {e}")
        # No salir en caso de error, Railway podría reintentar
        # sys.exit(1)

# Incluir routers
try:
    app.include_router(Usuario.router)
    app.include_router(Administrador.router)
    app.include_router(Test.router)
    app.include_router(Respuestas.router)
    app.include_router(Estadisticas.router)
    app.include_router(TestEstadistica.router)
    app.include_router(Segmentacion.router)
    app.include_router(Auth.router, prefix="/api", tags=["Auth"])
    logger.info("Routers incluidos correctamente.")
except Exception as e:
    logger.error(f"Error al incluir los routers: {e}")
    # No salir en caso de error, Railway podría reintentar
    # sys.exit(1)

# Ruta raíz - también servirá como healthcheck
@app.get("/")
async def root(): 
    return {"message": "API de GESEX funcionando correctamente", "status": "healthy"}

# Ruta para healthcheck con validación de la conexión a la base de datos
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Verificar conexión a la base de datos
        result = db.execute("SELECT 1").first()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Error de conexión a base de datos: {e}")
        return {"status": "unhealthy", "error": str(e)}

# Ruta para depuración
@app.get("/debug")
async def debug_info():
    try:
        environment = {
            k: v for k, v in os.environ.items() 
            if not k.startswith('_') and not k.lower().startswith('secret') 
            and not k.lower().startswith('password')
        }
        
        return {
            "environment": environment,
            "railway": {
                "environment": os.getenv('RAILWAY_ENVIRONMENT', None),
                "project_id": os.getenv('RAILWAY_PROJECT_ID', None),
                "service_id": os.getenv('RAILWAY_SERVICE_ID', None),
            }
        }
    except Exception as e:
        return {"error": str(e)}
