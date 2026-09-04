from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class AuditEvent(BaseModel):
    id: str
    shipment_id: str
    event_type: str  # AGENT_EXECUTION, RULE_EVALUATION, FINDING_CREATED, STATUS_CHANGED, DOCUMENT_UPLOADED, APPROVAL_PERFORMED
    agent_name: Optional[str] = None
    title: str
    description: str
    metadata: Dict[str, Any] = {}
    timestamp: datetime
