from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class ShipmentStatus(str, Enum):
    CREATED = "CREATED"
    ANALYZING = "ANALYZING"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    HOLD = "HOLD"
    READY_FOR_APPROVAL = "READY_FOR_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class ExporterProfile(BaseModel):
    exporter_id: str = "EXP-IND-908"
    name: str = "Royal Agri Exports Ltd"
    origin_country: str = "India"
    registration_number: str = "APEDA/2024/IND-908"

class ShipmentCreate(BaseModel):
    crop: str = Field(..., json_schema_extra={"example": "Mango"})
    variety: Optional[str] = Field("Alphonso", json_schema_extra={"example": "Alphonso"})
    origin: str = Field("India", json_schema_extra={"example": "India"})
    destination: str = Field("European Union", json_schema_extra={"example": "European Union"})
    quantity_kg: float = Field(2000.0, json_schema_extra={"example": 2000.0})
    deadline_days: int = Field(7, json_schema_extra={"example": 7})
    exporter_notes: Optional[str] = None

class Shipment(BaseModel):
    id: str
    tracking_number: str
    crop: str
    variety: str
    origin: str
    destination: str
    quantity_kg: float
    deadline_days: int
    created_at: datetime
    updated_at: datetime
    status: ShipmentStatus = ShipmentStatus.CREATED
    exporter: ExporterProfile = Field(default_factory=ExporterProfile)
    compliance_score: float = 0.0
    risk_level: str = "MEDIUM"
    assessment_confidence: int = 94
