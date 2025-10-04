# app/database/profiling.py (adaptado)
import time
import logging
from sqlalchemy import event
from sqlalchemy.engine import Engine


# Configurar logging para consultas lentas
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sql_performance")

@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()

@event.listens_for(Engine, "after_cursor_execute")
def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - context._query_start_time
    if total > 0.1:  # Log consultas que toman más de 100ms
        logger.warning(f"Consulta lenta ({total:.3f}s): {statement[:100]}...")

def analyze_domain_queries(domain_prefix: str = "edu_"):
    """
    Analiza las consultas específicas de la Academia de Música
    """
    slow_queries = []

    # Consultas típicas a analizar para tu dominio
    test_queries = [
        "SELECT * FROM eventos WHERE dia_semana = '2025-10-03' AND hora_inicio >= '07:00 PM'",  # Horarios
        "SELECT r.nombre FROM recursos r LEFT JOIN eventos e ON r.id = e.recurso_id WHERE r.disponible = true",  # Disponibilidad
        "SELECT e.* FROM eventos e JOIN reservas r ON e.id = r.evento_id WHERE r.usuario_id = 123",  # Reservas por estudiante
        "SELECT p.nombre FROM profesores p JOIN eventos e ON p.id = e.responsable_id WHERE e.dia_semana = '2025-10-03'"  # Profesores por día
    ]

    return slow_queries