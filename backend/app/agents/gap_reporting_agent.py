import time
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent, AgentExecutionResult
from app.models.compliance import SeverityLevel

class GapReportingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Gap Reporting Agent",
            description="Aggregates multi-agent compliance findings, ranks severity, and generates evidence-backed gap reports with recommended remediation actions."
        )

    def execute(self, input_data: Dict[str, Any]) -> AgentExecutionResult:
        start_time = time.time()
        
        regulatory_findings = input_data.get("regulatory_findings", [])
        farm_findings = input_data.get("farm_findings", [])
        document_findings = input_data.get("document_findings", [])
        deadline_days = input_data.get("deadline_days", 7)

        all_findings = []
        
        # Add farm findings that failed
        for f in farm_findings:
            if f.get("status") == "FAIL":
                ai = f.get('active_ingredient', 'Pesticide')
                title = f"Pesticide MRL Violation ({ai})"
                all_findings.append({
                    "id": "GAP-FARM-01",
                    "category": "FARM_RECORD",
                    "title": title,
                    "severity": f.get("severity", "CRITICAL"),
                    "status": "FAIL",
                    "reason": f.get("reason", "Residue exceeds limit"),
                    "actual_data": f.get("actual_data") or (f"{f.get('actual_residue')} {f.get('unit', 'mg/kg')}" if f.get('actual_residue') is not None else "Could not extract this field from uploaded evidence."),
                    "allowed_limit": f.get("allowed_limit"),
                    "difference": f.get("difference"),
                    "applicable_requirement": f.get("applicable_requirement", "EU MRL Regulation"),
                    "source_evidence": f.get("source_evidence", "EFSA Database"),
                    "source_type": f.get("source_type", "OFFICIAL SOURCE"),
                    "source_url": f.get("source_url"),
                    "recommended_action": f.get("recommended_action", "Re-test residue before shipment"),
                    "deadline_impact_days": 3,
                    "resolved": False
                })

        # Add document findings that failed
        for f in document_findings:
            if f.get("status") == "FAIL":
                cat = "DOCUMENT"
                is_missing = (f.get("type") == "DOCUMENT_MISSING")
                doc_type = f.get("document_type", "Document")
                title = f"Missing Mandatory Document ({doc_type})" if is_missing else "Document Contradiction"
                
                actual = f.get("actual_data")
                if is_missing:
                    actual = f"No uploaded document classified as {doc_type}."
                elif not actual:
                    actual = doc_type

                all_findings.append({
                    "id": f"GAP-DOC-{len(all_findings)+1:02d}",
                    "category": cat,
                    "title": title,
                    "severity": f.get("severity", "HIGH"),
                    "status": "FAIL",
                    "reason": f.get("reason"),
                    "document_type": doc_type,
                    "file_name": f.get("file_name"),
                    "actual_data": actual,
                    "applicable_requirement": f.get("applicable_requirement"),
                    "source_evidence": f.get("source_evidence") or ("No uploaded evidence. European Union Border Control Post rules." if is_missing else "Uploaded export certificates"),
                    "source_type": f.get("source_type", "APPLICATION/DOCUMENT RULE"),
                    "recommended_action": f.get("recommended_action"),
                    "deadline_impact_days": 2,
                    "resolved": False
                })

        # Add deadline risk if tight
        if deadline_days <= 3:
            all_findings.append({
                "id": "GAP-TIME-01",
                "category": "DEADLINE",
                "title": "Imminent Shipment Deadline Risk",
                "severity": "HIGH",
                "status": "WARNING",
                "reason": f"Only {deadline_days} days remaining until shipping deadline.",
                "actual_data": f"{deadline_days} days remaining",
                "applicable_requirement": "Port Dispatch Protocol",
                "source_evidence": "Customs Export Schedule",
                "source_type": "APPLICATION/DOCUMENT RULE",
                "recommended_action": "Expedite document revalidation and priority phytosanitary clearance.",
                "deadline_impact_days": 1,
                "resolved": False
            })

        # Rank findings by severity: CRITICAL -> HIGH -> MEDIUM -> LOW
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
        all_findings.sort(key=lambda x: severity_order.get(x["severity"], 5))

        execution_time = (time.time() - start_time) * 1000

        return AgentExecutionResult(
            agent_name=self.name,
            status="completed",
            findings=all_findings,
            evidence_ids=[f["id"] for f in all_findings],
            warnings=[f"{f['title']}: {f['reason']}" for f in all_findings if f["severity"] in ["CRITICAL", "HIGH"]],
            execution_time_ms=round(execution_time, 2),
            metadata={
                "total_gaps_identified": len(all_findings),
                "critical_gaps_count": sum(1 for f in all_findings if f["severity"] == "CRITICAL")
            }
        )
