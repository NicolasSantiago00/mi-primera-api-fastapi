# semana-07/app/routers/optimized_domain_routes.py
from fastapi import APIRouter

router = APIRouter(prefix="/edu")

@router.get("/class/booking")
async def book_class():
    return {"message": "Reserva de clase exitosa"}

@router.get("/schedule")
async def get_schedule():
    return {"message": "Consulta de horarios exitosa"}

@router.get("/teacher/availability")
async def get_teacher_availability():
    return {"message": "Disponibilidad de profesores exitosa"}

@router.get("/admin")
async def admin_action():
    return {"message": "Acción administrativa exitosa"}