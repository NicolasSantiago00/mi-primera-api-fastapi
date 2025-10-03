# app/routers/clase_optimized.py

from fastapi import APIRouter, HTTPException, Query, Depends
# Asumiendo que esta importación ya funciona:
from ..cache.cache_decorators import cache_result 

# 🚨 NUEVA IMPORTACIÓN: Sube de 'routers' a 'app', y de 'app' a 'semana-07'
from app import crud 

# También necesitarás importar get_db y Session si tu CRUD las usa:
from database import get_db, Session # Para la conexión a la DB
from crud import get_horarios_disponibles, get_profesor_detail # Para las funciones CRUD

router = APIRouter(prefix="/edu_", tags=["Academia de Música - Clases Optimizado"])

# ... (resto de las importaciones) 
# app/routers/clase_optimized.py

# ... (código de importaciones y router definition) ...

# 1. ENFOQUE PRINCIPAL: Horarios y disponibilidad (Clase Frecuente - 5 min TTL)
@router.get("/clase/disponibilidad")
@cache_result(ttl_type='frequent_data', key_prefix='horario_disponible')
async def get_clases_disponibles(
    instrumento: str = Query(...), 
    nivel: str = Query(...),
    db: Session = Depends(get_db) # ⬅️ Usa las funciones importadas
):
    # Llama a la función importada directamente
    # 🚨 NOTA: Asegúrate de que esta función exista en tu crud.py
    resultado = get_horarios_disponibles(db, instrumento, nivel) 
    
    return resultado

# ... (El resto del código con get_info_profesor, etc., DEBE ser corregido de forma similar)

# Ejemplo para Profesor (también requiere corrección):
@router.get("/profesor/{profesor_id}")
@cache_result(ttl_type='stable_data', key_prefix='profesor_info')
async def get_info_profesor(profesor_id: str, db: Session = Depends(get_db)):
    """
    Obtiene información detallada de un profesor (cambia ocasionalmente).
    """
    # 🚨 CORRECCIÓN PROFESOR
    info_profesor = crud.get_profesor_detail(db, profesor_id) 
    if not info_profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return info_profesor