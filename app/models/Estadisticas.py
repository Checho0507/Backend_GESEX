from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.database import Base

class Estadisticas(Base):
    __tablename__ = "estadisticas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resumen = Column(String, nullable=False)
    fecha_generacion = Column(DateTime, default=datetime.utcnow)

    # Relación con TestEstadistica (uno a muchos)
    test_estadisticas = relationship("TestEstadistica", back_populates="estadistica")
