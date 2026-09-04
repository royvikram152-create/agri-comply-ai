from typing import Dict, Any, List
from app.models.shipment import ShipmentStatus
from app.models.compliance import DecisionCode

class ComplianceDecisionEngine:
    """
    Final Shipment Decision Engine.
    Enforces non-negotiable status transitions based on deterministic evaluation.
    """
    def make_decision(self, evaluation: Dict[str, Any], findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        critical = evaluation.get("critical_violations", 0)
        high = evaluation.get("high_violations", 0)
        medium = evaluation.get("medium_violations", 0)

        if critical > 0:
            status = ShipmentStatus.HOLD
            decision_code = DecisionCode.HOLD
            reason = f"Shipment placed on HOLD due to {critical} CRITICAL compliance violation(s) (e.g. pesticide MRL breach or missing mandatory phytosanitary certificate)."
        elif high > 0:
            status = ShipmentStatus.REVIEW_REQUIRED
            decision_code = DecisionCode.REVIEW
            reason = f"Shipment requires REVIEW due to {high} HIGH severity finding(s) (e.g. cross-document weight contradiction)."
        elif medium > 0:
            status = ShipmentStatus.REVIEW_REQUIRED
            decision_code = DecisionCode.REVIEW
            reason = f"Shipment requires REVIEW due to {medium} UNRESOLVED warning(s)."
        else:
            status = ShipmentStatus.READY_FOR_APPROVAL
            decision_code = DecisionCode.READY_FOR_APPROVAL
            reason = "All mandatory regulatory, farm, and document checks PASSED cleanly. Shipment is READY FOR HUMAN APPROVAL."

        return {
            "shipment_status": status,
            "decision_code": decision_code,
            "decision_reason": reason,
            "approval_eligible": (critical == 0 and high == 0)
        }

decision_engine_instance = ComplianceDecisionEngine()
