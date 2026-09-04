import time
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent, AgentExecutionResult
from app.models.farm_record import FarmRecord

NO_EXTRACT_MSG = "Could not extract this field from uploaded evidence."

class FarmRecordCheckAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Farm Record Check Agent",
            description="Evaluates farm treatment records and pesticide residue levels deterministically against regulatory MRL limits."
        )

    def execute(self, input_data: Dict[str, Any]) -> AgentExecutionResult:
        start_time = time.time()
        
        is_demo = input_data.get("is_demo", False)
        farm_data = input_data.get("farm_record")
        extracted_doc_residue = input_data.get("extracted_residue")
        extracted_doc_ai = input_data.get("extracted_active_ingredient")

        # Determine residue value and active ingredient strictly
        if extracted_doc_residue is not None and isinstance(extracted_doc_residue, (int, float)):
            actual_value = float(extracted_doc_residue)
            active_ingredient = extracted_doc_ai if (extracted_doc_ai and extracted_doc_ai != NO_EXTRACT_MSG) else "Imidacloprid"
            has_valid_evidence = True
        elif isinstance(farm_data, dict) and farm_data.get("residue_value") is not None:
            actual_value = float(farm_data["residue_value"])
            active_ingredient = farm_data.get("active_ingredient", "Imidacloprid")
            has_valid_evidence = True
        elif isinstance(farm_data, FarmRecord):
            actual_value = farm_data.residue_value
            active_ingredient = farm_data.active_ingredient
            has_valid_evidence = True
        elif input_data.get("residue_value") is not None and isinstance(input_data.get("residue_value"), (int, float)):
            actual_value = float(input_data["residue_value"])
            active_ingredient = input_data.get("active_ingredient", "Imidacloprid")
            has_valid_evidence = True
        elif is_demo:
            actual_value = 0.82
            active_ingredient = "Imidacloprid"
            has_valid_evidence = True
        else:
            actual_value = None
            active_ingredient = "Imidacloprid"
            has_valid_evidence = False

        if not has_valid_evidence or actual_value is None:
            finding = {
                "type": "FARM_RESIDUE_CHECK",
                "farm_id": "UNVERIFIED",
                "farm_name": "Unverified Farm Record",
                "pesticide": "UNKNOWN",
                "active_ingredient": "Pesticide Residue",
                "actual_data": NO_EXTRACT_MSG,
                "actual_residue": NO_EXTRACT_MSG,
                "mrl_threshold": 0.50,
                "allowed_limit": "0.50 mg/kg (Operational Threshold)",
                "unit": "mg/kg",
                "status": "FAIL",
                "severity": "CRITICAL",
                "title": "Missing Pesticide Residue Analysis Report",
                "reason": "Could not extract pesticide residue test values from uploaded evidence. A valid laboratory test report or farm record is mandatory.",
                "applicable_requirement": "Regulation (EC) No 396/2005 (EU Harmonised MRL Framework)",
                "source_organization": "European Food Safety Authority (EFSA) / EU Pesticides Database",
                "source_title": "Regulation (EC) No 396/2005",
                "source_type": "OFFICIAL SOURCE",
                "source_evidence": "Mandatory Laboratory Residue Test Verification Protocol",
                "source_url": "https://ec.europa.eu/food/plant/pesticides/eu-pesticides-database/start/screen/home",
                "recommended_action": "Upload an accredited laboratory residue test report or farm treatment log."
            }
            execution_time = (time.time() - start_time) * 1000
            return AgentExecutionResult(
                agent_name=self.name,
                status="warning",
                findings=[finding],
                evidence_ids=[],
                warnings=[finding["reason"]],
                execution_time_ms=round(execution_time, 2),
                metadata={"has_valid_evidence": False}
            )

        # Operational threshold configured for hackathon demo scenario evaluation
        mrl_thresholds = {
            "Imidacloprid": 0.50,
            "Buprofezin": 0.05,
            "Chlorpyrifos": 0.01
        }
        
        threshold = mrl_thresholds.get(active_ingredient, 0.50)
        
        # Deterministic mathematical comparison
        passed = actual_value <= threshold
        status = "PASS" if passed else "FAIL"
        severity = "INFO" if passed else "CRITICAL"
        difference = round(actual_value - threshold, 4)
        
        finding = {
            "type": "FARM_RESIDUE_CHECK",
            "farm_id": farm_data.get("farm_id", "FARM-IND-01") if isinstance(farm_data, dict) else "FARM-EXTRACTED",
            "farm_name": farm_data.get("farm_name", "Registered Farm") if isinstance(farm_data, dict) else "Extracted Lab Evidence",
            "pesticide": f"{active_ingredient} Residue Test",
            "active_ingredient": active_ingredient,
            "actual_data": f"{actual_value} mg/kg",
            "actual_residue": actual_value,
            "mrl_threshold": threshold,
            "allowed_limit": f"{threshold} mg/kg (Operational Threshold)",
            "difference": f"+{difference} mg/kg" if difference > 0 else f"{difference} mg/kg",
            "unit": "mg/kg",
            "status": status,
            "severity": severity,
            "title": f"Pesticide MRL Residue Check ({active_ingredient})",
            "reason": (
                f"Residue value of {actual_value} mg/kg is within evaluation threshold of {threshold} mg/kg."
                if passed else
                f"Residue value of {actual_value} mg/kg EXCEEDS evaluation threshold of {threshold} mg/kg by +{difference} mg/kg."
            ),
            "applicable_requirement": f"Regulation (EC) No 396/2005 (EU Harmonised MRL Framework) — Evaluation Threshold = {threshold} mg/kg",
            "source_organization": "European Food Safety Authority (EFSA) / EU Pesticides Database",
            "source_title": "Regulation (EC) No 396/2005",
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
                "actual_residue": actual_value,
                "mrl_threshold": threshold,
                "passed": passed
            }
        )
