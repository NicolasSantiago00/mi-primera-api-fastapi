# semana-07/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session # Necesaria para tipado, aunque no se use directamente aquí

# 1. IMPORTACIONES DE LA BASE DE DATOS Y CRUD (ASUMIMOS ARCHIVOS EN LA RAÍZ)
from database import Base, engine # Base y engine son necesarios para crear tablas
from crud import get_db # Lo incluimos por si hace falta, aunque no es usado en main

# 2. IMPORTACIONES DE LA OPTIMIZACIÓN Y CACHING
from app.routers import clase_optimized          # Router de la Práctica 23 (Caching)
from app.cache.domain_strategies import DomainSpecificCaching
from app.database.indexes import DomainIndexes   # 🚨 NUEVA IMPORTACIÓN (Creación de Índices)
from app.routers import optimized_domain_routes  # 🚨 NUEVA IMPORTACIÓN (Router optimizado)


# --- EVENTOS DE INICIO Y CIERRE DE LA APLICACIÓN (LIFESPAN) ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    # CÓDIGO DE INICIO (STARTUP)
    
    # 1. Crea las tablas si no existen 
    Base.metadata.create_all(bind=engine) 
    
    # 🚨 PASO 1: CREAR ÍNDICES ESPECÍFICOS DE LA PRÁCTICA 24
    print("Creando índices optimizados para el dominio (Práctica 24)...")
    DomainIndexes.create_indexes_for_domain("type_b") # Tipo B = Horarios y Disponibilidad
    
    # 2. PASO 2: Ejecuta la precarga de caché de Redis (Práctica 23)
    print("Iniciando precarga de cache de Academia de Música...")
    # Asegúrate de que el servicio Redis Server esté activo
    await DomainSpecificCaching.implement_domain_cache("edu_")
    print("Precarga de cache finalizada.")

    yield
    
    # CÓDIGO DE CIERRE (SHUTDOWN)
    print("Aplicación cerrándose...")
    
    
# --- INICIALIZACIÓN DE FASTAPI ---

app = FastAPI(
    title="Academia de Música - Optimizada (Semana 07)",
    version="1.0",
    description="API con caching Redis y optimización de DB.",
    lifespan=lifespan # Conecta los eventos de inicio y cierre
)


# --- INCLUSIÓN DE ROUTERS ---

# Conecta el router de la Práctica 23 (Caching)
app.include_router(clase_optimized.router)

# 🚨 NUEVO: Conecta el router de la Práctica 24 (Optimización DB)
app.include_router(optimized_domain_routes.router)

# Ruta simple para verificar que la app esté viva
@app.get("/")
def read_root():
    return {"status": "ok", "message": "API de Academia de Música activa con caching y DB optimizada."}
