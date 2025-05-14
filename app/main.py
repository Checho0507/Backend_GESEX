from fastapi import FastAPI
from app.routers import Usuario, Administrador, Test, Respuestas , Estadisticas , TestEstadistica , Segmentacion, Auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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