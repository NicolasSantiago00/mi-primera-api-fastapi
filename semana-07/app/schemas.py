

from pydantic import BaseModel, Field
from datetime import time
from typing import Optional



class ClaseHorarioBase(BaseModel):
    """
    Esquema base para la información de horario de clase.
    """
    instrumento: str = Field(..., max_length=50)
    nivel: str = Field(..., max_length=50)
    dia_semana: int = Field(..., ge=1, le=7) # 1=Lunes, 7=Domingo
    hora_inicio: time
    hora_fin: time



class ClaseHorarioOptimized(ClaseHorarioBase):
    """
    DTO utilizado para la respuesta de la consulta optimizada (RAW SQL).
    Debe reflejar exactamente las columnas devueltas por la consulta.
    """
    clase_id: int
    titulo: str = Field(..., max_length=100)
    profesor_id: int
    profesor_nombre: str = Field(..., alias="profesor_nombre") 
    disponible: bool = Field(..., description="True si la clase está disponible/activa.")

    
    class Config:
        from_attributes = True


