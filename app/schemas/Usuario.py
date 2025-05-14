from pydantic import BaseModel, EmailStr
from uuid import UUID

class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr

class UsuarioCreate(UsuarioBase):
    contrasena: str

class UsuarioOut(UsuarioBase):
    id: UUID

    model_config = {
        "from_attributes": True
    }