from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class SeverityLevel(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class DecisionCode(str, Enum):
    READY = "READY"
    REVIEW = "REVIEW"
    HOLD = "HOLD"
    BLOCKED = "BLOCKED"
    READY_FOR_APPROVAL = "READY_FOR_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class ComplianceFinding(BaseModel):
    id: str
    category: str  # REGULATORY, FARM_RECORD, DOCUMENT, DEADLINE
    title: str
    severity: SeverityLevel
    status: str  # PASS, FAIL, WARNING
    reason: str
    actual_data: str
    applicable_requirement: str
    source_evidence: str
    source_url: Optional[str] = None
    recommended_action: str
    deadline_impact_days: int = 0
    resolved: bool = False

class ComplianceResult(BaseModel):
    shipment_id: str
    overall_status: DecisionCode
    decision_reason: str
    compliance_score: float  # 0 to 100
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    findings: List[ComplianceFinding]
    summary: Dict[str, int]  # count of pass, fail, warning
    evaluated_at: datetime

class RiskAssessment(BaseModel):
    shipment_id: str
    risk_score: float  # 0 to 100
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    deadline_days_remaining: int
    estimated_remediation_days: int
    deadline_buffer_days: int
    timeline_steps: List[Dict[str, Any]]
