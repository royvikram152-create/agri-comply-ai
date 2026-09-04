from fastapi import APIRouter, HTTPException, Body
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid

from app.models.shipment import Shipment, ShipmentCreate, ShipmentStatus, ExporterProfile
from app.models.farm_record import FarmRecord
from app.models.document import Document, DocumentType, DocumentStatus
from app.models.compliance import ComplianceResult
from app.models.audit import AuditEvent
from app.database.store import store
from app.orchestration.orchestrator import orchestrator_instance

router = APIRouter()

@router.get("/shipments", response_model=List[Shipment])
def list_shipments():
    return list(store.shipments.values())

@router.post("/shipments", response_model=Shipment)
def create_shipment(payload: ShipmentCreate):
    now = datetime.now(timezone.utc)
    shipment_id = f"SHP-{uuid.uuid4().hex[:6].upper()}"
    tracking_no = f"AGRI-{now.strftime('%Y')}-{uuid.uuid4().hex[:4].upper()}"
    
    shipment = Shipment(
        id=shipment_id,
        tracking_number=tracking_no,
        crop=payload.crop,
        variety=payload.variety or "Standard",
        origin=payload.origin,
        destination=payload.destination,
        quantity_kg=payload.quantity_kg,
        deadline_days=payload.deadline_days,
        created_at=now,
        updated_at=now,
        status=ShipmentStatus.CREATED,
        exporter=ExporterProfile(
            exporter_id="EXP-IND-908",
            name="Royal Agri Exports Ltd",
            origin_country=payload.origin,
            registration_number="APEDA/2024/IND-908"
        ),
        compliance_score=0.0,
        risk_level="MEDIUM",
        assessment_confidence=94
    )
    
    store.shipments[shipment_id] = shipment
    store.documents[shipment_id] = []
    store.audit_events[shipment_id] = [
        AuditEvent(
            id=f"AUD-{uuid.uuid4().hex[:6]}",
            shipment_id=shipment_id,
            event_type="SHIPMENT_CREATED",
            agent_name="Exporter Interaction Agent",
            title="Shipment Created",
            description=f"New export shipment registered for {payload.crop} ({payload.origin} -> {payload.destination})",
            timestamp=now
        )
    ]
    
    return shipment

@router.get("/shipments/{shipment_id}", response_model=Shipment)
def get_shipment(shipment_id: str):
    if shipment_id not in store.shipments:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return store.shipments[shipment_id]

@router.post("/shipments/{shipment_id}/analyze")
def analyze_shipment(shipment_id: str):
    if shipment_id not in store.shipments:
        raise HTTPException(status_code=404, detail="Shipment not found")
    
    result = orchestrator_instance.run_pipeline(shipment_id)
    return {
        "message": "Analysis pipeline executed successfully",
        "compliance_result": result,
        "shipment": store.shipments[shipment_id]
    }

@router.post("/shipments/{shipment_id}/remediate")
def remediate_shipment(shipment_id: str, payload: Dict[str, Any] = Body(...)):
    """
    Phase H: "What Changed?" remediation trigger.
    Uploads/simulates new passing residue test (e.g., residue = 0.31 mg/kg).
    Re-evaluates compliance pipeline and records BEFORE vs ACTION vs AFTER transition.
    """
    if shipment_id not in store.shipments:
        raise HTTPException(status_code=404, detail="Shipment not found")

    before_status = store.shipments[shipment_id].status.value
    before_score = store.shipments[shipment_id].compliance_score
    
    new_residue = payload.get("residue_value", 0.31)
    
    # Update farm record
    if shipment_id in store.farm_records:
        store.farm_records[shipment_id].residue_value = new_residue
    
    now = datetime.now(timezone.utc)
    res_doc = Document(
        id=f"DOC-RES-{uuid.uuid4().hex[:4]}",
        shipment_id=shipment_id,
        document_type=DocumentType.RESIDUE_TEST_REPORT,
        file_name="NABL_Lab_Residue_Test_Report_PASS.pdf",
        uploaded_at=now,
        status=DocumentStatus.VALID,
        issue_date=now.strftime("%Y-%m-%d"),
        expiry_date="2026-10-01",
        extracted_fields={
            "laboratory": "NABL Accredited Export Quality Control Lab, Mumbai",
            "active_ingredient": "Imidacloprid",
            "residue_value": new_residue,
            "unit": "mg/kg",
            "mrl_threshold": 0.50,
            "test_result": "PASS"
        }
    )
    if shipment_id not in store.documents:
        store.documents[shipment_id] = []
    
    store.documents[shipment_id] = [d for d in store.documents[shipment_id] if d.document_type != DocumentType.RESIDUE_TEST_REPORT]
    store.documents[shipment_id].append(res_doc)

    # Re-run Orchestrator Pipeline
    result = orchestrator_instance.run_pipeline(shipment_id, custom_residue=new_residue)
    
    after_status = store.shipments[shipment_id].status.value
    after_score = store.shipments[shipment_id].compliance_score

    remediation_summary = {
        "shipment_id": shipment_id,
        "before": {
            "status": before_status,
            "compliance_score": before_score,
            "critical_gaps": 1 if before_status == "HOLD" else 0,
            "residue_value": 0.82
        },
        "action": {
            "type": "RESIDUE_TEST_UPLOADED",
            "document_name": "NABL_Lab_Residue_Test_Report_PASS.pdf",
            "new_residue_value": new_residue,
            "unit": "mg/kg"
        },
        "after": {
            "status": after_status,
            "compliance_score": after_score,
            "critical_gaps": 0,
            "residue_value": new_residue
        },
        "transition_summary": f"Residue re-test passed ({new_residue} mg/kg <= 0.50 mg/kg demo evaluation threshold). Official legal framework: Regulation (EC) No 396/2005. Compliance status updated from {before_status} to {after_status}!"
    }
    
    store.remediation_history[shipment_id] = remediation_summary

    store.audit_events[shipment_id].append(
        AuditEvent(
            id=f"AUD-REM-{uuid.uuid4().hex[:6]}",
            shipment_id=shipment_id,
            event_type="REMEDIATION_PERFORMED",
            agent_name="Document Assembly Agent",
            title="Passing Residue Test Uploaded",
            description=f"Uploaded lab test showing Imidacloprid residue at {new_residue} mg/kg. Compliance status upgraded to READY FOR APPROVAL.",
            metadata=remediation_summary,
            timestamp=now
        )
    )

    return remediation_summary

@router.post("/shipments/{shipment_id}/what-if")
def simulate_what_if(shipment_id: str, payload: Dict[str, Any] = Body(...)):
    """
    Phase K: Non-destructive What-If simulation mode.
    Simulates parameter changes against the compliance engine.
    Does NOT mutate the real shipment state or real assessment_confidence!
    """
    if shipment_id not in store.shipments:
        raise HTTPException(status_code=404, detail="Shipment not found")

    real_shipment = store.shipments[shipment_id]
    farm_rec = store.farm_records.get(shipment_id)
    real_residue = farm_rec.residue_value if farm_rec else 0.82

    sim_destination = payload.get("destination", "European Union")
    sim_deadline = payload.get("deadline_days", 7)
    sim_residue = payload.get("residue_value", 0.31)

    passed = sim_residue <= 0.50
    sim_score = 100.0 if passed else 72.0
    sim_status = "READY_FOR_APPROVAL" if passed else "HOLD"
    sim_confidence = 94 if passed else 89

    return {
        "shipment_id": shipment_id,
        "is_simulation": True,
        "current_real_shipment": {
            "status": real_shipment.status.value,
            "compliance_score": real_shipment.compliance_score,
            "assessment_confidence": real_shipment.assessment_confidence,
            "risk_level": real_shipment.risk_level,
            "residue_value": real_residue,
            "unit": "mg/kg"
        },
        "parameters": {
            "destination": sim_destination,
            "deadline_days": sim_deadline,
            "residue_value": sim_residue
        },
        "simulated_outcome": {
            "compliance_score": sim_score,
            "simulated_assessment_confidence": sim_confidence,
            "status": sim_status,
            "critical_gaps": 0 if passed else 1,
            "risk_level": "LOW" if passed else "HIGH"
        }
    }
