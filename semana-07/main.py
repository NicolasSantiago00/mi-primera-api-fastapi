from fastapi import FastAPI, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers.music_academy_optimized import router as music_router
from app.routers.optimized_domain_routes import router as optimized_router
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.monitoring.metrics import APIMetrics, monitor_performance
from app.monitoring.profiler import APIProfiler
from app.monitoring.alerts import AlertManager, AlertRule, email_alert
import time
from app.middleware.domain_rate_limiter import DomainRateLimiter
from app.middleware.domain_logger import DomainLogger
from app.middleware.domain_validator import DomainValidator
import redis

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = "sqlite:///./academia.db"  # Cambia esto según tu DB (ej. PostgreSQL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})  # Para SQLite
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configuración de la aplicación FastAPI
app = FastAPI(title="Academia de Música API - Semana 07", description="API optimizada con Redis para horarios y disponibilidad")

# Middleware para CORS (opcional, si necesitas acceso desde otros dominios)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajusta según tus necesidades
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de Práctica 25 (Rate Limiter, Logger, Validator)
redis_client = redis.Redis(host='localhost', port=6379, db=0)
DOMAIN_PREFIX = "edu_"

app.add_middleware(DomainValidator, domain_prefix=DOMAIN_PREFIX)
app.add_middleware(DomainLogger, domain_prefix=DOMAIN_PREFIX)
app.add_middleware(DomainRateLimiter, domain_prefix=DOMAIN_PREFIX, redis_client=redis_client)

# Inicializar sistemas de monitoring (Práctica 26)
metrics = APIMetrics(
    app_name="academia-musica-api",
    domain=DOMAIN_PREFIX
)

profiler = APIProfiler(domain=DOMAIN_PREFIX)

alert_manager = AlertManager(domain=DOMAIN_PREFIX)


# Configurar alertas específicas para Academia de Música
alert_manager.add_rule(AlertRule(
    name=f"{DOMAIN_PREFIX}high_response_time_horarios",
    metric_name="response_time",
    threshold=2.0,  # 2 segundos en consultas de horarios
    comparison="gt",
    duration=60,    # 1 minuto
    action=email_alert
))

alert_manager.add_rule(AlertRule(
    name=f"{DOMAIN_PREFIX}high_cpu_reservas",
    metric_name="cpu_usage",
    threshold=80.0,  # 80% CPU durante reservas
    comparison="gt",
    duration=120,    # 2 minutos
    action=email_alert
))

# Middleware para métricas automáticas (Práctica 26)
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    metrics.record_request(
        method=request.method,
        endpoint=str(request.url.path),
        status=response.status_code,
        duration=duration
    )

    # Verificar alertas cada 10 requests (simplificado)
    if int(time.time()) % 10 == 0:
        metrics.update_system_metrics()
        alert_manager.check_alerts({
            'response_time': duration,
           
        })

    return response

# Tarea en background para métricas del sistema
