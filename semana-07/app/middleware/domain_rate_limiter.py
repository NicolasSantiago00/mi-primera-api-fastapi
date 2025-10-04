# semana-07/app/middleware/domain_rate_limiter.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import redis
import time
from typing import Dict

class DomainRateLimiter(BaseHTTPMiddleware):
    def __init__(self, app, domain_prefix: str, redis_client: redis.Redis):
        super().__init__(app)
        self.domain_prefix = domain_prefix
        self.redis = redis_client
        self.rate_limits = self._get_domain_rate_limits()

    def _get_domain_rate_limits(self) -> Dict[str, Dict]:
        """Configuración de límites específicos para Academia de Música"""
        return {
            "edu_": {
                "class_booking": {"requests": 50, "window": 60},   # 50 req/min para reservas de clases
                "schedule_query": {"requests": 150, "window": 60}, # 150 req/min para consultas de horarios
                "teacher_availability": {"requests": 100, "window": 60}, # 100 req/min para disponibilidad de profesores
                "general": {"requests": 100, "window": 60},        # 100 req/min para otras consultas
                "admin": {"requests": 30, "window": 60}            # 30 req/min para tareas administrativas
            }
        }.get(self.domain_prefix, {
            "general": {"requests": 100, "window": 60},
            "admin": {"requests": 30, "window": 60}
        })

    def _get_rate_limit_category(self, path: str, method: str) -> str:
        """Determina la categoría de rate limit según el endpoint"""
        if self.domain_prefix == "edu_":
            if "/class/booking" in path or "/reserva/clase" in path:
                return "class_booking"
            elif "/schedule" in path or "/horario" in path:
                return "schedule_query"
            elif "/teacher/availability" in path or "/profesor/disponibilidad" in path:
                return "teacher_availability"
            elif "/admin" in path:
                return "admin"
        return "general"

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        path = request.url.path
        method = request.method

        if not path.startswith("/edu"):
            return await call_next(request)

        category = self._get_rate_limit_category(path, method)
        rate_config = self.rate_limits.get(category, self.rate_limits["general"])

        if not self._check_rate_limit(client_ip, category, rate_config):
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Límite de solicitudes excedido",
                    "category": category,
                    "limit": rate_config["requests"],
                    "window": rate_config["window"],
                    "domain": self.domain_prefix
                }
            )

        response = await call_next(request)
        return response

    def _check_rate_limit(self, client_ip: str, category: str, config: Dict) -> bool:
        current_time = int(time.time())
        window_start = current_time - config["window"]
        key = f"{self.domain_prefix}:rate_limit:{category}:{client_ip}"

        requests = self.redis.zrangebyscore(key, window_start, current_time)
        if len(requests) >= config["requests"]:
            return False

        self.redis.zadd(key, {str(current_time): current_time})
        self.redis.expire(key, config["window"])
        self.redis.zremrangebyscore(key, 0, window_start)
        return True