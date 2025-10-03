import time
from contextlib import contextmanager

# Definición simple de un monitor para medir el tiempo de ejecución
class DatabasePerformanceMonitor:

    @staticmethod
    @contextmanager
    def measure_query_time(query_name: str):
        """Context manager para medir tiempo de consultas y loguear si es lenta."""
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            print(f"Monitor: Query '{query_name}' ejecutada en {duration:.4f}s")

            # Umbral de lentitud para la Academia de Música: 200ms
            if duration > 0.2:  
                print(f"⚠️  ALERTA LENTITUD: Query '{query_name}' tardó {duration:.4f}s")
