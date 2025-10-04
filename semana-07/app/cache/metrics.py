# app/cache/metrics.py
from .redis_config import cache_manager
import time

class CacheMetrics:
    @staticmethod
    def track_cache_hit(key: str):
        """Registra un hit de cache"""
        metric_key = f"metrics:hits:{int(time.time() // 300)}"
        cache_manager.redis_client.incr(metric_key)
        cache_manager.redis_client.expire(metric_key, 3600)

    @staticmethod
    def track_cache_miss(key: str):
        """Registra un miss de cache"""
        metric_key = f"metrics:misses:{int(time.time() // 300)}"
        cache_manager.redis_client.incr(metric_key)
        cache_manager.redis_client.expire(metric_key, 3600)