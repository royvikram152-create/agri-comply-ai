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
    FARM_TREATMENT_RECORD = "FARM_TREATMENT_RECORD"
    CERTIFICATE_OF_ORIGIN = "CERTIFICATE_OF_ORIGIN"
    SUPPORTING_DOC = "SUPPORTING_DOC"

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
    extracted_text: Optional[str] = None
    provenance_map: Dict[str, Any] = {}
    file_format: Optional[str] = None
    file_size: Optional[int] = None
    classification_confidence: float = 1.0

class DocumentValidationResult(BaseModel):
    document_type: DocumentType
    present: bool
    status: DocumentStatus
    expiry_check: str
    field_validations: Dict[str, str]
    issues: list[str] = []
