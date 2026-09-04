import pytest
from app.agents.exporter_agent import ExporterInteractionAgent
from app.agents.regulatory_agent import RegulatoryRetrievalAgent
from app.agents.farm_record_agent import FarmRecordCheckAgent
from app.agents.document_agent import DocumentAssemblyAgent
from app.agents.gap_reporting_agent import GapReportingAgent
from app.models.document import Document, DocumentType, DocumentStatus
from datetime import datetime, timezone

def test_exporter_agent_extraction():
    agent = ExporterInteractionAgent()
    result = agent.execute({
        "raw_input": "I am exporting mangoes from India to the EU next week."
    })
    assert result.status in ["completed", "warning"]
    assert result.metadata["crop"] == "Mango"
    assert result.metadata["origin"] == "India"
    assert result.metadata["destination"] == "European Union"

def test_regulatory_agent_retrieval():
    agent = RegulatoryRetrievalAgent()
    result = agent.execute({
        "crop": "Mango",
        "destination": "European Union"
    })
    assert len(result.findings) > 0
    assert "REQ-EU-PHYTO-01" in result.evidence_ids or "REQ-EU-MRL-01" in result.evidence_ids

def test_farm_record_agent_deterministic_comparison():
    agent = FarmRecordCheckAgent()
    # Failing case (0.82 > 0.50)
    fail_res = agent.execute({"residue_value": 0.82})
    assert fail_res.findings[0]["status"] == "FAIL"
    assert fail_res.findings[0]["severity"] == "CRITICAL"

    # Passing case (0.31 <= 0.50)
    pass_res = agent.execute({"residue_value": 0.31})
    assert pass_res.findings[0]["status"] == "PASS"

def test_document_agent_validation():
    agent = DocumentAssemblyAgent()
    now = datetime.now(timezone.utc)
    docs = [
        Document(
            id="DOC-1",
            shipment_id="SHP-1",
            document_type=DocumentType.PHYTOSANITARY_CERT,
            file_name="Phyto.pdf",
            uploaded_at=now,
            status=DocumentStatus.VALID,
            extracted_fields={"quantity_kg": 2000.0}
        )
    ]
    res = agent.execute({"documents": docs})
    # Should flag missing mandatory commercial invoice and packing list
    assert res.metadata["missing_documents_count"] > 0
