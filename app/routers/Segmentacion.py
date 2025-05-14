# routers/Segmentacion.py

from fastapi import APIRouter
from app.models.Segmentacion import Segmentacion
from app.schemas.Segmentacion import ResultadoSegmentacion, EntradasSegmentacion
from app.database import SessionLocal  # Import SessionLocal from your database module

router = APIRouter(prefix="/segmentacion", tags=["Segmentación"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ResultadoSegmentacion)
def analizar_respuestas(datos: EntradasSegmentacion):
    """
    Recibe una lista de respuestas y calcula el porcentaje y categoría.
    """
    resultado = Segmentacion.calcular_categoria(datos.respuestas)
    return resultado
