from fastapi import APIRouter, HTTPException
from typing import List
from app.models.audit import AuditEvent
from app.database.store import store

router = APIRouter()

@router.get("/shipments/{shipment_id}/audit", response_model=List[AuditEvent])
def get_audit_trail(shipment_id: str):
    if shipment_id not in store.shipments:
        raise HTTPException(status_code=404, detail="Shipment not found")

    return store.audit_events.get(shipment_id, [])
