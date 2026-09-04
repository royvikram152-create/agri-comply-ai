import pytest
import io
import json
from fastapi.testclient import TestClient
from app.main import app
from app.database.store import store

client = TestClient(app)

def create_sample_pdf(text_lines: list) -> bytes:
    """Helper to generate a valid raw PDF 1.4 in memory."""
    content = " ".join(text_lines)
    stream_data = f"BT /F1 12 Tf 50 700 Td ({content}) Tj ET"
    pdf_str = f"""%PDF-1.4
1 0 obj <</Type /Catalog /Pages 2 0 R>> endobj
2 0 obj <</Type /Pages /Kids [3 0 R] /Count 1>> endobj
3 0 obj <</Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources <</Font <</F1 4 0 R>>>> /Contents 5 0 R>> endobj
4 0 obj <</Type /Font /Subtype /Type1 /BaseFont /Helvetica>> endobj
5 0 obj <</Length {len(stream_data)}>>
stream
{stream_data}
endstream
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000230 00000 n 
0000000296 00000 n 
trailer <</Size 6 /Root 1 0 R>>
startxref
400
%%EOF"""
    return pdf_str.encode("latin-1")

def test_user_shipment_creation_and_no_demo_fallback():
    res = client.post("/api/shipments", json={
        "crop": "Mango",
        "variety": "Alphonso",
        "origin": "India",
        "destination": "European Union",
        "quantity_kg": 1500.0,
        "deadline_days": 10
    })
    assert res.status_code == 200
    data = res.json()
    shipment_id = data["id"]
    assert data["status"] == "DOCUMENTS_PENDING"
    assert data["is_demo"] is False
    assert data["assessment_confidence"] == 0

    proc_res = client.post(f"/api/shipments/{shipment_id}/process")
    assert proc_res.status_code == 200
    proc_data = proc_res.json()
    assert proc_data["shipment"]["status"] == "HOLD"
    assert proc_data["shipment"]["compliance_score"] < 100

def test_real_pdf_upload_extraction_and_compliance():
    s_res = client.post("/api/shipments", json={
        "crop": "Mango",
        "variety": "Alphonso",
        "origin": "India",
        "destination": "European Union",
        "quantity_kg": 2000.0,
        "deadline_days": 7
    })
    shipment_id = s_res.json()["id"]

    pdf_bytes = create_sample_pdf([
        "Laboratory Residue Analysis Report",
        "Product: Mango",
        "Active Ingredient: Imidacloprid",
        "Measured Residue: 0.31 mg/kg",
        "Laboratory: NABL Export Quality Control Lab",
        "Batch: BATCH-MANGO-908"
    ])

    upload_res = client.post(
        f"/api/shipments/{shipment_id}/documents",
        files={"file": ("residue_report.pdf", pdf_bytes, "application/pdf")},
        data={"document_type": "RESIDUE_TEST_REPORT"}
    )
    assert upload_res.status_code == 200
    doc_data = upload_res.json()
    assert doc_data["document_type"] == "RESIDUE_TEST_REPORT"
    assert doc_data["extracted_fields"]["residue_value"] == 0.31
    assert doc_data["extracted_fields"]["active_ingredient"] == "Imidacloprid"
    assert doc_data["provenance_map"]["residue_value"]["source_page"] == "Page 1"

def test_cross_document_quantity_contradiction_detection():
    s_res = client.post("/api/shipments", json={
        "crop": "Mango",
        "variety": "Alphonso",
        "origin": "India",
        "destination": "European Union",
        "quantity_kg": 2000.0,
        "deadline_days": 7
    })
    shipment_id = s_res.json()["id"]

    inv_pdf = create_sample_pdf([
        "Commercial Invoice INV-2026-001",
        "Product: Mango",
        "Quantity: 2000 kg"
    ])
    client.post(
        f"/api/shipments/{shipment_id}/documents",
        files={"file": ("invoice.pdf", inv_pdf, "application/pdf")},
        data={"document_type": "COMMERCIAL_INVOICE"}
    )

    pack_pdf = create_sample_pdf([
        "Export Packing List PL-2026-001",
        "Product: Mango",
        "Quantity: 1800 kg"
    ])
    client.post(
        f"/api/shipments/{shipment_id}/documents",
        files={"file": ("packing_list.pdf", pack_pdf, "application/pdf")},
        data={"document_type": "PACKING_LIST"}
    )

    proc_res = client.post(f"/api/shipments/{shipment_id}/process")
    assert proc_res.status_code == 200
    findings = proc_res.json()["compliance_result"]["findings"]
    
    contradictions = [f for f in findings if f.get("title") == "Document Contradiction" or "Contradiction" in f.get("reason", "")]
    assert len(contradictions) >= 1
    assert proc_res.json()["shipment"]["status"] == "HOLD"

def test_txt_and_json_document_upload_and_remediation():
    s_res = client.post("/api/shipments", json={
        "crop": "Mango",
        "variety": "Alphonso",
        "origin": "India",
        "destination": "European Union",
        "quantity_kg": 2000.0,
        "deadline_days": 7
    })
    shipment_id = s_res.json()["id"]

    # Upload TXT residue report with failing residue (0.82 mg/kg)
    txt_content = "Laboratory Residue Test Report\nProduct: Mango\nActive Ingredient: Imidacloprid\nMeasured Residue: 0.82 mg/kg\n"
    client.post(
        f"/api/shipments/{shipment_id}/documents",
        files={"file": ("failing_report.txt", txt_content.encode("utf-8"), "text/plain")},
        data={"document_type": "RESIDUE_TEST_REPORT"}
    )

    proc1 = client.post(f"/api/shipments/{shipment_id}/process")
    assert proc1.json()["shipment"]["status"] == "HOLD"
    fail_findings = proc1.json()["compliance_result"]["findings"]
    assert any("Pesticide MRL Violation" in f.get("title", "") for f in fail_findings)

    # Upload JSON passing report (0.31 mg/kg)
    json_data = json.dumps({
        "report": "Residue Analysis",
        "product": "Mango",
        "active_ingredient": "Imidacloprid",
        "residue_value": 0.31,
        "unit": "mg/kg"
    })
    client.post(
        f"/api/shipments/{shipment_id}/documents",
        files={"file": ("passing_report.json", json_data.encode("utf-8"), "application/json")},
        data={"document_type": "RESIDUE_TEST_REPORT"}
    )

    reproc = client.post(f"/api/shipments/{shipment_id}/reprocess")
    assert reproc.status_code == 200
    reproc_findings = reproc.json()["compliance_result"]["findings"]
    # Check that residue MRL violation gap is cleared
    mrl_gaps = [f for f in reproc_findings if "Pesticide MRL Violation" in f.get("title", "")]
    assert len(mrl_gaps) == 0

def test_evidence_provenance_modal_data_structures():
    """Verify that missing document findings state explicit missing evidence without logical contradictions."""
    s_res = client.post("/api/shipments", json={
        "crop": "Mango",
        "variety": "Alphonso",
        "origin": "India",
        "destination": "European Union",
        "quantity_kg": 1000.0,
        "deadline_days": 5
    })
    shipment_id = s_res.json()["id"]

    proc_res = client.post(f"/api/shipments/{shipment_id}/process")
    assert proc_res.status_code == 200
    findings = proc_res.json()["compliance_result"]["findings"]

    # 1. Assert missing document finding structure
    missing_phyto = next((f for f in findings if "PHYTOSANITARY_CERT" in f.get("title", "") or "PHYTOSANITARY_CERT" in f.get("reason", "")), None)
    assert missing_phyto is not None
    assert missing_phyto["status"] == "FAIL"
    assert missing_phyto["actual_data"] == "No uploaded document classified as PHYTOSANITARY_CERT."
    assert "No uploaded evidence" in missing_phyto["source_evidence"]
    assert missing_phyto["source_type"] == "APPLICATION/DOCUMENT RULE"
    assert missing_phyto["actual_data"] != "PHYTOSANITARY_CERT"

    # 2. Upload document and assert present document finding structure
    phyto_pdf = create_sample_pdf(["Phytosanitary Certificate India NPPO", "Crop: Mango"])
    client.post(
        f"/api/shipments/{shipment_id}/documents",
        files={"file": ("phytosanitary_cert.pdf", phyto_pdf, "application/pdf")},
        data={"document_type": "PHYTOSANITARY_CERT"}
    )
    reproc = client.post(f"/api/shipments/{shipment_id}/reprocess")
    assert reproc.status_code == 200
    updated_findings = reproc.json()["compliance_result"]["findings"]
    missing_phyto_after = [f for f in updated_findings if "PHYTOSANITARY_CERT" in f.get("title", "") and f.get("status") == "FAIL"]
    assert len(missing_phyto_after) == 0

    # 3. Assert seed demo shipment compatibility
    demo_res = client.get("/api/shipments/SHP-MANGO-001/compliance")
    assert demo_res.status_code == 200
    demo_result = demo_res.json()
    assert demo_result["shipment_id"] == "SHP-MANGO-001"

