from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.services.optimized_domain_service import OptimizedDomainService
from database import get_db # Asume que get_db está en el archivo raíz 'database.py'
from typing import Optional, List, Dict, Any

router = APIRouter(prefix="/opt/clases", tags=["Optimized Classes"])

@router.get("/disponibilidad", response_model=List[Dict[str, Any]])
async def get_availability_optimized(
    instrumento_id: Optional[int] = Query(None, description="Filtrar por ID de Instrumento"),
    nivel_id: Optional[int] = Query(None, description="Filtrar por ID de Nivel"),
    dia_semana: Optional[str] = Query(None, description="Filtrar por día (Ej: Lunes)"),
    limit: int = Query(20, gt=0, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """
    Endpoint optimizado para encontrar clases disponibles.
    Utiliza consultas Raw SQL con índices específicos.
    """
    service = OptimizedDomainService(db, "type_b")
    return await service.get_available_classes(
        instrumento_id=instrumento_id, 
        nivel_id=nivel_id,
        dia_semana=dia_semana,
        limit=limit
    )

@router.get("/profesor/{profesor_id}/horario", response_model=List[Dict[str, Any]])
async def get_professor_schedule_optimized(
    profesor_id: int,
    dia_semana: str = Query(..., description="Día de la semana (Ej: Martes)"),
    db: Session = Depends(get_db)
):
    """Endpoint optimizado para consultar el horario de un profesor."""
    service = OptimizedDomainService(db, "type_b")
    return await service.get_professor_schedule(profesor_id, dia_semana)
