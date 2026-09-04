from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from app.models.shipment import Shipment, ShipmentStatus, ExporterProfile
from app.models.document import Document, DocumentType, DocumentStatus
from app.models.farm_record import FarmRecord
from app.models.compliance import ComplianceResult, ComplianceFinding, SeverityLevel, DecisionCode, RiskAssessment
from app.models.audit import AuditEvent
from app.models.approval import ApprovalRecord

class DataStore:
    def __init__(self):
        self.shipments: Dict[str, Shipment] = {}
        self.documents: Dict[str, List[Document]] = {}
        self.farm_records: Dict[str, FarmRecord] = {}
        self.compliance_results: Dict[str, ComplianceResult] = {}
        self.risk_assessments: Dict[str, RiskAssessment] = {}
        self.audit_events: Dict[str, List[AuditEvent]] = {}
        self.approvals: Dict[str, List[ApprovalRecord]] = {}
        self.remediation_history: Dict[str, Dict[str, Any]] = {}
        
        self.seed_demo_data()

    def seed_demo_data(self):
        # Demo Shipment 1: SHP-MANGO-001 (Mango India -> EU, 7 days)
        shipment_id = "SHP-MANGO-001"
        now = datetime.now(timezone.utc)
        
        shipment = Shipment(
            id=shipment_id,
            tracking_number="AGRI-2026-EU-9081",
            crop="Mango",
            variety="Alphonso",
            origin="India",
            destination="European Union",
            quantity_kg=2000.0,
            deadline_days=7,
            created_at=now,
            updated_at=now,
            status=ShipmentStatus.HOLD,
            exporter=ExporterProfile(
                exporter_id="EXP-IND-908",
                name="Royal Agri Exports Ltd",
                origin_country="India",
                registration_number="APEDA/2024/IND-908"
            ),
            compliance_score=72.0,
            risk_level="HIGH",
            assessment_confidence=94,
            is_demo=True
        )
        self.shipments[shipment_id] = shipment
        
        # Demo Documents
        docs = [
            Document(
                id="DOC-PHYTO-001",
                shipment_id=shipment_id,
                document_type=DocumentType.PHYTOSANITARY_CERT,
                file_name="Phytosanitary_Certificate_IN908.pdf",
                uploaded_at=now,
                status=DocumentStatus.VALID,
                issue_date="2026-08-28",
                expiry_date="2026-09-15",
                extracted_fields={
                    "certificate_number": "IN-PHYTO-2026-4421",
                    "commodity": "Fresh Mangoes (Mangifera indica)",
                    "quantity_kg": 2000.0,
                    "origin": "India",
                    "destination": "European Union (Rotterdam)",
                    "treatment": "Vapour Heat Treatment (VHT) at 48°C for 60 min"
                }
            ),
            Document(
                id="DOC-QUAL-001",
                shipment_id=shipment_id,
                document_type=DocumentType.QUALITY_CERT,
                file_name="APEDA_Quality_Grading_Report.pdf",
                uploaded_at=now,
                status=DocumentStatus.VALID,
                issue_date="2026-08-29",
                expiry_date="2026-09-29",
                extracted_fields={
                    "certificate_number": "APEDA-Q-8821",
                    "grade": "Class I Export",
                    "brix_level": "16.5° Brix",
                    "inspection_result": "PASS"
                }
            ),
            Document(
                id="DOC-INV-001",
                shipment_id=shipment_id,
                document_type=DocumentType.COMMERCIAL_INVOICE,
                file_name="Commercial_Invoice_INV202609.pdf",
                uploaded_at=now,
                status=DocumentStatus.VALID,
                issue_date="2026-08-30",
                expiry_date="2026-10-30",
                extracted_fields={
                    "invoice_number": "INV-2026-0901",
                    "quantity_kg": 2000.0,
                    "buyer": "EuroAgri Imports BV, Netherlands",
                    "total_value_eur": 18500.0
                }
            ),
            Document(
                id="DOC-PACK-001",
                shipment_id=shipment_id,
                document_type=DocumentType.PACKING_LIST,
                file_name="Export_Packing_List.pdf",
                uploaded_at=now,
                status=DocumentStatus.VALID,
                issue_date="2026-08-30",
                expiry_date="2026-10-30",
                extracted_fields={
                    "packing_list_number": "PL-2026-0901",
                    "total_boxes": 400,
                    "quantity_kg": 2000.0,
                    "packaging_type": "Corrugated Fiberboard Boxes with ventilation"
                }
            )
        ]
        self.documents[shipment_id] = docs
        
        # Farm Record (Initial Non-compliant residue: 0.82 mg/kg vs MRL 0.50 mg/kg)
        self.farm_records[shipment_id] = FarmRecord(
            farm_id="FARM-IND-MH-042",
            farm_name="Green Valley Orchards, Ratnagiri",
            crop="Mango",
            variety="Alphonso",
            treatment_date="2026-08-15",
            pesticide="Imidacloprid 17.8 SL",
            active_ingredient="Imidacloprid",
            dose="0.5 ml/L",
            residue_value=0.82,  # EXCEEDS EU MRL threshold (0.50 mg/kg)
            unit="mg/kg",
            pre_harvest_interval_days=14,
            harvest_date="2026-08-30"
        )
        
        # Initial Audit log timeline
        self.audit_events[shipment_id] = [
            AuditEvent(
                id="AUD-001",
                shipment_id=shipment_id,
                event_type="SHIPMENT_CREATED",
                agent_name="Exporter Interaction Agent",
                title="Shipment Created",
                description="Exporter registered shipment SHP-MANGO-001 (Mango, 2000 kg, India -> EU, 7 days deadline)",
                metadata={"quantity": 2000, "deadline": 7},
                timestamp=now
            ),
            AuditEvent(
                id="AUD-002",
                shipment_id=shipment_id,
                event_type="AGENT_EXECUTION",
                agent_name="Regulatory Retrieval Agent",
                title="Regulatory Requirements Retrieved",
                description="Retrieved EU Regulation (EU) 2019/2072 and MRL thresholds for Mangoes from India.",
                metadata={"requirements_count": 5},
                timestamp=now
            ),
            AuditEvent(
                id="AUD-003",
                shipment_id=shipment_id,
                event_type="AGENT_EXECUTION",
                agent_name="Farm Record Check Agent",
                title="Farm Pesticide Check Failed",
                description="Detected active ingredient Imidacloprid residue at 0.82 mg/kg exceeding EU MRL threshold (0.50 mg/kg).",
                metadata={"residue": 0.82, "threshold": 0.50},
                timestamp=now
            ),
            AuditEvent(
                id="AUD-004",
                shipment_id=shipment_id,
                event_type="RULE_EVALUATION",
                agent_name="Deterministic Rule Engine",
                title="Deterministic Compliance Firewall Evaluated",
                description="Rule CRIT-MRL-01 triggered HOLD status due to critical residue threshold violation.",
                metadata={"rule_id": "CRIT-MRL-01", "decision": "HOLD"},
                timestamp=now
            )
        ]
        
        self.approvals[shipment_id] = []

store = DataStore()
