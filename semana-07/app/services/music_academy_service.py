# app/services/music_academy_service.py
import asyncio
from datetime import datetime



async def get_class_schedules(day: str):
    """Simula consulta de horarios de clases para un día"""
    await asyncio.sleep(1)  # Simula latencia
    return {
        "day": day,
        "schedules": [
            {"time": "06:00 PM - 07:00 PM", "class": "Piano Individual", "teacher": "Prof. López"},
            {"time": "07:00 PM - 08:00 PM", "class": "Guitarra Grupal", "teacher": "Prof. García"}
        ]
    }

async def get_teacher_availability(teacher_id: str):
    """Simula disponibilidad de un profesor"""
    await asyncio.sleep(1)  # Simula latencia
    return {
        "teacher_id": teacher_id,
        "available_slots": ["2025-10-03 06:00 PM", "2025-10-03 07:00 PM"]
    }

async def get_instrument_catalog():
    """Simula catálogo de instrumentos"""
    await asyncio.sleep(1)  # Simula latencia
    return {
        "instruments": ["Piano", "Guitarra", "Violín", "Batería"]
    }
