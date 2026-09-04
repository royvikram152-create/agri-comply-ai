from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["mode"] == "DEMO_ZERO_COST"

def test_list_shipments():
    response = client.get("/api/shipments")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["id"] == "SHP-MANGO-001"

def test_get_shipment_details():
    response = client.get("/api/shipments/SHP-MANGO-001")
    assert response.status_code == 200
    data = response.json()
    assert data["crop"] == "Mango"
    assert data["destination"] == "European Union"

def test_get_compliance_details():
    response = client.get("/api/shipments/SHP-MANGO-001/compliance")
    assert response.status_code == 200
    data = response.json()
    assert "compliance_result" in data

def test_get_evidence_chain():
    response = client.get("/api/shipments/SHP-MANGO-001/evidence")
    assert response.status_code == 200
    data = response.json()
    assert "evidence_chain" in data
