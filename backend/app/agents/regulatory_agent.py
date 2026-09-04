import time
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent, AgentExecutionResult
from app.rag.retriever import retriever_instance

class RegulatoryRetrievalAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Regulatory Retrieval Agent",
            description="Retrieves official regulatory requirements for commodity/destination pairs with evidence provenance."
        )

    def execute(self, input_data: Dict[str, Any]) -> AgentExecutionResult:
        start_time = time.time()
        crop = input_data.get("crop", "Mango")
        destination = input_data.get("destination", "European Union")
        query = f"{crop} export from India to {destination} phytosanitary pesticide MRL"

        matched_requirements = retriever_instance.search(query, top_k=5)
        
        evidence_ids = [req["requirement_id"] for req in matched_requirements]
        findings = []
        for req in matched_requirements:
            source_org = req.get("source_organization", req.get("source", "European Commission"))
            source_title = req.get("source_title", req.get("document", "Regulation"))
            findings.append({
                "type": "REGULATORY_REQUIREMENT_RETRIEVED",
                "requirement_id": req["requirement_id"],
                "category": req["category"],
                "requirement": req["requirement"],
                "severity": req["severity"],
                "source": f"{source_org} - {source_title}",
                "source_organization": source_org,
                "source_title": source_title,
                "source_type": req.get("source_type", "OFFICIAL SOURCE"),
                "source_url": req["source_url"],
                "document": req["document"],
                "page": req.get("page"),
                "evidence_text": req["evidence_text"],
                "relevance_score": req.get("relevance_score", 0.95)
            })

        execution_time = (time.time() - start_time) * 1000

        return AgentExecutionResult(
            agent_name=self.name,
            status="completed",
            findings=findings,
            evidence_ids=evidence_ids,
            warnings=[],
            execution_time_ms=round(execution_time, 2),
            metadata={"total_requirements_retrieved": len(matched_requirements)}
        )
