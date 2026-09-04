from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class DocumentType(str, Enum):
    PHYTOSANITARY_CERT = "PHYTOSANITARY_CERT"
    QUALITY_CERT = "QUALITY_CERT"
    COMMERCIAL_INVOICE = "COMMERCIAL_INVOICE"
    PACKING_LIST = "PACKING_LIST"
    RESIDUE_TEST_REPORT = "RESIDUE_TEST_REPORT"
    BILL_OF_LADING = "BILL_OF_LADING"

class DocumentStatus(str, Enum):
    VALID = "VALID"
    EXPIRED = "EXPIRED"
    CONTRADICTION = "CONTRADICTION"
    MISSING = "MISSING"
    PENDING = "PENDING"

class Document(BaseModel):
    id: str
    shipment_id: str
    document_type: DocumentType
    file_name: str
    file_path: Optional[str] = None
    uploaded_at: datetime
    status: DocumentStatus = DocumentStatus.PENDING
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    extracted_fields: Dict[str, Any] = {}

class DocumentValidationResult(BaseModel):
    document_type: DocumentType
    present: bool
    status: DocumentStatus
    expiry_check: str
    field_validations: Dict[str, str]
    issues: list[str] = []
