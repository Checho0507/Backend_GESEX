from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import JSON
import uuid
from app.database import Base
from sqlalchemy.orm import relationship

class Test(Base):
    __tablename__ = "tests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = Column(String, nullable=False)
    dimensiones = Column(JSON, nullable=False)  # Estructura de dimensiones y preguntas en formato JSON
    caracterizacion_template = Column(JSON, nullable=False)  # Nuevo campo para datos de caracterización
    categoria = Column(JSON, nullable=True)  # Estructura de categoría dada por la segmentación

    respuesta = relationship("Respuesta", back_populates="test", lazy="joined")
    def __repr__(self):
        return f"<Test id={self.id} titulo={self.titulo}>"
