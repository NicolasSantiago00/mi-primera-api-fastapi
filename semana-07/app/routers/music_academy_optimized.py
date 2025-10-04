# app/routers/music_academy_optimized.py
from fastapi import APIRouter, HTTPException
from ..services.music_academy_service import get_class_schedules, get_teacher_availability, get_instrument_catalog
from ..cache.cache_decorators import cache_result

router = APIRouter(prefix="/edu", tags=["Music Academy Optimized"])

@router.get("/classes/schedules")
@cache_result(ttl_type='class_schedules', key_prefix='edu_schedules')
async def get_class_schedules_endpoint(day: str = "2025-10-03"):
    """Obtiene horarios de clases para un día específico"""
    schedules = await get_class_schedules(day)
    if not schedules:
        raise HTTPException(status_code=404, detail="No schedules found")
    return schedules

@router.get("/teachers/availability")
@cache_result(ttl_type='teacher_availability', key_prefix='edu_availability')
async def get_teacher_availability_endpoint(teacher_id: str):
    """Obtiene disponibilidad de un profesor"""
    availability = await get_teacher_availability(teacher_id)
    if not availability:
        raise HTTPException(status_code=404, detail="No availability found")
    return availability

@router.get("/catalog/instruments")
@cache_result(ttl_type='instrument_catalog', key_prefix='edu_catalog')
async def get_instrument_catalog_endpoint():
    """Obtiene catálogo de instrumentos"""
    catalog = await get_instrument_catalog()
    return catalog