from typing import List, Dict, Any

class DomainOptimizedQueries:
    """
    Consultas optimizadas específicas para el dominio de la Academia de Música (Tipo B)
    """

    @staticmethod
    def get_optimized_queries_type_b():
        return {
            'disponibilidad_clase': """
                -- Consulta optimizada para encontrar clases disponibles por filtros clave.
                SELECT 
                    c.id, c.dia_semana, c.hora_inicio, c.hora_fin, c.capacidad, c.estudiantes_inscritos,
                    i.nombre AS instrumento_nombre, n.nombre AS nivel_nombre, p.nombre AS profesor_nombre
                FROM 
                    clase c
                JOIN 
                    instrumento i ON c.instrumento_id = i.id
                JOIN 
                    nivel n ON c.nivel_id = n.id
                JOIN 
                    profesor p ON c.profesor_id = p.id
                WHERE 
                    (:instrumento_id IS NULL OR c.instrumento_id = :instrumento_id)
                    AND (:nivel_id IS NULL OR c.nivel_id = :nivel_id)
                    AND c.estudiantes_inscritos < c.capacidad -- Solo clases con cupo
                    AND (:dia_semana IS NULL OR c.dia_semana = :dia_semana)
                ORDER BY 
                    c.dia_semana, c.hora_inicio
                LIMIT :limit;
            """,
            
            'clases_profesor_dia': """
                -- Consulta optimizada para obtener todas las clases de un profesor en un día específico.
                SELECT 
                    c.id, c.hora_inicio, c.hora_fin, i.nombre AS instrumento, n.nombre AS nivel
                FROM 
                    clase c
                JOIN 
                    instrumento i ON c.instrumento_id = i.id
                JOIN 
                    nivel n ON c.nivel_id = n.id
                WHERE 
                    c.profesor_id = :profesor_id
                    AND c.dia_semana = :dia_semana
                ORDER BY 
                    c.hora_inicio;
            """
        }

    @staticmethod
    def get_queries_for_domain(domain_type: str = "type_b"):
        """Obtiene consultas optimizadas según el tipo de dominio"""
        if domain_type == "type_b":
            return DomainOptimizedQueries.get_optimized_queries_type_b()
        return {}
