from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import date
from uuid import UUID

# Subschema para agrupar respuestas por dimensión
class RespuestaDimension(BaseModel):
    dimension: str
    respuestas: List[int]

# Esquema para crear una respuesta
class RespuestaCreate(BaseModel):
    test_id: UUID
    respuestas: List[RespuestaDimension]
    caracterizacion_datos: Dict[str, Any]  # Nuevo campo dinámico
    fecha: date
    fingerprint: str # Campo de validación de respuestas

# Esquema de salida (incluye el ID generado)
class RespuestaOut(RespuestaCreate):
    id: UUID

    class Config:
        orm_mode = True
