from fastapi import FastAPI, Depends
from routers import Usuario, Administrador, Test, Respuestas, Estadisticas, TestEstadistica, Segmentacion, Auth
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import Base, engine, get_db

import logging
import os
import sys
import uvicorn

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear instancia de FastAPI
app = FastAPI()

# Configuración desde variables de entorno
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://frontend-gesex-production.up.railway.app")
DEVELOPMENT_URL = os.getenv("DEVELOPMENT_URL", "http://localhost:5173")

# Mostrar configuración
logger.info(f"FRONTEND_URL: {FRONTEND_URL}")
logger.info(f"DEVELOPMENT_URL: {DEVELOPMENT_URL}")
logger.info(f"DATABASE_URL existe: {os.getenv('DATABASE_URL') is not None}")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, DEVELOPMENT_URL, "*"],  # puedes dejar "*" solo mientras depuras
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar BD al iniciar
@app.on_event("startup")
async def startup_db_client():
    try:
        logger.info("Iniciando creación de tablas...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas creadas correctamente")
    except Exception as e:
        logger.error(f"Error al crear las tablas: {e}")
        sys.exit(1)

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
    logger.info("Todos los routers incluidos correctamente")
except Exception as e:
    logger.error(f"Error al incluir los routers: {e}")

# Endpoints básicos
@app.get("/")
async def root():
    return {"message": "API de GESEX funcionando correctamente"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/debug")
async def debug_info(db: Session = Depends(get_db)):
    try:
        db_info = {
            "connected": True,
            "tables": list(Base.metadata.tables.keys())
        }
        return {
            "database": db_info,
            "environment": {
                k: v for k, v in os.environ.items() if not k.startswith('_')
            }
        }
    except Exception as e:
        return {"error": str(e)}

# Punto de entrada para ejecución local o Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
