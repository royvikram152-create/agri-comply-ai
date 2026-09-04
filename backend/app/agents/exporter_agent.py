import time
import re
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent, AgentExecutionResult

class ExporterInteractionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Exporter Interaction Agent",
            description="Parses natural language exporter shipment requests and extracts structured trade metadata."
        )

    def execute(self, input_data: Dict[str, Any]) -> AgentExecutionResult:
        start_time = time.time()
        text = input_data.get("raw_input", "")
        
        # Rule-based natural language extraction
        crop = input_data.get("crop")
        if not crop:
            if re.search(r'\bmango(es)?\b', text, re.IGNORECASE):
                crop = "Mango"
            elif re.search(r'\bgrape(s)?\b', text, re.IGNORECASE):
                crop = "Grape"
            elif re.search(r'\brice\b', text, re.IGNORECASE):
                crop = "Rice"

        origin = input_data.get("origin")
        if not origin:
            if re.search(r'\b(india|ind)\b', text, re.IGNORECASE):
                origin = "India"

        destination = input_data.get("destination")
        if not destination:
            if re.search(r'\b(eu|european union|europe)\b', text, re.IGNORECASE):
                destination = "European Union"

        deadline_days = input_data.get("deadline_days")
        if not deadline_days:
            if re.search(r'\bnext week\b', text, re.IGNORECASE) or re.search(r'\b7 days?\b', text, re.IGNORECASE):
                deadline_days = 7
            elif re.search(r'\bin 3 days?\b', text, re.IGNORECASE):
                deadline_days = 3
            else:
                deadline_days = 7

        quantity_kg = input_data.get("quantity_kg")

        missing_information = []
        if not crop:
            missing_information.append("crop")
        if not origin:
            missing_information.append("origin")
        if not destination:
            missing_information.append("destination")
        if not quantity_kg:
            missing_information.append("quantity_kg")

        extracted_metadata = {
            "crop": crop or "Mango",
            "variety": input_data.get("variety", "Alphonso"),
            "origin": origin or "India",
            "destination": destination or "European Union",
            "deadline_days": deadline_days or 7,
            "quantity_kg": quantity_kg or 2000.0,
            "missing_information": missing_information
        }

        execution_time = (time.time() - start_time) * 1000

        return AgentExecutionResult(
            agent_name=self.name,
            status="completed" if not missing_information else "warning",
            findings=[
                {
                    "type": "SHIPMENT_METADATA_EXTRACTED",
                    "extracted": extracted_metadata,
                    "missing": missing_information
                }
            ],
            evidence_ids=["EXP-INT-001"],
            warnings=[f"Missing required parameter: {item}" for item in missing_information],
            execution_time_ms=round(execution_time, 2),
            metadata=extracted_metadata
        )
