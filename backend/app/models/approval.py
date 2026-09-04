from enum import Enum
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ApprovalAction(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    REQUEST_CORRECTION = "REQUEST_CORRECTION"

class ApprovalRequest(BaseModel):
    reviewer: str = "Senior Export Compliance Officer"
    action: ApprovalAction
    comments: Optional[str] = None

class ApprovalRecord(BaseModel):
    id: str
    shipment_id: str
    reviewer: str
    action: ApprovalAction
    comments: Optional[str] = None
    timestamp: datetime
    previous_status: str
    new_status: str
