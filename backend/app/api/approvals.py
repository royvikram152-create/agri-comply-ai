from fastapi import APIRouter, HTTPException, Body
from datetime import datetime, timezone
import uuid

from app.models.approval import ApprovalRequest, ApprovalRecord, ApprovalAction
from app.models.shipment import ShipmentStatus
from app.models.audit import AuditEvent
from app.database.store import store

router = APIRouter()

@router.post("/shipments/{shipment_id}/approval")
def perform_human_approval(shipment_id: str, request: ApprovalRequest):
    """
    Phase E: Human Approval Gate.
    Disabled when unresolved critical gaps exist.
    """
    if shipment_id not in store.shipments:
        raise HTTPException(status_code=404, detail="Shipment not found")

    shipment = store.shipments[shipment_id]
    
    # Check if critical violations exist
    comp_res = store.compliance_results.get(shipment_id)
    if comp_res:
        critical_count = sum(1 for f in comp_res.findings if f.get("severity") == "CRITICAL" and f.get("status") == "FAIL")
        if critical_count > 0 and request.action == ApprovalAction.APPROVE:
            raise HTTPException(
                status_code=400,
                detail=f"Human Approval BLOCKED: Cannot approve shipment while {critical_count} critical compliance gap(s) exist!"
            )

    now = datetime.now(timezone.utc)
    prev_status = shipment.status.value

    if request.action == ApprovalAction.APPROVE:
        new_status = ShipmentStatus.APPROVED.value
        shipment.status = ShipmentStatus.APPROVED
    elif request.action == ApprovalAction.REJECT:
        new_status = ShipmentStatus.REJECTED.value
        shipment.status = ShipmentStatus.REJECTED
    else:
        new_status = ShipmentStatus.REVIEW_REQUIRED.value
        shipment.status = ShipmentStatus.REVIEW_REQUIRED

    shipment.updated_at = now

    record = ApprovalRecord(
        id=f"APP-{uuid.uuid4().hex[:6].upper()}",
        shipment_id=shipment_id,
        reviewer=request.reviewer,
        action=request.action,
        comments=request.comments or "No comments provided",
        timestamp=now,
        previous_status=prev_status,
        new_status=new_status
    )

    if shipment_id not in store.approvals:
        store.approvals[shipment_id] = []
    store.approvals[shipment_id].append(record)

    # Log Audit Event
    if shipment_id not in store.audit_events:
        store.audit_events[shipment_id] = []
    store.audit_events[shipment_id].append(
        AuditEvent(
            id=f"AUD-APP-{uuid.uuid4().hex[:6]}",
            shipment_id=shipment_id,
            event_type="APPROVAL_PERFORMED",
            agent_name="Human Approval Gate",
            title=f"Human Approval Decision: {request.action.value}",
            description=f"Reviewer '{request.reviewer}' performed action '{request.action.value}'. Comments: {request.comments}",
            metadata={"reviewer": request.reviewer, "action": request.action.value},
            timestamp=now
        )
    )

    return record
