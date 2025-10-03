# app/cache/domain_strategies.py

from .redis_config import cache_manager
# 🚨 NUEVAS IMPORTACIONES: Sube de 'cache' a 'app', y de 'app' a 'semana-07'
from crud import get_instrumentos, get_niveles, get_horarios_disponibles

# Si necesitas la sesión de DB, también importaría get_db, pero para la precarga 
# a menudo se trabaja sin la sesión de FastAPI o con una temporal (simplificaremos).
class DomainSpecificCaching:
    # ... (Los métodos cache_for_domain_type_a, b, c, d genéricos) ...

    # Personaliza este método para TU dominio específico
    @staticmethod
    async def implement_domain_cache(domain_prefix: str):
        """
        Estrategia de precarga de cache para la Academia de Música.
        Precarga los datos de referencia y los horarios más comunes.
        """
        # 1. Precargar Catálogos (reference_data)
        print("Precargando Catálogo de Instrumentos y Niveles...")
        print("Precargando horarios para Piano y Guitarra (frecuente)...")
        
        # Obtener datos de instrumentos y niveles antes de precargar
        instrumentos = get_instrumentos()
        niveles = get_niveles()
        # Uso directo de set_cache para precargar
        cache_manager.set_cache("catalogo:instrumentos:all", instrumentos, 'reference_data')
        cache_manager.set_cache("catalogo:niveles:all", niveles, 'reference_data')
        
        # 2. Precargar Horarios Populares (frequent_data)
        # Asumiendo que el piano y la guitarra son los más buscados
        print("Precargando horarios para Piano y Guitarra (frecuente)...")
        clases_piano =  get_horarios_disponibles("piano", "basico")
        clases_guitarra = get_horarios_disponibles("guitarra", "basico")
        
        # La clave debe coincidir con la que generaría el decorador (simplificado para el ejemplo)
        # edu_:data:horario_disponible:get_clases_disponibles:[hash]
        # Aquí se usaría un patrón más directo, o se llamaría la función cacheada:
        # await get_clases_disponibles("piano", "basico") 
        # Pero como no tenemos la función importada, simulamos la clave con una más simple:
        cache_manager.set_cache("horario:piano:basico", clases_piano, 'frequent_data')
        cache_manager.set_cache("horario:guitarra:basico", clases_guitarra, 'frequent_data')
        
        print("Precarga de cache de Academia de Música finalizada.")
        