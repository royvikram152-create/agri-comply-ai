from datetime import datetime, timezone
from typing import Dict, Any, List
import uuid
from app.agents.exporter_agent import ExporterInteractionAgent
from app.agents.regulatory_agent import RegulatoryRetrievalAgent
from app.agents.farm_record_agent import FarmRecordCheckAgent
from app.agents.document_agent import DocumentAssemblyAgent
from app.agents.gap_reporting_agent import GapReportingAgent
from app.compliance.rule_engine import rule_engine_instance
from app.compliance.decision_engine import decision_engine_instance
from app.compliance.risk_engine import risk_engine_instance
from app.compliance.confidence_engine import confidence_engine_instance
from app.database.store import store
from app.models.compliance import ComplianceResult, DecisionCode
from app.models.audit import AuditEvent
from app.models.document import DocumentType

class AgentOrchestrator:
    def __init__(self):
        self.exporter_agent = ExporterInteractionAgent()
        self.regulatory_agent = RegulatoryRetrievalAgent()
        self.farm_agent = FarmRecordCheckAgent()
        self.document_agent = DocumentAssemblyAgent()
        self.gap_agent = GapReportingAgent()

    def run_pipeline(self, shipment_id: str, custom_residue: float = None) -> ComplianceResult:
        now = datetime.now(timezone.utc)
        shipment = store.shipments.get(shipment_id)
        if not shipment:
            raise ValueError(f"Shipment {shipment_id} not found")

        # 1. Exporter Interaction Agent
        exp_res = self.exporter_agent.execute({
            "crop": shipment.crop,
            "origin": shipment.origin,
            "destination": shipment.destination,
            "deadline_days": shipment.deadline_days,
            "quantity_kg": shipment.quantity_kg
        })

        # 2. Regulatory Retrieval Agent
        reg_res = self.regulatory_agent.execute({
            "crop": shipment.crop,
            "destination": shipment.destination
        })

        # 3. Extract evidence from uploaded real documents
        docs = store.documents.get(shipment_id, [])
        extracted_residue = custom_residue
        extracted_active_ingredient = None

        if extracted_residue is None:
            for doc in docs:
                fields = doc.extracted_fields or {}
                if doc.document_type in [DocumentType.RESIDUE_TEST_REPORT, DocumentType.FARM_TREATMENT_RECORD]:
                    res_val = fields.get("residue_value")
                    if res_val is not None and isinstance(res_val, (int, float)):
                        extracted_residue = float(res_val)
                    ai_val = fields.get("active_ingredient")
                    if ai_val and isinstance(ai_val, str) and ai_val != "Could not extract this field from uploaded evidence.":
                        extracted_active_ingredient = ai_val

        # Farm Record Check Agent
        farm_rec = store.farm_records.get(shipment_id)
        farm_input = farm_rec.model_dump() if hasattr(farm_rec, 'model_dump') else farm_rec.dict() if farm_rec else {}
        
        farm_agent_input = {
            "farm_record": farm_input,
            "extracted_residue": extracted_residue,
            "extracted_active_ingredient": extracted_active_ingredient,
            "is_demo": shipment.is_demo,
            "residue_value": custom_residue
        }
        farm_res = self.farm_agent.execute(farm_agent_input)

        # 4. Document Assembly Agent
        doc_res = self.document_agent.execute({
            "documents": docs,
            "shipment": shipment
        })

        # 5. Gap Reporting Agent
        gap_res = self.gap_agent.execute({
            "regulatory_findings": reg_res.findings,
            "farm_findings": farm_res.findings,
            "document_findings": doc_res.findings,
            "deadline_days": shipment.deadline_days
        })

        # 6. Deterministic Compliance Firewall
        rule_eval = rule_engine_instance.evaluate(gap_res.findings)
        decision_eval = decision_engine_instance.make_decision(rule_eval, gap_res.findings)

        # 7. Risk Intelligence Engine
        risk_eval = risk_engine_instance.calculate_risk(
            shipment_id=shipment_id,
            deadline_days=shipment.deadline_days,
            critical_count=rule_eval["critical_violations"],
            high_count=rule_eval["high_violations"],
            medium_count=rule_eval["medium_violations"]
        )
        store.risk_assessments[shipment_id] = risk_eval

        # 8. Deterministic Assessment Confidence Engine
        confidence_val = confidence_engine_instance.calculate_confidence(
            shipment=shipment,
            reg_findings=reg_res.findings,
            farm_findings=farm_res.findings,
            documents=docs
        )

        # 9. Update Shipment State
        shipment.status = decision_eval["shipment_status"]
        shipment.compliance_score = rule_eval["compliance_score"]
        shipment.risk_level = risk_eval.risk_level
        shipment.assessment_confidence = confidence_val
        shipment.updated_at = now

        findings_summary = {
            "pass": rule_eval["passed_checks"],
            "fail": rule_eval["critical_violations"] + rule_eval["high_violations"],
            "warning": rule_eval["medium_violations"] + rule_eval["low_violations"]
        }

        result = ComplianceResult(
            shipment_id=shipment_id,
            overall_status=decision_eval["decision_code"],
            decision_reason=decision_eval["decision_reason"],
            compliance_score=rule_eval["compliance_score"],
            assessment_confidence=confidence_val,
            risk_level=risk_eval.risk_level,
            findings=gap_res.findings,
            summary=findings_summary,
            evaluated_at=now
        )
        store.compliance_results[shipment_id] = result

        # 10. Record Pipeline Audit Event
        audit_event = AuditEvent(
            id=f"AUD-RUN-{uuid.uuid4().hex[:6]}",
            shipment_id=shipment_id,
            event_type="PIPELINE_EXECUTED",
            agent_name="Agent Orchestrator",
            title="Multi-Agent Pipeline Execution Completed",
            description=f"Pipeline finished with status '{decision_eval['decision_code'].value}'. Reason: {decision_eval['decision_reason']}",
            metadata={
                "compliance_score": rule_eval["compliance_score"],
                "assessment_confidence": confidence_val,
                "decision_code": decision_eval["decision_code"].value,
                "critical_violations": rule_eval["critical_violations"]
            },
            timestamp=now
        )
        if shipment_id not in store.audit_events:
            store.audit_events[shipment_id] = []
        store.audit_events[shipment_id].append(audit_event)

        return result

orchestrator_instance = AgentOrchestrator()
