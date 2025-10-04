from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

# 🚨 CORRECCIÓN CLAVE: Importaciones absolutas desde 'app.database'
from app.database.performance_monitor import PerformanceMonitor
from app.database.optimized_queries import OPTIMIZED_QUERY_TYPE_B

# Importamos el DTO de respuesta (asumiendo que está en app/schemas)
from app.schemas import ClaseHorarioOptimized # Asume que este DTO existe


class OptimizedDomainService:
    """
    Capa de servicio para la Práctica 24: Optimizaciones de Base de Datos.
    Se encarga de ejecutar la consulta RAW SQL optimizada y medir su rendimiento.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_optimized_schedule(self, instrumento: str, dia_semana: int) -> List[ClaseHorarioOptimized]:
        """
        Ejecuta la consulta RAW SQL optimizada (Tipo B) para encontrar
        la disponibilidad de clases por instrumento y día.
        """
        
        # 1. Obtenemos el texto de la consulta optimizada (con placeholders de SQLAlchemy)
        query_template = OPTIMIZED_QUERY_TYPE_B
        
        # 2. Preparamos los parámetros para la consulta
        params = {
            "instrumento_param": instrumento,
            "dia_semana_param": dia_semana
        }

        # 3. Ejecución de la consulta usando el monitor de rendimiento
        # Esto nos permite ver en la consola cuánto tardó la consulta.
        monitor = PerformanceMonitor(
            query_template, 
            params, 
            query_name="Optimized Schedule Query (P24)"
        )
        
        # Ejecutamos y obtenemos los resultados como Rows de SQLAlchemy
        raw_results = monitor.execute_query(self.db)
        
        # 4. Transformamos los resultados a una lista de Pydantic DTOs
        # El DTO ClaseHorarioOptimized debe mapear las columnas del RAW SQL
        results: List[ClaseHorarioOptimized] = []
        for row in raw_results:
            try:
                # Mapeo directo de las columnas de la consulta (asegúrate de que coincidan)
                results.append(ClaseHorarioOptimized(
                    clase_id=row.clase_id,
                    titulo=row.titulo,
                    instrumento=row.instrumento,
                    nivel=row.nivel,
                    profesor_id=row.profesor_id,
                    profesor_nombre=row.profesor_nombre,
                    dia_semana=row.dia_semana,
                    hora_inicio=datetime.strptime(row.hora_inicio, '%H:%M:%S').time(), # Convertir string a time
                    hora_fin=datetime.strptime(row.hora_fin, '%H:%M:%S').time(),      # Convertir string a time
                    disponible=row.disponible
                ))
            except Exception as e:
                # Esto ayuda a debuggear si el mapeo del DTO falla
                print(f"Error al mapear fila a DTO: {e} | Fila: {row}")
                continue

        return results