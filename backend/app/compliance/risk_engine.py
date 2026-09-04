from typing import Dict, Any, List
from app.models.compliance import RiskAssessment

class RiskIntelligenceEngine:
    """
    Calculates system-generated operational risk score, deadline buffer, and remediation timeline.
    Clearly designated as operational risk (not an official government rating).
    """
    def calculate_risk(
        self,
        shipment_id: str,
        deadline_days: int,
        critical_count: int,
        high_count: int,
        medium_count: int
    ) -> RiskAssessment:
        
        estimated_remediation_days = 0
        if critical_count > 0:
            estimated_remediation_days += 3  # Lab residue testing takes ~3 days
        if high_count > 0:
            estimated_remediation_days += 1  # Document re-issue takes ~1 day

        deadline_buffer_days = deadline_days - estimated_remediation_days
        
        if deadline_buffer_days < 1 or critical_count > 0:
            risk_level = "HIGH"
            risk_score = 78.5
        elif high_count > 0 or deadline_days <= 3:
            risk_level = "MEDIUM"
            risk_score = 45.0
        else:
            risk_level = "LOW"
            risk_score = 12.0

        timeline_steps = [
            {
                "step": 1,
                "label": "TODAY",
                "status": "COMPLETED",
                "description": "Shipment registered & compliance audit initiated."
            },
            {
                "step": 2,
                "label": "Corrective Action",
                "status": "PENDING" if critical_count > 0 else "SKIPPED",
                "description": "Perform pesticide residue lab re-testing (Est. 2 days)"
            },
            {
                "step": 3,
                "label": "Document Revalidation",
                "status": "PENDING" if high_count > 0 or critical_count > 0 else "COMPLETED",
                "description": "Upload updated lab test report & re-issue APEDA cert."
            },
            {
                "step": 4,
                "label": "Human Approval",
                "status": "PENDING",
                "description": "Senior Export Compliance Officer sign-off."
            },
            {
                "step": 5,
                "label": "SHIPMENT DEADLINE",
                "status": "SCHEDULED",
                "description": f"Port dispatch deadline in {deadline_days} days."
            }
        ]

        return RiskAssessment(
            shipment_id=shipment_id,
            risk_score=risk_score,
            risk_level=risk_level,
            deadline_days_remaining=deadline_days,
            estimated_remediation_days=estimated_remediation_days,
            deadline_buffer_days=deadline_buffer_days,
            timeline_steps=timeline_steps
        )

risk_engine_instance = RiskIntelligenceEngine()
