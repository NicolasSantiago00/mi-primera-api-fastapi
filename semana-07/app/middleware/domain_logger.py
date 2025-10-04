# semana-07/app/middleware/domain_logger.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import json
import time
from typing import Dict, Any

class DomainLogger(BaseHTTPMiddleware):
    def __init__(self, app, domain_prefix: str):
        super().__init__(app)
        self.domain_prefix = domain_prefix
        self.logger = logging.getLogger(f"{domain_prefix}domain_logger")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(f"logs/{domain_prefix}domain.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logged_endpoints = self._get_logged_endpoints()

    def _get_logged_endpoints(self) -> Dict[str, str]:
        """Define los endpoints a registrar para Academia de Música"""
        return {
            "edu_": {
                "/class/booking": "INFO",       # Reservas de clases
                "/schedule": "INFO",            # Consultas o cambios de horarios
                "/enrollment": "WARNING",       # Inscripciones de estudiantes
                "/teacher/availability": "INFO", # Consultas de disponibilidad de profesores
                "/admin": "WARNING"             # Acciones administrativas
            }
        }.get(self.domain_prefix, {
            "/create": "INFO",
            "/update": "WARNING",
            "/delete": "CRITICAL",
            "/admin": "WARNING"
        })

    def _should_log_endpoint(self, path: str) -> tuple[bool, str]:
        for endpoint_pattern, level in self.logged_endpoints.items():
            if endpoint_pattern in path:
                return True, level
        return False, "INFO"

    def _extract_domain_specific_data(self, request: Request, path: str) -> Dict[str, Any]:
        data = {
            "domain": self.domain_prefix,
            "path": path,
            "method": request.method,
            "client_ip": request.client.host,
            "user_agent": request.headers.get("user-agent", "unknown")
        }
        if self.domain_prefix == "edu_":
            if "estudiante_id" in str(request.url):
                data["entity_type"] = "estudiante"
            elif "clase_id" in str(request.url):
                data["entity_type"] = "clase"
            elif "profesor_id" in str(request.url):
                data["entity_type"] = "profesor"
        return data

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        path = request.url.path

        if not path.startswith("/edu"):
            return await call_next(request)

        should_log, log_level = self._should_log_endpoint(path)
        if should_log:
            request_data = self._extract_domain_specific_data(request, path)
            self.logger.log(
                getattr(logging, log_level),
                f"INICIO_SOLICITUD: {json.dumps(request_data)}"
            )

        response = await call_next(request)
        if should_log:
            process_time = time.time() - start_time
            response_data = {
                **request_data,
                "status_code": response.status_code,
                "process_time": round(process_time, 3)
            }
            response_level = "CRITICAL" if response.status_code >= 500 else "WARNING" if response.status_code >= 400 else log_level
            self.logger.log(
                getattr(logging, response_level),
                f"FIN_SOLICITUD: {json.dumps(response_data)}"
            )
        return response