# app/cache/invalidation.py
from .redis_config import cache_manager

class DomainCacheInvalidation:
    @staticmethod
    async def on_schedule_update(class_id: str):
        """Invalida cache cuando se actualiza un horario"""
        cache_manager.invalidate_cache(f"class_schedules:{class_id}")

    @staticmethod
    async def on_availability_update(teacher_id: str):
        """Invalida cache cuando cambia la disponibilidad de un profesor"""
        cache_manager.invalidate_cache(f"teacher_availability:{teacher_id}")

    @staticmethod
    async def on_catalog_update():
        """Invalida cache del catálogo de instrumentos"""
        cache_manager.invalidate_cache("instrument_catalog")