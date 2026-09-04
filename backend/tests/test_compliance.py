import pytest
from app.compliance.rule_engine import rule_engine_instance
from app.compliance.decision_engine import decision_engine_instance
from app.models.shipment import ShipmentStatus
from app.models.compliance import DecisionCode

def test_deterministic_rule_engine_evaluation():
    findings = [
        {
            "id": "GAP-1",
            "category": "FARM_RECORD",
            "title": "MRL Breach",
            "severity": "CRITICAL",
            "status": "FAIL"
        }
    ]
    eval_res = rule_engine_instance.evaluate(findings)
    assert eval_res["critical_violations"] == 1
    assert eval_res["compliance_score"] < 100.0

    dec_res = decision_engine_instance.make_decision(eval_res, findings)
    assert dec_res["shipment_status"] == ShipmentStatus.HOLD
    assert dec_res["decision_code"] == DecisionCode.HOLD

def test_passing_compliance_decision():
    findings = []
    eval_res = rule_engine_instance.evaluate(findings)
    dec_res = decision_engine_instance.make_decision(eval_res, findings)
    assert dec_res["shipment_status"] == ShipmentStatus.READY_FOR_APPROVAL
    assert dec_res["decision_code"] == DecisionCode.READY_FOR_APPROVAL
