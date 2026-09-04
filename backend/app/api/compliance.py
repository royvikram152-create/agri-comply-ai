from fastapi import APIRouter, HTTPException
from app.database.store import store
from app.models.compliance import ComplianceResult
from app.rag.knowledge_base import EU_MANGO_REGULATIONS

router = APIRouter()

@router.get("/shipments/{shipment_id}/compliance")
def get_compliance_details(shipment_id: str):
    if shipment_id not in store.shipments:
        raise HTTPException(status_code=404, detail="Shipment not found")

    result = store.compliance_results.get(shipment_id)
    risk = store.risk_assessments.get(shipment_id)
    remediation = store.remediation_history.get(shipment_id)

    return {
        "shipment_id": shipment_id,
        "shipment": store.shipments[shipment_id],
        "compliance_result": result,
        "risk_assessment": risk,
        "remediation_history": remediation
    }

@router.get("/shipments/{shipment_id}/evidence")
def get_evidence_chain(shipment_id: str):
    if shipment_id not in store.shipments:
        raise HTTPException(status_code=404, detail="Shipment not found")

    shipment = store.shipments[shipment_id]
    farm = store.farm_records.get(shipment_id)

    evidence_items = []
    if farm:
        threshold = 0.50
        passed = farm.residue_value <= threshold
        evidence_items.append({
            "id": "EVI-MRL-01",
            "decision": "FAIL" if not passed else "PASS",
            "title": f"Pesticide MRL residue evaluation ({farm.active_ingredient})",
            "reason": f"Residue value {farm.residue_value} mg/kg vs operational threshold {threshold} mg/kg.",
            "actual_data": f"{farm.residue_value} mg/kg (Active Ingredient: {farm.active_ingredient})",
            "allowed_limit": f"{threshold} mg/kg",
            "difference": f"+{round(farm.residue_value - threshold, 4)} mg/kg" if not passed else "0 mg/kg",
            "applicable_requirement": f"Regulation (EC) No 396/2005 (EU Harmonised MRL Framework)",
            "source_evidence": "European Food Safety Authority (EFSA) / EU Pesticides Database under Regulation (EC) No 396/2005",
            "source_type": "OFFICIAL SOURCE",
            "source_url": "https://ec.europa.eu/food/plant/pesticides/eu-pesticides-database/start/screen/home",
            "rule_evaluation": "CRIT-MRL-01 -> HOLD" if not passed else "CRIT-MRL-01 -> PASS",
            "final_status": shipment.status.value
        })

    return {
        "shipment_id": shipment_id,
        "evidence_chain": evidence_items,
        "regulatory_corpus": EU_MANGO_REGULATIONS
    }
