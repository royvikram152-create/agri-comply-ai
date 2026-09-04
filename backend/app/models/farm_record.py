from typing import Optional
from pydantic import BaseModel

class FarmRecord(BaseModel):
    farm_id: str = "FARM-IND-MH-042"
    farm_name: str = "Green Valley Orchards, Ratnagiri"
    crop: str = "Mango"
    variety: str = "Alphonso"
    treatment_date: str = "2026-08-15"
    pesticide: str = "Imidacloprid 17.8 SL"
    active_ingredient: str = "Imidacloprid"
    dose: str = "0.5 ml/L"
    residue_value: float  # e.g., 0.82 or 0.31 mg/kg
    unit: str = "mg/kg"
    pre_harvest_interval_days: int = 14
    harvest_date: str = "2026-08-30"

class ResidueCheckResult(BaseModel):
    pesticide: str
    active_ingredient: str
    residue_value: float
    mrl_threshold: float
    unit: str
    status: str  # PASS or FAIL
    severity: str  # HIGH, MEDIUM, LOW
    source: str
    source_url: str
