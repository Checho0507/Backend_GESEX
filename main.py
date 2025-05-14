from fastapi import FastAPI
from routers import Usuario, Administrador, Test, Respuestas, Estadisticas, TestEstadistica, Segmentacion, Auth
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Obtener las URLs permitidas desde variables de entorno o usar valores por defecto
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://frontend-gesex-production.up.railway.app")
DEVELOPMENT_URL = os.getenv("DEVELOPMENT_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, DEVELOPMENT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Usuario.router)
app.include_router(Administrador.router)
app.include_router(Test.router)
app.include_router(Respuestas.router)
app.include_router(Estadisticas.router)
app.include_router(TestEstadistica.router)
app.include_router(Segmentacion.router)
# NUEVO: Router de autenticación
app.include_router(Auth.router, prefix="/api", tags=["Auth"])

@app.get("/")
async def root():
    return {"message": "API de GESEX funcionando correctamente"}
