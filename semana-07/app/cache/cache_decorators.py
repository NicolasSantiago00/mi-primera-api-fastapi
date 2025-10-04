# app/cache/cache_decorators.py
from functools import wraps
from .redis_config import cache_manager
import hashlib

def cache_result(ttl_type: str = 'class_schedules', key_prefix: str = "edu_queries"):
    """Decorator para cachear resultados de consultas de Academia de Música"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            func_name = func.__name__
            args_str = str(args) + str(sorted(kwargs.items()))
            key_hash = hashlib.md5(args_str.encode()).hexdigest()[:8]
            cache_key = f"{key_prefix}:{func_name}:{key_hash}"

            cached_result = cache_manager.get_cache(cache_key)
            if cached_result is not None:
                return cached_result

            result = await func(*args, **kwargs)
            cache_manager.set_cache(cache_key, result, ttl_type)
            return result
        return wrapper
    return decorator