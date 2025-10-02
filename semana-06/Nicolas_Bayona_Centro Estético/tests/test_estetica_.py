import pytest
from fastapi.testclient import TestClient

class TestEsteticaAPI:
    """
    Tests para la API del Centro Estético - FICHA 3147246
    """

    def test_create_tratamiento_success(self, client, sample_tratamiento_data, auth_headers):
        """Test de creación exitosa de un tratamiento."""
        response = client.post(
            f"/estetica_tratamientos/",
            json=sample_tratamiento_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()

        # Validaciones específicas del Centro Estético
        assert "nombre_tratamiento" in data
        assert data["nombre_tratamiento"] == sample_tratamiento_data["nombre_tratamiento"]
        assert data["precio"] == sample_tratamiento_data["precio"]
        assert data["duracion_minutos"] == sample_tratamiento_data["duracion_minutos"]

    def test_get_tratamiento_not_found(self, client, auth_headers):
        """Test para un tratamiento no encontrado."""
        response = client.get(f"/estetica_tratamientos/999", headers=auth_headers)

        assert response.status_code == 404
        assert "Tratamiento no encontrado" in response.json()["detail"]

    def test_tratamiento_validation_error(self, client, auth_headers):
        """Test de validación con datos de tratamiento inválidos."""
        invalid_data = {
            "nombre_tratamiento": "", # Campo requerido vacío
            "duracion_minutos": -10, # Valor inválido
            "precio": 0 # Precio debe ser mayor a 0
        }

        response = client.post(
            f"/estetica_tratamientos/",
            json=invalid_data,
            headers=auth_headers
        )

        assert response.status_code == 422
        errors = response.json()["detail"]

        # Validar errores específicos del Centro Estético
        assert any("nombre_tratamiento" in str(error) for error in errors)
        assert any("duracion_minutos" in str(error) for error in errors)
        assert any("precio" in str(error) for error in errors)
def test_create_tratamiento_complete(self, client, auth_headers):
    """Test completo de creación para un nuevo tratamiento."""
    data = {
        "nombre_tratamiento": "Masaje Relajante de Espalda",
        "descripcion": "Masaje de 45 minutos para aliviar la tensión muscular y reducir el estrés.",
        "duracion_minutos": 45,
        "precio": 60.00
    }

    response = client.post(f"/estetica_tratamientos/", json=data, headers=auth_headers)

    assert response.status_code == 201
    created = response.json()

    # Validaciones específicas del Centro Estético
    assert created["nombre_tratamiento"] == data["nombre_tratamiento"]
    assert "id" in created
    assert created["duracion_minutos"] == data["duracion_minutos"]
    assert created["precio"] == data["precio"]

def test_create_tratamiento_duplicate(self, client, auth_headers):
    """Test de creación duplicada de un tratamiento."""
    data = {
        "nombre_tratamiento": "Masaje de Piedras Calientes",
        "descripcion": "Masaje con piedras volcánicas.",
        "duracion_minutos": 75,
        "precio": 95.00
    }

    # Crear por primera vez
    client.post(f"/estetica_tratamientos/", json=data, headers=auth_headers)

    # Intentar crear duplicado (asumiendo que el nombre es único)
    response = client.post(f"/estetica_tratamientos/", json=data, headers=auth_headers)

    assert response.status_code == 400
    assert "tratamiento con este nombre ya existe" in response.json()["detail"].lower()

def test_get_tratamiento_by_id(self, client, auth_headers):
    """Test de consulta por ID para un tratamiento."""
    # Crear un tratamiento primero
    create_data = {
        "nombre_tratamiento": "Tratamiento con Radiofrecuencia",
        "descripcion": "Tratamiento facial para tensar la piel.",
        "duracion_minutos": 60,
        "precio": 120.00
    }
    create_response = client.post(f"/estetica_tratamientos/", json=create_data, headers=auth_headers)
    created_id = create_response.json()["id"]

    # Consultar por ID
    response = client.get(f"/estetica_tratamientos/{created_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_id
    assert data["nombre_tratamiento"] == create_data["nombre_tratamiento"]

def test_get_all_tratamientos(self, client, auth_headers):
    """Test de consulta de todos los tratamientos."""
    response = client.get(f"/estetica_tratamientos/", headers=auth_headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_tratamiento_not_found(self, client, auth_headers):
    """Test de tratamiento no encontrado."""
    response = client.get(f"/estetica_tratamientos/99999", headers=auth_headers)

    assert response.status_code == 404
    assert "tratamiento no encontrado" in response.json()["detail"].lower()

# tests/test_estetica_.py - Agregar al archivo existente

def test_update_tratamiento_complete(self, client, auth_headers):
    """Test de actualización completa para un tratamiento."""
    # Crear un tratamiento inicial
    create_data = {
        "nombre_tratamiento": "Depilación con Láser",
        "descripcion": "Sesión de depilación en piernas completas.",
        "duracion_minutos": 40,
        "precio": 80.00
    }
    create_response = client.post(f"/estetica_tratamientos/", json=create_data, headers=auth_headers)
    entity_id = create_response.json()["id"]

    # Datos de actualización para el tratamiento
    update_data = {
        "nombre_tratamiento": "Depilación con Láser de Diodo",
        "descripcion": "Sesión de depilación de alta potencia.",
        "duracion_minutos": 35,
        "precio": 90.00
    }

    response = client.put(f"/estetica_tratamientos/{entity_id}", json=update_data, headers=auth_headers)

    assert response.status_code == 200
    updated = response.json()

    # Validar que los campos se han actualizado correctamente
    assert updated["id"] == entity_id
    assert updated["nombre_tratamiento"] == update_data["nombre_tratamiento"]
    assert updated["precio"] == update_data["precio"]

# tests/test_estetica_.py - Agregar al archivo existente

def test_delete_tratamiento_success(self, client, auth_headers):
    """Test de eliminación exitosa de un tratamiento."""
    # Crear un tratamiento para eliminar
    create_data = {
        "nombre_tratamiento": "Manicura y Pedicura",
        "descripcion": "Servicio de cuidado completo de uñas de manos y pies.",
        "duracion_minutos": 100,
        "precio": 45.00
    }
    create_response = client.post(f"/estetica_tratamientos/", json=create_data, headers=auth_headers)
    entity_id = create_response.json()["id"]

    # Eliminar
    response = client.delete(f"/estetica_tratamientos/{entity_id}", headers=auth_headers)

    assert response.status_code == 200

    # Verificar que ya no existe
    get_response = client.get(f"/estetica_tratamientos/{entity_id}", headers=auth_headers)
    assert get_response.status_code == 404

def test_delete_tratamiento_not_found(self, client, auth_headers):
    """Test de eliminación de un tratamiento inexistente."""
    response = client.delete(f"/estetica_tratamientos/99999", headers=auth_headers)

    assert response.status_code == 404

# tests/test_estetica_.py - Agregar al archivo existente

def test_tratamiento_business_rules_validation(self, client, auth_headers):
    """Test de reglas de negocio para la creación de un tratamiento."""
    # Intentar crear un tratamiento con precio negativo
    invalid_data = {
        "nombre_tratamiento": "Masaje de Prueba",
        "descripcion": "Test de regla de negocio.",
        "duracion_minutos": 60,
        "precio": -10.00
    }

    response = client.post(f"/estetica_tratamientos/", json=invalid_data, headers=auth_headers)

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("precio" in str(error) and "mayor a 0" in str(error) for error in errors)
    
    # Intentar crear un tratamiento con duración no razonable
    invalid_data_2 = {
        "nombre_tratamiento": "Tratamiento Rápido",
        "descripcion": "Duración de 5 minutos.",
        "duracion_minutos": 5, # Asumiendo una regla de negocio que la duración mínima es 15
        "precio": 25.00
    }
    
    response_2 = client.post(f"/estetica_tratamientos/", json=invalid_data_2, headers=auth_headers)
    
    assert response_2.status_code == 422
    errors_2 = response_2.json()["detail"]
    assert any("duracion_minutos" in str(error) for error in errors_2)