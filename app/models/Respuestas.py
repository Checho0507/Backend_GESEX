from sqlalchemy import Column, ForeignKey, String, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
import uuid
from app.database import Base


class Respuesta(Base):
    __tablename__ = "respuestas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    test_id = Column(UUID(as_uuid=True), ForeignKey("tests.id"), nullable=False)
    respuestas = Column(MutableList.as_mutable(JSON), nullable=False)  # Lista de respuestas
    caracterizacion_datos = Column(JSON, nullable=False)  # Nuevo: campos dinámicos según el template
    fecha = Column(Date, nullable=False)
    fingerprint = Column(String, nullable=False)

    # Relaciones
    test = relationship("Test", back_populates="respuesta", lazy="joined")

    def __repr__(self):
        return f"<Respuesta id={self.id} usuario_id={self.usuario_id} test_id={self.test_id}>"
