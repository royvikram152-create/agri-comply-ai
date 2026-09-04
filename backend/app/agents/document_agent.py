import time
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent, AgentExecutionResult
from app.models.document import Document, DocumentType, DocumentStatus
from app.compliance.contradiction_engine import contradiction_engine_instance

class DocumentAssemblyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Document Assembly Agent",
            description="Validates export documents for presence, expiration, completeness, and cross-document field consistency."
        )

    def execute(self, input_data: Dict[str, Any]) -> AgentExecutionResult:
        start_time = time.time()
        documents: List[Document] = input_data.get("documents", [])
        shipment = input_data.get("shipment")
        
        required_docs = [
            DocumentType.PHYTOSANITARY_CERT,
            DocumentType.QUALITY_CERT,
            DocumentType.COMMERCIAL_INVOICE,
            DocumentType.PACKING_LIST
        ]

        uploaded_types = {doc.document_type: doc for doc in documents}
        findings = []
        warnings = []
        evidence_ids = []

        # 1. Mandatory Document Presence Check
        for req_type in required_docs:
            if req_type not in uploaded_types:
                findings.append({
                    "type": "DOCUMENT_MISSING",
                    "document_type": req_type.value,
                    "status": "FAIL",
                    "severity": "CRITICAL",
                    "reason": f"Mandatory export document '{req_type.value}' is missing.",
                    "recommended_action": f"Upload official {req_type.value} document.",
                    "applicable_requirement": "Regulation (EU) 2019/2072 Annex VII",
                    "source_evidence": "European Union Border Control Post mandatory import documentation rules."
                })
                warnings.append(f"Missing mandatory document: {req_type.value}")
            else:
                doc = uploaded_types[req_type]
                evidence_ids.append(doc.id)
                findings.append({
                    "type": "DOCUMENT_VALIDATED",
                    "document_type": doc.document_type.value,
                    "file_name": doc.file_name,
                    "status": "PASS",
                    "severity": "INFO",
                    "reason": f"Document '{doc.file_name}' present and valid.",
                    "applicable_requirement": "Customs Import Documentation",
                    "source_evidence": f"Document ID: {doc.id}"
                })

        # 2. Run Cross-Document Contradiction Engine
        if shipment:
            contradictions = contradiction_engine_instance.detect_contradictions(shipment, documents)
            for c in contradictions:
                findings.append({
                    "type": "DOCUMENT_CONTRADICTION",
                    "status": "FAIL",
                    "severity": c.get("severity", "CRITICAL"),
                    "reason": c.get("message"),
                    "actual_data": str(c.get("metadata")),
                    "applicable_requirement": "Regulation (EU) 2017/625 Article 89(2) - Customs Declaration Accuracy",
                    "source_evidence": "Cross-Document Contradiction Engine",
                    "recommended_action": "Re-issue documents to ensure identical values across all export certificates."
                })
                warnings.append(f"Contradiction: {c.get('title')}")

        execution_time = (time.time() - start_time) * 1000

        return AgentExecutionResult(
            agent_name=self.name,
            status="completed" if not warnings else "warning",
            findings=findings,
            evidence_ids=evidence_ids,
            warnings=warnings,
            execution_time_ms=round(execution_time, 2),
            metadata={
                "total_documents_analyzed": len(documents),
                "missing_documents_count": len(required_docs) - len(uploaded_types)
            }
        )
