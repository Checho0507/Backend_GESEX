from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.Administrador import Administrador
from app.schemas.Administrador import AdministradorCreate, AdministradorOut

router = APIRouter(prefix="/Administradores", tags=["Administradores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AdministradorOut)
def crear_administrador(admin: AdministradorCreate, db: Session = Depends(get_db)):
    nuevo_admin = Administrador(**admin.dict())
    db.add(nuevo_admin)
    db.commit()
    db.refresh(nuevo_admin)
    return nuevo_admin

@router.get("/", response_model=list[AdministradorOut])
def listar_administradores(db: Session = Depends(get_db)):
    return db.query(Administrador).all()
