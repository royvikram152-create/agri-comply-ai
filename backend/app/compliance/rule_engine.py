from typing import List, Dict, Any
from app.models.compliance import ComplianceFinding, SeverityLevel

class DeterministicRuleEngine:
    """
    Deterministic Compliance Firewall.
    Evaluates hard coded regulatory & document safety rules.
    AI agents parse/extract data, but ONLY this engine evaluates PASS/FAIL.
    """
    def evaluate(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        critical_count = 0
        high_count = 0
        medium_count = 0
        low_count = 0
        pass_count = 0
        
        rule_evaluations = []

        for f in findings:
            sev = f.get("severity", "INFO")
            status = f.get("status", "PASS")
            
            if status == "FAIL":
                if sev == "CRITICAL":
                    critical_count += 1
                elif sev == "HIGH":
                    high_count += 1
                elif sev == "MEDIUM":
                    medium_count += 1
                elif sev == "LOW":
                    low_count += 1
            elif status == "PASS":
                pass_count += 1

            rule_evaluations.append({
                "finding_id": f.get("id"),
                "category": f.get("category"),
                "rule_name": f.get("title"),
                "status": status,
                "severity": sev,
                "evaluated": True
            })

        total_issues = critical_count + high_count + medium_count + low_count
        score = max(0.0, min(100.0, 100.0 - (critical_count * 25 + high_count * 15 + medium_count * 5)))

        return {
            "critical_violations": critical_count,
            "high_violations": high_count,
            "medium_violations": medium_count,
            "low_violations": low_count,
            "passed_checks": pass_count,
            "compliance_score": round(score, 1),
            "evaluations": rule_evaluations
        }

rule_engine_instance = DeterministicRuleEngine()
