from fastapi.testclient import TestClient
from app.main import app
from app.database.store import store

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

def test_initial_082_residue_produces_hold():
    """Regression Test 1: Initial residue 0.82 mg/kg produces HOLD status."""
    client.post("/api/shipments/SHP-MANGO-001/analyze")
    response = client.get("/api/shipments/SHP-MANGO-001/compliance")
    assert response.status_code == 200
    data = response.json()
    comp_res = data["compliance_result"]
    assert comp_res["overall_status"] == "HOLD"
    assert comp_res["compliance_score"] < 100.0
    farm_gaps = [f for f in comp_res["findings"] if f.get("category") == "FARM_RECORD"]
    assert len(farm_gaps) > 0
    assert "Imidacloprid" in farm_gaps[0]["title"]

def test_remediation_031_upgrades_to_ready_for_approval():
    """Regression Test 2: Uploading 0.31 mg/kg passing residue upgrades status to READY_FOR_APPROVAL."""
    response = client.post("/api/shipments/SHP-MANGO-001/remediate", json={"residue_value": 0.31})
    assert response.status_code == 200
    rem_data = response.json()
    assert rem_data["after"]["status"] == "READY_FOR_APPROVAL"
    assert rem_data["after"]["compliance_score"] == 100.0

    shp_res = client.get("/api/shipments/SHP-MANGO-001")
    assert shp_res.json()["status"] == "READY_FOR_APPROVAL"

def test_human_approval_transitions_to_approved():
    """Regression Test 3: Human approval transitions status to APPROVED."""
    approval_payload = {
        "reviewer": "Senior Export Compliance Officer (APEDA/EU)",
        "action": "APPROVE",
        "comments": "All mandatory phytosanitary and lab residue checks cleared cleanly."
    }
    app_res = client.post("/api/shipments/SHP-MANGO-001/approval", json=approval_payload)
    assert app_res.status_code == 200
    app_data = app_res.json()
    assert app_data["new_status"] == "APPROVED"

    shp_res = client.get("/api/shipments/SHP-MANGO-001")
    assert shp_res.json()["status"] == "APPROVED"

def test_non_destructive_what_if_while_approved():
    """
    Regression Test 4 & 5: What-If simulation with 0.82 mg/kg while real shipment is APPROVED.
    - Simulation returns HOLD outcome.
    - Real shipment state remains APPROVED!
    - Current-state display in response contains real persisted shipment data (APPROVED / 100).
    """
    what_if_payload = {
        "destination": "European Union",
        "deadline_days": 7,
        "residue_value": 0.82
    }
    sim_res = client.post("/api/shipments/SHP-MANGO-001/what-if", json=what_if_payload)
    assert sim_res.status_code == 200
    data = sim_res.json()
    
    # Simulation outcome is HOLD
    assert data["simulated_outcome"]["status"] == "HOLD"
    
    # Real shipment state in response and database store remains APPROVED!
    assert data["current_real_shipment"]["status"] == "APPROVED"
    assert data["current_real_shipment"]["compliance_score"] == 100.0
    
    # Verify database store real shipment was NOT mutated by What-If
    real_shipment = client.get("/api/shipments/SHP-MANGO-001").json()
    assert real_shipment["status"] == "APPROVED"
    assert real_shipment["compliance_score"] == 100.0

def test_audit_trail_preserves_remediation_and_approval_events():
    """Regression Test 6: Audit trail records remediation and approval events."""
    audit_res = client.get("/api/shipments/SHP-MANGO-001/audit")
    assert audit_res.status_code == 200
    events = audit_res.json()
    event_types = [e["event_type"] for e in events]
    assert "REMEDIATION_PERFORMED" in event_types
    assert "APPROVAL_PERFORMED" in event_types
