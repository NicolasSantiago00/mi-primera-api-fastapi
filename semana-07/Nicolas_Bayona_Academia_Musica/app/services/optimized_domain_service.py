from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.optimized_queries import DomainOptimizedQueries
from app.database.performance_monitor import DatabasePerformanceMonitor
from typing import List, Dict, Any, Optional

class OptimizedDomainService:
    def __init__(self, db: Session, domain_prefix: str = "type_b"):
        self.db = db
        self.queries = DomainOptimizedQueries.get_queries_for_domain(domain_prefix)

    async def execute_optimized_query(self, query_name: str, params: Dict[str, Any]) -> List[Dict]:
        """Ejecuta consulta optimizada específica del dominio"""
        if query_name not in self.queries:
            raise ValueError(f"Query {query_name} no encontrada.")

        query = self.queries[query_name]
        
        # Usa el monitor de performance para medir el tiempo de la consulta
        with DatabasePerformanceMonitor.measure_query_time(query_name):
            # Ejecuta la consulta SQL cruda con parámetros seguros
            result = self.db.execute(text(query), params)
            # Retorna los resultados como lista de diccionarios
            return [dict(row) for row in result.all()]

    async def get_available_classes(
        self, 
        instrumento_id: Optional[int] = None, 
        nivel_id: Optional[int] = None,
        dia_semana: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """Obtiene disponibilidad de clases de forma optimizada."""
        params = {
            "instrumento_id": instrumento_id,
            "nivel_id": nivel_id,
            "dia_semana": dia_semana,
            "limit": limit
        }
        return await self.execute_optimized_query('disponibilidad_clase', params)

    async def get_professor_schedule(self, profesor_id: int, dia_semana: str) -> List[Dict]:
        """Obtiene el horario de un profesor en un día específico de forma optimizada."""
        params = {
            "profesor_id": profesor_id,
            "dia_semana": dia_semana
        }
        return await self.execute_optimized_query('clases_profesor_dia', params)
