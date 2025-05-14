from pydantic import BaseModel
from uuid import UUID

class AdministradorBase(BaseModel):
    usuario_id: UUID
    cargo: str

class AdministradorCreate(AdministradorBase):
    pass

class AdministradorOut(AdministradorBase):
    id: UUID

    model_config = {
        "from_attributes": True
    }