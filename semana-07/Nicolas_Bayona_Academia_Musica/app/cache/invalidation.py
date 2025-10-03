from .redis_config import cache_manager
from fastapi import APIRouter

router = APIRouter()

# Simulación de un servicio de reserva (debes reemplazarlo por tu implementación real)
class TuServicioReserva:
    async def crear_reserva(self, reserva_data: dict):
        # Lógica simulada de creación de reserva
        class ClaseReservada:
            clase_id = "123"
            instrumento = "guitarra"
            nivel = "intermedio"
        return ClaseReservada()

tu_servicio_reserva = TuServicioReserva()

class DomainCacheInvalidation:

    @staticmethod
    async def on_clase_update_or_reserva(clase_id: str, instrumento: str, nivel: str):
        """
        Invalida caches relacionados con la disponibilidad/horario de una CLASE.
        Esto es crítico para el Foco Performance: Horarios y disponibilidad.
        Se ejecuta cada vez que se reserva una clase, se cancela o se edita el horario.
        """
        # 1. Invalida la clase específica
        cache_manager.invalidate_cache(f"*clase*{clase_id}*")
        
        # 2. Invalida la consulta de disponibilidad frecuente que involucra esta clase
        # El patrón cubre las consultas de disponibilidad: edu_:data:horario_disponible:*
        cache_manager.invalidate_cache("*horario_disponible*") 
        
        # Se podría ser más granular invalidando por instrumento y nivel si la clave lo permitiera
        # cache_manager.invalidate_cache(f"*{instrumento}*{nivel}*") 

    @staticmethod
    async def on_profesor_update(profesor_id: str):
        """Invalida cache cuando se actualiza la información de un profesor."""
        cache_manager.invalidate_cache(f"*profesor_info*{profesor_id}*")
    
    @staticmethod
    async def on_catalog_update():
        """Invalida cache de catálogo de instrumentos o niveles."""
        cache_manager.invalidate_cache("*catalogo*")

# Ejemplo de uso en endpoints de actualización de la API:
@router.post("/edu_/reserva_clase")
async def reservar_clase(reserva_data: dict):
    # Proceso de reserva
    clase_reservada = await tu_servicio_reserva.crear_reserva(reserva_data)
    
    # Después de una reserva exitosa, la disponibilidad CAmBIA -> Invalidar cache
    await DomainCacheInvalidation.on_clase_update_or_reserva(
        clase_id=clase_reservada.clase_id, 
        instrumento=clase_reservada.instrumento, 
        nivel=clase_reservada.nivel
    )
    
    return {"message": "Reserva exitosa y cache de disponibilidad actualizado."}