from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class EstadisticasBase(BaseModel):
    resumen: str

class EstadisticasCreate(EstadisticasBase):
    pass

class EstadisticasOut(EstadisticasBase):
    id: UUID
    fecha_generacion: datetime
    
    class Config:
        orm_mode = True

   
        