from pydantic import BaseModel
from typing import List
from uuid import UUID
from typing import Optional

class Dimension(BaseModel):
    nombre: str
    preguntas: List[str]

class CaracterizacionTemplate(BaseModel):
    tipo_participante: str
    campos_requeridos: List[str]
    
class Categoria(BaseModel):
    porcentaje: float
    categoria: str

class TestCreate(BaseModel):
    titulo: str
    dimensiones: List[Dimension]
    caracterizacion_template: CaracterizacionTemplate  # nuevo campo
    categoria : Categoria
    
class TestOut(BaseModel):
    id: UUID
    titulo: str
    dimensiones: List[Dimension]
    caracterizacion_template: CaracterizacionTemplate  # nuevo campo
    categoria : Categoria

    class Config:
        orm_mode = True
