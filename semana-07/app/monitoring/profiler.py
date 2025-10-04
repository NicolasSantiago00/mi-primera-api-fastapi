# semana-07/app/monitoring/profiler.py
import cProfile
import pstats
import io
from functools import wraps
import asyncio
import time
from typing import Dict, Any

class APIProfiler:
    def __init__(self, domain: str):
        self.domain = domain  # 'edu_'
        self.profiles = {}
        self.memory_profiles = {}

    def profile_function(self, func_name: str = None):
        """Decorador para profiling de funciones (foco en endpoints de clases y horarios)"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                func_id = func_name or func.__name__

                # Profile CPU
                pr = cProfile.Profile()
                pr.enable()

                start_time = time.time()

                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)

                execution_time = time.time() - start_time

                pr.disable()

                # Guardar profile
                s = io.StringIO()
                ps = pstats.Stats(pr, stream=s)
                ps.sort_stats('cumulative')
                ps.print_stats(20)  # Top 20 funciones más lentas

                self.profiles[func_id] = {
                    'execution_time': execution_time,
                    'profile_data': s.getvalue(),
                    'timestamp': time.time()
                }

                return result
            return wrapper
        return decorator

    def get_profile_report(self, func_name: str = None) -> Dict[str, Any]:
        """Obtiene reporte de profiling para endpoints de clases/horarios"""
        if func_name:
            return self.profiles.get(func_name, {})
        return self.profiles

    def clear_profiles(self):
        """Limpia los profiles almacenados"""
        self.profiles.clear()
        self.memory_profiles.clear()

# Decorador específico para memoria (útil para consultas de disponibilidad)
def memory_profile_async(profiler: APIProfiler):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator