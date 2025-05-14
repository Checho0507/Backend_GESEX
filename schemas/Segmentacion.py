# schemas/Segmentacion.py

from pydantic import BaseModel

# Representa la respuesta de la segmentación
class ResultadoSegmentacion(BaseModel):
    porcentaje: float
    categoria: str

# Recibe las respuestas que serán analizadas
class EntradasSegmentacion(BaseModel):
    respuestas: list[str]
