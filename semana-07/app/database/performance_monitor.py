# app/database/performance_monitor.py (adaptado)
import time
from sqlalchemy import text
from contextlib import contextmanager
from sqlalchemy.orm import Session

class DatabasePerformanceMonitor:
    @staticmethod
    @contextmanager
    def measure_query_time(query_name: str):
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            if duration > 0.5:  # 500ms threshold
                print(f"⚠️ Consulta lenta: {query_name} - {duration:.3f}s")

    @staticmethod
    def analyze_slow_queries(db: Session, domain_prefix: str = "edu_"):
        slow_queries = """
        SELECT query, calls, total_time, mean_time
        FROM pg_stat_statements
        WHERE query LIKE '%eventos%' OR query LIKE '%reservas%'
        ORDER BY mean_time DESC
        LIMIT 10;
        """
        try:
            result = db.execute(text(slow_queries))
            return [dict(row) for row in result]
        except Exception as e:
            print(f"Error: {e}")
            return []