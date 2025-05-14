from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

# Importaciones internas del proyecto
from app.database import SessionLocal
from app.models.TestEstadistica import TestEstadistica 
from app.schemas.TestEstadistica import TestEstadisticaCreate, TestEstadistica

# Enrutador para el recurso test-estadistica
router = APIRouter(prefix="/test-estadistica", tags=["TestEstadistica"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear una nueva relación entre respuesta y estadística
@router.post("/", response_model=TestEstadistica)
def crear_test_estadistica(
    relacion: TestEstadisticaCreate,
    db: Session = Depends(get_db)
):
    # Crear instancia a partir del schema recibido
    nueva = TestEstadistica.TestEstadistica(**relacion.dict())
    db.add(nueva)  
    db.commit()    
    db.refresh(nueva)  
    return nueva  

# Endpoint para obtener una relación específica por ID
@router.get("/{test_estadistica_id}", response_model=TestEstadistica)
def obtener_test_estadistica(test_estadistica_id: UUID, db: Session = Depends(get_db)):
    # Buscar en la base de datos la relación por ID
    est = db.query(TestEstadistica.TestEstadistica).filter_by(id=test_estadistica_id).first()
    if not est:
        # Si no se encuentra, lanzar excepción HTTP 404
        raise HTTPException(status_code=404, detail="Relación TestEstadistica no encontrada")
    return est  # Devolver resultado encontrado
