# semana-07/app/monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge
import time
from functools import wraps
from typing import Dict

class APIMetrics:
    def __init__(self, app_name: str, domain: str):
        self.app_name = app_name
        self.domain = domain  # 'edu_'

        # Métricas personalizadas para Academia de Música
        self.request_counter = Counter(
            f'{domain}_requests_total',
            'Total de requests por endpoint',
            ['method', 'endpoint', 'status']
        )

        self.response_time = Histogram(
            f'{domain}_response_duration_seconds',
            'Tiempo de respuesta por endpoint (foco en horarios y disponibilidad)',
            ['method', 'endpoint'],
            buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
        )

        self.active_connections = Gauge(
            f'{domain}_active_connections',
            'Conexiones activas en consultas de clases'
        )

        self.system_metrics = {
            'cpu_usage': Gauge(f'{domain}_cpu_usage_percent', 'Uso de CPU durante reservas'),
            'memory_usage': Gauge(f'{domain}_memory_usage_bytes', 'Uso de memoria en horarios'),
            'disk_usage': Gauge(f'{domain}_disk_usage_percent', 'Uso de disco')
        }

        # Métricas específicas del dominio: Academia de Música (entidad 'clase')
        self.business_metrics = self._create_business_metrics()

    def _create_business_metrics(self):
        """Métricas específicas para clases, horarios y disponibilidad"""
        return {
            'classes_booked': Counter(
                f'{self.domain}_classes_booked_total',
                'Total de clases reservadas'
            ),
            'schedule_queries': Counter(
                f'{self.domain}_schedule_queries_total',
                'Total de consultas de horarios'
            ),
            'teacher_availability_checks': Counter(
                f'{self.domain}_teacher_availability_checks_total',
                'Total de chequeos de disponibilidad de profesores'
            ),
            'api_errors': Counter(
                f'{self.domain}_api_errors_total',
                'Total de errores de API',
                ['error_type']
            )
        }

    def record_request(self, method: str, endpoint: str, status: int, duration: float):
        """Registra métricas de request"""
        self.request_counter.labels(
            method=method,
            endpoint=endpoint,
            status=status
        ).inc()

        self.response_time.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)

    def record_business_event(self, event_type: str, **kwargs):
        """Registra eventos de negocio específicos (ej. reserva de clase)"""
        if event_type in self.business_metrics:
            if hasattr(self.business_metrics[event_type], 'labels'):
                self.business_metrics[event_type].labels(**kwargs).inc()
            else:
                self.business_metrics[event_type].inc()

# Decorador para métricas automáticas
def monitor_performance(metrics: APIMetrics):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time

                # Registrar métricas de éxito (ajustar method según endpoint)
                metrics.record_request(
                    method="POST",  # Ejemplo; personaliza por endpoint
                    endpoint=func.__name__,
                    status=200,
                    duration=duration
                )
                return result
            except Exception as e:
                duration = time.time() - start_time

                # Registrar métricas de error
                metrics.record_request(
                    method="POST",
                    endpoint=func.__name__,
                    status=500,
                    duration=duration
                )

                metrics.record_business_event(
                    'api_errors',
                    error_type=type(e).__name__
                )
                raise
        return wrapper
    return decorator