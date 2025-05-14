from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import SessionLocal
from app.models.Estadisticas import Estadisticas as EstadisticasModel
from app.schemas.Estadisticas import EstadisticasCreate , EstadisticasOut

from app.models.Respuestas import Respuesta

router = APIRouter(prefix="/estadisticas", tags=["Estadísticas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=EstadisticasOut)
def crear_estadistica(
    estadistica: EstadisticasCreate,
    db: Session = Depends(get_db)
):
    nueva = EstadisticasModel.Estadisticas(resumen=estadistica.resumen)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/{test_id}/dimensiones/promedios", description="Obtener el promedio de cada dimensión (de 1 a 5) con base en todas las respuestas de un test_id")
def promedios_por_dimension(test_id: UUID, db: Session = Depends(get_db)):
    respuestas = db.query(Respuesta).filter(Respuesta.test_id == test_id).all()

    if not respuestas:
        raise HTTPException(status_code=404, detail="No se encontraron respuestas para este test.")

    suma_por_dimension = defaultdict(int)
    conteo_por_dimension = defaultdict(int)

    for r in respuestas:
        for d in r.respuestas:
            nombre_dimension = d["dimension"]
            valores = d["respuestas"]
            suma_por_dimension[nombre_dimension] += sum(valores)
            conteo_por_dimension[nombre_dimension] += len(valores)

    promedios = {
        dimension: round(suma_por_dimension[dimension] / conteo_por_dimension[dimension], 2)
        for dimension in suma_por_dimension
    }

    return promedios

@router.get("/{test_id}/dimensiones/distribucion", description="Mostrar cuántas veces fue elegida cada opción (1 a 5) en cada dimensión.")
def distribucion_por_dimension(test_id: UUID, db: Session = Depends(get_db)):
    respuestas = db.query(Respuesta).filter(Respuesta.test_id == test_id).all()

    if not respuestas:
        raise HTTPException(status_code=404, detail="No se encontraron respuestas para este test.")

    distribucion = defaultdict(lambda: defaultdict(int))

    for r in respuestas:
        for d in r.respuestas:
            dimension = d["dimension"]
            for valor in d["respuestas"]:
                distribucion[dimension][str(valor)] += 1

    return distribucion

@router.get("/comparacion/tipo_participante", description="Ver cómo varía el promedio por dimensión entre grupos: 'universitario', 'habitante', etc.")
def comparacion_global_por_tipo_participante(db: Session = Depends(get_db)):
    respuestas = db.query(Respuesta).all()

    if not respuestas:
        raise HTTPException(status_code=404, detail="No se encontraron respuestas.")

    suma = defaultdict(lambda: defaultdict(float))
    conteo = defaultdict(lambda: defaultdict(int))

    for r in respuestas:
        tipo = r.caracterizacion_datos.get("tipo_participante", "otro")
        for d in r.respuestas:
            dimension = d["dimension"]
            valores = d["respuestas"]
            suma[tipo][dimension] += sum(valores)
            conteo[tipo][dimension] += len(valores)

    resultado = {}
    for tipo in ("universitario", "habitante"):
        if tipo in suma:
            resultado[tipo] = {
                dimension: round(suma[tipo][dimension] / conteo[tipo][dimension], 2)
                for dimension in suma[tipo]
            }
        else:
            resultado[tipo] = {}

    return resultado

@router.get("/{test_id}/por-edad",description="Muestra cómo se comportan los promedios por dimensión según los rangos de edad.")
def promedio_por_edad(test_id: UUID, db: Session = Depends(get_db)):
    respuestas = db.query(Respuesta).filter(Respuesta.test_id == test_id).all()

    agrupados = defaultdict(lambda: defaultdict(list))

    for r in respuestas:
        edad = r.caracterizacion_datos.get("edad", "No especificado")
        for d in r.respuestas:
            dimension = d["dimension"]
            agrupados[edad][dimension].extend(d["respuestas"])

    resultado = {}
    for edad in agrupados:
        resultado[edad] = {
            dim: round(sum(valores) / len(valores), 2)
            for dim, valores in agrupados[edad].items() if valores
        }

    return resultado

@router.get("/{test_id}/por-pronombre", description="Ayuda a ver si hay diferencias perceptibles según el pronombre que usan los participantes.")
def promedio_por_pronombre(test_id: UUID, db: Session = Depends(get_db)):
    respuestas = db.query(Respuesta).filter(Respuesta.test_id == test_id).all()

    agrupados = defaultdict(lambda: defaultdict(list))

    for r in respuestas:
        pronombre = r.caracterizacion_datos.get("pronombre", "No especificado")
        for d in r.respuestas:
            dimension = d["dimension"]
            agrupados[pronombre][dimension].extend(d["respuestas"])

    resultado = {}
    for pronombre in agrupados:
        resultado[pronombre] = {
            dim: round(sum(valores) / len(valores), 2)
            for dim, valores in agrupados[pronombre].items() if valores
        }

    return resultado

@router.get("/{test_id}/habitantes/comuna", description="Muestra cuántas respuestas hay por comuna.")
def conteo_por_comuna(test_id: UUID, db: Session = Depends(get_db)):
    respuestas = db.query(Respuesta).filter(Respuesta.test_id == test_id).all()

    conteo = defaultdict(int)
    for r in respuestas:
        tipo = r.caracterizacion_datos.get("tipo_participante", "")
        if tipo == "habitante":
            comuna = r.caracterizacion_datos.get("comuna", "No especificado")
            conteo[comuna] += 1

    return dict(conteo)
