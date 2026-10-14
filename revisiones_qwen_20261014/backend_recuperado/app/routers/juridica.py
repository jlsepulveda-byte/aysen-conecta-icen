import re
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Norma

router = APIRouter(prefix="/juridica", tags=["juridica"])
MATERIAS_MAP = {"PAGOS": "plazos_pago", "PLAZOS_PAGO": "plazos_pago", "plazos_pago": "plazos_pago"}

@router.get("/consulta")
def consulta_juridica(materia: str, fecha_contrato: str | None = None, db: Session = Depends(get_db)):
    if fecha_contrato:
        try:
            date.fromisoformat(fecha_contrato)
        except ValueError:
            raise HTTPException(status_code=422, detail="Fecha no válida. Use AAAA-MM-DD.")
    materia_normalizada = MATERIAS_MAP.get(materia)
    if not materia_normalizada:
        return {"materia": materia, "registros": [], "estado": "SIN_COBERTURA_NORMATIVA",
                "advertencia": "No hay artículos incorporados para esta materia."}
    normas = db.query(Norma).filter(Norma.materia == materia_normalizada).order_by(Norma.norma, Norma.articulo).all()
    return {"materia": materia, "fecha_contrato": fecha_contrato, "vigencia_verificada": False,
            "registros": [{"id": n.id, "norma": n.norma, "articulo": n.articulo, "resumen": n.resumen, "fuente": n.fuente} for n in normas],
            "estado": "REFERENCIAS_CANDIDATAS",
            "advertencia": "Referencias indicativas: sin validación de texto legal histórico ni conclusión jurídica."}
