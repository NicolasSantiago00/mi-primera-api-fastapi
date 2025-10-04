# semana-07/app/middleware/domain_validator.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
from typing import Dict, Any, Optional

class DomainValidator(BaseHTTPMiddleware):
    def __init__(self, app, domain_prefix: str):
        super().__init__(app)
        self.domain_prefix = domain_prefix
        self.validators = self._get_domain_validators()

    def _get_domain_validators(self) -> Dict[str, Any]:
        """Validadores para Academia de Música"""
        return {
            "edu_": {
                "required_headers": ["X-Institution-ID"],  # ID de la academia
                "business_hours": (8, 20),                # 8 AM a 8 PM
                "weekend_restricted": ["class/booking"],  # No reservas los fines de semana
                "class_capacity_limit": True               # Límite de capacidad por clase
            }
        }.get(self.domain_prefix, {
            "required_headers": [],
            "business_hours": (0, 24),
            "special_validations": []
        })

    def _validate_business_hours(self, path: str) -> bool:
        current_hour = datetime.now().hour
        start_hour, end_hour = self.validators.get("business_hours", (0, 24))
        return start_hour <= current_hour <= end_hour

    def _validate_required_headers(self, request: Request) -> bool:
        required = self.validators.get("required_headers", [])
        for header in required:
            if header not in request.headers:
                return False
        return True

    def _validate_domain_specific_rules(self, request: Request, path: str) -> tuple[bool, Optional[str]]:
        if self.domain_prefix == "edu_":
            weekend_restricted = self.validators.get("weekend_restricted", [])
            if any(restriction in path for restriction in weekend_restricted):
                if datetime.now().weekday() >= 5:
                    return False, "Las reservas de clases no están disponibles los fines de semana"
            if "/class/booking" in path and self.validators.get("class_capacity_limit"):
                # Aquí implementarías lógica para verificar la capacidad de la clase (simplificado)
                pass
        return True, None
    
    

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if not path.startswith("/edu"):
            return await call_next(request)

        if not self._validate_business_hours(path):
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "Fuera del horario de atención",
                    "domain": self.domain_prefix,
                    "business_hours": self.validators["business_hours"]
                }
            )

        if not self._validate_required_headers(request):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Faltan encabezados requeridos",
                    "required_headers": self.validators["required_headers"]
                }
            )

        is_valid, error_message = self._validate_domain_specific_rules(request, path)
        if not is_valid:
            raise HTTPException(
                status_code=422,
                detail={
                    "error": error_message,
                    "domain": self.domain_prefix
                }
            )

     