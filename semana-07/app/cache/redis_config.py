# app/cache/redis_config.py
import redis
import os
from typing import Optional, Any

class DomainCacheConfig:
    def __init__(self, domain_prefix: str):
        self.domain_prefix = domain_prefix
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=os.getenv('REDIS_PORT', 6379),
            db=0,
            decode_responses=True
        )
        # TTL personalizados para Academia de Música
        self.cache_ttl = {
            'class_schedules': 300,      # 5 minutos para horarios de clases
            'teacher_availability': 60,  # 1 minuto para disponibilidad de profesores
            'instrument_catalog': 86400, # 24 horas para catálogo de instrumentos
            'class_types': 3600          # 1 hora para tipos de clases
        }

    def get_cache_key(self, category: str, identifier: str) -> str:
        """Genera claves de cache específicas para Academia de Música"""
        return f"{self.domain_prefix}:{category}:{identifier}"

    def set_cache(self, key: str, value: Any, ttl_type: str = 'class_schedules') -> bool:
        """Almacena datos en cache con TTL específico"""
        try:
            cache_key = self.get_cache_key("data", key)
            serialized_value = str(value)  # Simplificación para este ejemplo
            ttl = self.cache_ttl.get(ttl_type, 300)
            return self.redis_client.setex(cache_key, ttl, serialized_value)
        except Exception as e:
            print(f"Error setting cache: {e}")
            return False

    def get_cache(self, key: str) -> Optional[Any]:
        """Recupera datos del cache"""
        try:
            cache_key = self.get_cache_key("data", key)
            cached_value = self.redis_client.get(cache_key)
            return cached_value if cached_value else None
        except Exception as e:
            print(f"Error getting cache: {e}")
            return None

    def invalidate_cache(self, pattern: str = None):
        """Invalida cache específico o por patrón"""
        try:
            if pattern:
                cache_pattern = self.get_cache_key("data", pattern)
                keys = self.redis_client.keys(cache_pattern + "*")
                if keys:
                    self.redis_client.delete(*keys)
            else:
                domain_keys = self.redis_client.keys(f"{self.domain_prefix}:*")
                if domain_keys:
                    self.redis_client.delete(*domain_keys)
        except Exception as e:
            print(f"Error invalidating cache: {e}")

# Instancia para tu dominio
cache_manager = DomainCacheConfig("edu_")