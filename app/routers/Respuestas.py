from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, date

from app.database import SessionLocal
from app.models.Respuestas import Respuesta
from app.models.Test import Test
from app.models.Segmentacion import Segmentacion
from app.schemas.Respuestas import RespuestaCreate, RespuestaOut

router = APIRouter(prefix="/Respuestas", tags=["Respuestas"])

# Dependencia para obtener la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST para recibir y guardar respuestas
@router.post("/", response_model=RespuestaOut)
def enviar_respuesta(respuesta: RespuestaCreate, db: Session = Depends(get_db)):
    # Verifica si ya existe una respuesta con ese test_id y fingerprint
    existente = db.query(Respuesta).filter_by(
        test_id=respuesta.test_id,
        fingerprint=respuesta.fingerprint
    ).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya se ha respondido este test desde esta sesión."
        )
    nueva = Respuesta(
        test_id=respuesta.test_id,
        respuestas=[r.dict() for r in respuesta.respuestas],
        caracterizacion_datos=respuesta.caracterizacion_datos,
        fecha=respuesta.fecha,
        fingerprint = respuesta.fingerprint
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    # Calcular categoría basada en las respuestas
    categoria = Segmentacion.calcular_categoria(nueva.respuestas)

    # Actualizar la categoría del usuario
    test = db.query(Test).filter_by(id=respuesta.test_id).first()
    if test:
        test.categoria = categoria
        db.commit()

    return nueva

# GET general para ver todas las respuestas
@router.get("/", response_model=list[RespuestaOut])
def listar_respuestas(db: Session = Depends(get_db)):
    return db.query(Respuesta).all()
