import uuid
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class Administrador(Base):
    __tablename__ = "administradores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cargo = Column(String, nullable=False)

    usuario = relationship("Usuario")
