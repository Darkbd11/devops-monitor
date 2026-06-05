from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

# On va bypasser l'authentification par variable d'environnement pour le test,
# on définit une clé API statique.
import os
os.environ["API_KEY"] = "super-secret"
HEADERS = {"X-API-Key": "super-secret"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_metrics_route():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "cpu_percent" in data

def test_add_server_unauthorized():
    payload = {"name": "Test Server", "host": "localhost", "port": 8080}
    response = client.post("/servers", json=payload)
    assert response.status_code == 403

def test_add_and_list_server():
    payload = {"name": "Test Server", "host": "localhost", "port": 8080}
    
    # Création
    response = client.post("/servers", json=payload, headers=HEADERS)
    assert response.status_code == 201
    server_data = response.json()
    assert server_data["name"] == "Test Server"
    server_id = server_data["id"]
    
    # Liste
    res_list = client.get("/servers")
    assert res_list.status_code == 200
    assert len(res_list.json()) >= 1
    
    # Suppression
    res_del = client.delete(f"/servers/{server_id}", headers=HEADERS)
    assert res_del.status_code == 204

def test_delete_nonexistent_server():
    response = client.delete("/servers/invalid-id", headers=HEADERS)
    assert response.status_code == 404

def test_check_server():
    # Ajouter un serveur d'abord
    payload = {"name": "Test Server Check", "host": "localhost", "port": 8000}
    response = client.post("/servers", json=payload, headers=HEADERS)
    server_id = response.json()["id"]

    # Checker
    res_check = client.post(f"/servers/{server_id}/check")
    assert res_check.status_code == 200
    assert "status" in res_check.json()

def test_check_nonexistent_server():
    response = client.post("/servers/invalid-id/check")
    assert response.status_code == 404

def test_websocket_metrics():
    with client.websocket_connect("/ws/metrics") as websocket:
        data = websocket.receive_json()
        assert "cpu_percent" in data
        assert "memory_percent" in data
        assert "disk_percent" in data
