import pytest
from fastapi.testclient import TestClient

# Asumiendo que esta es tu aplicación principal
from main import app

class TestEsteticaAuth:
    
    def test_register_estetica_user(self, client):
        """Test de registro de un nuevo cliente en el centro estético."""
        data = {
            "username": "cliente_nuevo",
            "password": "password123",
            "role": "cliente"  # Rol específico para un cliente
        }

        response = client.post("/auth/register", json=data)
        assert response.status_code == 201
        assert "id" in response.json()
    
    def test_register_esteticista_user(self, client):
        """Test de registro de un esteticista."""
        data = {
            "username": "esteticista_sofia",
            "password": "password123",
            "role": "esteticista"  # Rol para un esteticista
        }

        response = client.post("/auth/register", json=data)
        assert response.status_code == 201
        assert "id" in response.json()

    def test_login_estetica_user(self, client):
        """Test de login de un usuario del centro estético."""
        # Primero, registrar al usuario
        register_data = {
            "username": "admin_estetica",
            "password": "admin123",
            "role": "admin"  # Rol de administrador
        }
        client.post("/auth/register", json=register_data)

        # Intentar login con las credenciales correctas
        login_data = {
            "username": "admin_estetica",
            "password": "admin123"
        }
        response = client.post("/auth/login", data=login_data)

        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_invalid_credentials(self, client):
        """Test de login con credenciales incorrectas."""
        login_data = {
            "username": "usuario_inexistente",
            "password": "password_incorrecta"
        }
        response = client.post("/auth/login", data=login_data)
        
        assert response.status_code == 401
        assert "Credenciales inválidas" in response.json()["detail"]

    def test_create_tratamiento_requires_auth(self, client, sample_tratamiento_data):
        """Test que crear un tratamiento requiere autenticación."""
        response = client.post("/estetica_tratamientos/", json=sample_tratamiento_data)
        assert response.status_code == 401
    
    def test_admin_can_delete_tratamiento(self, client, auth_headers):
        """Test que solo un administrador puede eliminar un tratamiento."""
        # Crear un tratamiento para eliminar
        create_data = {
            "nombre_tratamiento": "Tratamiento a Eliminar",
            "descripcion": "Descripción",
            "duracion_minutos": 30,
            "precio": 50.00
        }
        create_response = client.post("/estetica_tratamientos/", json=create_data, headers=auth_headers)
        tratamiento_id = create_response.json()["id"]

        # Intentar eliminar con rol de admin
        response = client.delete(f"/estetica_tratamientos/{tratamiento_id}", headers=auth_headers)
        assert response.status_code == 200

    def test_esteticista_cannot_delete_tratamiento(self, client, esteticista_headers):
        """Test que un esteticista no puede eliminar tratamientos."""
        # Crear un tratamiento como admin para que un esteticista intente eliminarlo
        admin_headers = self.get_admin_headers(client) # Suponiendo una fixture para obtener headers de admin
        create_data = {
            "nombre_tratamiento": "Tratamiento a Eliminar por Esteticista",
            "descripcion": "Descripción",
            "duracion_minutos": 30,
            "precio": 50.00
        }
        create_response = client.post("/estetica_tratamientos/", json=create_data, headers=admin_headers)
        tratamiento_id = create_response.json()["id"]

        # Intentar eliminar con rol de esteticista
        response = client.delete(f"/estetica_tratamientos/{tratamiento_id}", headers=esteticista_headers)
        assert response.status_code == 403