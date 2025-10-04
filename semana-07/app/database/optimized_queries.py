# app/database/optimized_queries.py (adaptado para edu_)
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any

class DomainOptimizedQueries:
    @staticmethod
    def get_optimized_queries_type_b():
        """Consultas optimizadas para Academia de Música (tipo B)"""
        return {
            'horarios_disponibles': """
                SELECT r.nombre, e.dia_semana, e.hora_inicio, e.hora_fin
                FROM recursos r
                LEFT JOIN eventos e ON r.id = e.recurso_id
                    AND e.dia_semana = :dia
                    AND e.hora_inicio = :hora
                WHERE r.disponible = true
                AND r.capacidad >= :capacidad_minima
                AND e.id IS NULL
                ORDER BY r.capacidad
            """,
            'reservas_estudiante': """
                SELECT e.dia_semana, e.hora_inicio, p.nombre as profesor,
                       r.nombre as recurso
                FROM reservas res
                JOIN eventos e ON res.evento_id = e.id
                JOIN profesores p ON e.responsable_id = p.id
                JOIN recursos r ON e.recurso_id = r.id
                WHERE res.usuario_id = :usuario_id
                AND res.estado = 'activa'
                ORDER BY e.dia_semana, e.hora_inicio
            """
        }

    @staticmethod
    def get_queries_for_domain(domain_type: str = "type_b"):
        if domain_type == "type_b":
            return DomainOptimizedQueries.get_optimized_queries_type_b()
        return {}