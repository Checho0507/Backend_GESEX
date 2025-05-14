from pydantic import BaseModel
from uuid import UUID
from datetime import date

# Base que define los campos requeridos para crear o representar TestEstadistica
class TestEstadisticaBase(BaseModel):
    respuestaId: UUID 
    estadisticaId: UUID  
    fechaGeneracion: date  

# Esquema utilizado para la creación de TestEstadistica
class TestEstadisticaCreate(TestEstadisticaBase):
    pass  # Hereda todo de la base

# Esquema de salida, incluye también el ID generado
class TestEstadistica(TestEstadisticaBase):
    id: UUID

    class Config:
        orm_mode = True  # Permite compatibilidad con modelos ORM (SQLAlchemy)
