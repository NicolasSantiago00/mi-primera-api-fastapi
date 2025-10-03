from sqlalchemy import Index, text
from database import engine  # Asume que 'engine' se importa desde la raíz

class DomainIndexes:
    """Índices específicos para optimizar consultas de la Academia de Música (Tipo B)"""

    @staticmethod
    def create_domain_type_b_indexes():
        """
        Índices para dominios tipo B (horarios y disponibilidad).
        Acelera búsquedas por Instrumento, Nivel, Día y Profesor.
        """
        indexes = [
            # CRÍTICO: Búsquedas de clases por instrumento y nivel (combinado)
            "CREATE INDEX IF NOT EXISTS idx_clase_instrumento_nivel ON clase(instrumento_id, nivel_id);",
            
            # CRÍTICO: Consultas de disponibilidad por día y hora (para horarios)
            "CREATE INDEX IF NOT EXISTS idx_clase_horario_inicio ON clase(dia_semana, hora_inicio);",
            
            # Búsquedas por profesor
            "CREATE INDEX IF NOT EXISTS idx_clase_profesor ON clase(profesor_id, dia_semana);",
            
            # Índices en catálogos
            "CREATE INDEX IF NOT EXISTS idx_instrumento_nombre ON instrumento(nombre);",
        ]
        return indexes

    @staticmethod
    def get_domain_indexes(domain_type: str = "type_b"):
        """Obtiene índices específicos según el tipo de dominio"""
        if domain_type == "type_b":
            return DomainIndexes.create_domain_type_b_indexes()
        else:
            return []

    @staticmethod
    def create_indexes_for_domain(domain_type: str = "type_b"):
        """Crea índices específicos para tu dominio"""
        indexes = DomainIndexes.get_domain_indexes(domain_type)
        
        try:
            with engine.connect() as connection:
                for index_sql in indexes:
                    try:
                        # Usa 'text' para ejecutar Raw SQL
                        connection.execute(text(index_sql))
                        connection.commit()
                        print(f"✅ Índice creado: {index_sql[:50]}...")
                    except Exception as e:
                        # Esto podría ocurrir si la tabla no existe aún, pero lo manejamos
                        print(f"❌ Error creando índice '{index_sql[:20]}...': {e}")
        except Exception as e:
            print(f"❌ Error al conectar a la base de datos para crear índices: {e}")
