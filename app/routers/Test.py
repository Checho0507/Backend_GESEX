from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import SessionLocal
from app.models.Test import Test
from app.schemas.Test import TestCreate, TestOut

router = APIRouter(prefix="/cuestionarios", tags=["Tests"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TestOut)
def crear_test(test: TestCreate, db: Session = Depends(get_db)):
    nuevo_test = Test(
        titulo=test.titulo,
        dimensiones=[dim.dict() for dim in test.dimensiones],
        caracterizacion_template=test.caracterizacion_template.dict(),
        categoria=test.categoria.dict()
    )
    db.add(nuevo_test)
    db.commit()
    db.refresh(nuevo_test)
    return nuevo_test

@router.get("/", response_model=list[TestOut])
def listar_tests(db: Session = Depends(get_db)):
    return db.query(Test).all()

@router.get("/{id}", response_model=TestOut)
def obtener_test(id: UUID, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.id == id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test no encontrado")
    return test

@router.put("/{id}", response_model=TestOut)
def actualizar_test(id: UUID, test_actualizado: TestCreate, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.id == id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test no encontrado")
    
    test.titulo = test_actualizado.titulo
    test.dimensiones = [dim.dict() for dim in test_actualizado.dimensiones]
    test.caracterizacion_template = test_actualizado.caracterizacion_template.dict()

    db.commit()
    db.refresh(test)
    return test

@router.delete("/{id}")
def eliminar_test(id: UUID, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.id == id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test no encontrado")
    
    db.delete(test)
    db.commit()
    return {"mensaje": "Test eliminado correctamente"}
