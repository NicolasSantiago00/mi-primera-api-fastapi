import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base

# Base de datos de prueba para Centro Estético
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_estetica_.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def session(db):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

# FIXTURE ESPECÍFICA PARA TU DOMINIO: Centro Estético
@pytest.fixture
def sample_tratamiento_data():
    """
    Datos de ejemplo para un tratamiento en un centro estético.
    """
    return {
        "nombre_tratamiento": "Limpieza Facial Profunda",
        "descripcion": "Incluye exfoliación, vaporización, extracción de impurezas y mascarilla hidratante.",
        "duracion_minutos": 90,
        "precio": 85.50
    }

@pytest.fixture
def auth_headers(client):
    """Headers de autenticación para tests"""
    response = client.post("/auth/register", json={
        "username": "admin_estetica_",
        "password": "test123",
        "role": "admin"
    })

    login_response = client.post("/auth/login", data={
        "username": "admin_estetica_",
        "password": "test123"
    })
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}