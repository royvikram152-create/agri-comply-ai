from enum import Enum
from typing import Optional
from pydantic import BaseModel

class RequirementCategory(str, Enum):
    PHYTOSANITARY = "PHYTOSANITARY"
    PLANT_HEALTH = "PLANT_HEALTH"
    PESTICIDE_MRL = "PESTICIDE_MRL"
    COMMERCIAL_DOCS = "COMMERCIAL_DOCS"
    PACKAGING = "PACKAGING"

class Requirement(BaseModel):
    requirement_id: str
    commodity: str
    destination: str
    category: RequirementCategory
    requirement: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    source: str
    source_url: str
    document: str
    page: Optional[str] = None
    effective_date: str
    evidence_text: str

class RequirementCheck(BaseModel):
    requirement_id: str
    category: RequirementCategory
    description: str
    status: str  # PASS, FAIL, WARNING
    evidence: str
    severity: str
    source: str
    source_url: str
