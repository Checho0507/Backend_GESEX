from sqlalchemy import Column, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.database import Base

# Modelo que representa la relación entre una Respuesta y una Estadística generada a partir de esa respuesta
class TestEstadistica(Base):
    __tablename__ = "test_estadistica"

    # ID único para la entidad
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    respuestaId = Column(UUID(as_uuid=True), nullable=False)
    estadisticaId = Column(UUID(as_uuid=True), ForeignKey("estadisticas.id"), nullable=False)
    fechaGeneracion = Column(Date, nullable=False)

    # Relación con el modelo Estadisticas (permite acceso desde la entidad relacionada)
    estadistica = relationship("Estadisticas", back_populates="test_estadisticas")
