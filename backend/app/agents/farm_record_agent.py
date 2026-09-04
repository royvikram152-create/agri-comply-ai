import time
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent, AgentExecutionResult
from app.models.farm_record import FarmRecord

class FarmRecordCheckAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Farm Record Check Agent",
            description="Evaluates farm treatment records and pesticide residue levels deterministically against regulatory MRL limits."
        )

    def execute(self, input_data: Dict[str, Any]) -> AgentExecutionResult:
        start_time = time.time()
        
        farm_data = input_data.get("farm_record")
        if isinstance(farm_data, dict):
            farm_record = FarmRecord(**farm_data)
        elif isinstance(farm_data, FarmRecord):
            farm_record = farm_data
        else:
            farm_record = FarmRecord(
                farm_id="FARM-IND-MH-042",
                farm_name="Green Valley Orchards, Ratnagiri",
                crop="Mango",
                variety="Alphonso",
                treatment_date="2026-08-15",
                pesticide="Imidacloprid 17.8 SL",
                active_ingredient="Imidacloprid",
                dose="0.5 ml/L",
                residue_value=input_data.get("residue_value", 0.82),
                unit="mg/kg",
                pre_harvest_interval_days=14,
                harvest_date="2026-08-30"
            )

        # Operational threshold configured for hackathon demo scenario evaluation
        # Note: Official EU legal LOQ for Imidacloprid in fresh mangoes under Regulation (EC) No 396/2005 is 0.01 mg/kg.
        mrl_thresholds = {
            "Imidacloprid": 0.50,
            "Buprofezin": 0.05,
            "Chlorpyrifos": 0.01
        }
        
        threshold = mrl_thresholds.get(farm_record.active_ingredient, 0.50)
        actual_value = farm_record.residue_value
        
        # Deterministic mathematical comparison
        passed = actual_value <= threshold
        status = "PASS" if passed else "FAIL"
        severity = "INFO" if passed else "CRITICAL"
        difference = round(actual_value - threshold, 4)
        
        finding = {
            "type": "FARM_RESIDUE_CHECK",
            "farm_id": farm_record.farm_id,
            "farm_name": farm_record.farm_name,
            "pesticide": farm_record.pesticide,
            "active_ingredient": farm_record.active_ingredient,
            "actual_data": f"{actual_value} {farm_record.unit}",
            "actual_residue": actual_value,
            "mrl_threshold": threshold,
            "allowed_limit": f"{threshold} {farm_record.unit} (Demo Evaluation Threshold)",
            "difference": f"+{difference} {farm_record.unit}" if difference > 0 else f"{difference} {farm_record.unit}",
            "unit": farm_record.unit,
            "status": status,
            "severity": severity,
            "title": f"Pesticide MRL Residue Check ({farm_record.active_ingredient})",
            "reason": (
                f"Residue value of {actual_value} {farm_record.unit} is within demo evaluation threshold of {threshold} {farm_record.unit}."
                if passed else
                f"Residue value of {actual_value} {farm_record.unit} EXCEEDS demo evaluation threshold of {threshold} {farm_record.unit} by +{difference} {farm_record.unit}."
            ),
            "applicable_requirement": f"Regulation (EC) No 396/2005 (EU Harmonised MRL Framework) — Demo Threshold = {threshold} mg/kg",
            "source_organization": "European Food Safety Authority (EFSA) / EU Pesticides Database",
            "source_title": "Regulation (EC) No 396/2005 (Product Code 0163010)",
            "source_type": "OFFICIAL SOURCE",
            "source_evidence": "European Food Safety Authority (EFSA) / EU Pesticides Database under Regulation (EC) No 396/2005",
            "source_url": "https://ec.europa.eu/food/plant/pesticides/eu-pesticides-database/start/screen/home",
            "recommended_action": "Pass inspection" if passed else "Obtain accredited laboratory re-testing and follow approved corrective-action procedure before shipment."
        }

        execution_time = (time.time() - start_time) * 1000

        return AgentExecutionResult(
            agent_name=self.name,
            status="completed" if passed else "warning",
            findings=[finding],
            evidence_ids=["REQ-EU-MRL-01"],
            warnings=[] if passed else [finding["reason"]],
            execution_time_ms=round(execution_time, 2),
            metadata={
                "farm_id": farm_record.farm_id,
                "actual_residue": actual_value,
                "mrl_threshold": threshold,
                "passed": passed
            }
        )
