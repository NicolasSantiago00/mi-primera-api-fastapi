# 🚨 CORRECCIÓN CLAVE: Importación directa de la raíz
# Asume que 'database.py' está en el mismo nivel que la carpeta 'app'
from database import Base, engine

from sqlalchemy import text, inspect
from sqlalchemy.engine import Connection


class DomainIndexes:
    """
    Clase responsable de crear índices específicos en la base de datos 
    para optimizar consultas de dominios específicos (Práctica 24).
    """

    @staticmethod
    def create_indexes_for_domain(domain_type: str):
        """
        Crea índices optimizados basados en el tipo de dominio.

        Args:
            domain_type (str): El tipo de optimización a aplicar ('type_b' en este caso).
        """
        print("-" * 50)
        
        # 1. Conexión a la base de datos
        with engine.begin() as connection:
            connection: Connection # Tipado para claridad
            
            # 2. Obtener lista de índices existentes para evitar duplicados
            inspector = inspect(engine)
            
            # --- TIPO B: OPTIMIZACIÓN PARA HORARIOS Y DISPONIBILIDAD ---
            if domain_type == 'type_b':
                
                # 2.1. Índice en 'clases' para buscar por 'instrumento' y 'nivel' (clave foránea común)
                index_name_1 = "idx_clase_instr_nivel"
                # Usar el nombre de la tabla de la clase si existe, sino usar 'clases'
                table_name = Base.metadata.tables.get('clases', None) or 'clases'
                
                if index_name_1 not in inspector.get_index_names(table_name):
                    print(f"-> Creando índice: {index_name_1} en tabla '{table_name}'")
                    # Índice compuesto para consultas de disponibilidad
                    connection.execute(text(
                        f"CREATE INDEX {index_name_1} ON {table_name} (instrumento, nivel);"
                    ))
                    
                # 2.2. Índice en 'horarios' para buscar por 'dia_semana'
                index_name_2 = "idx_horarios_dia"
                table_name_2 = Base.metadata.tables.get('horarios', None) or 'horarios'

                if index_name_2 not in inspector.get_index_names(table_name_2):
                    print(f"-> Creando índice: {index_name_2} en tabla '{table_name_2}'")
                    connection.execute(text(
                        f"CREATE INDEX {index_name_2} ON {table_name_2} (dia_semana);"
                    ))

                print(f"✅ Índices para el dominio '{domain_type}' creados/verificados con éxito.")
                
            else:
                print(f"⚠️ Tipo de dominio '{domain_type}' no reconocido. No se crearon índices.")
        
        print("-" * 50)

# FIN DEL ARCHIVO
