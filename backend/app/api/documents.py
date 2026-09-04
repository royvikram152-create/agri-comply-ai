from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
from datetime import datetime, timezone
import uuid
import os

from app.models.document import Document, DocumentType, DocumentStatus
from app.models.audit import AuditEvent
from app.database.store import store
from app.services.storage_service import storage_service_instance
from app.services.extractor_service import extractor_service_instance
from app.services.classifier_service import classifier_service_instance

router = APIRouter()

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt", "csv", "json", "log"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB limit

@router.get("/shipments/{shipment_id}/documents", response_model=List[Document])
def list_documents(shipment_id: str):
    if shipment_id not in store.shipments:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return store.documents.get(shipment_id, [])

@router.post("/shipments/{shipment_id}/documents", response_model=Document)
async def upload_document(
    shipment_id: str,
    file: UploadFile = File(...),
    document_type: Optional[str] = Form(None)
):
    if shipment_id not in store.shipments:
        raise HTTPException(status_code=404, detail="Shipment not found")

    filename = os.path.basename(file.filename or "uploaded_document.pdf")
    ext = filename.split(".")[-1].lower() if "." in filename else ""

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '.{ext}'. Supported formats: PDF, DOCX, TXT, CSV, JSON."
        )

    # Read bytes immediately for serverless/memory execution
    content_bytes = await file.read()
    if len(content_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds maximum allowed 10MB limit.")

    doc_id = f"DOC-{uuid.uuid4().hex[:6].upper()}"
    now = datetime.now(timezone.utc)

    # Save to storage service
    saved_path = storage_service_instance.save_file(doc_id, filename, content_bytes)

    # Instant Document Content & Provenance Extraction
    extracted_res = extractor_service_instance.extract_document(filename, content_bytes)

    # Heuristic Classification if type not specified or AUTO
    if not document_type or document_type == "AUTO" or document_type not in DocumentType.__members__:
        classified_type, confidence = classifier_service_instance.classify(
            filename, extracted_res["full_text"]
        )
    else:
        classified_type = DocumentType(document_type)
        confidence = 1.0

    doc = Document(
        id=doc_id,
        shipment_id=shipment_id,
        document_type=classified_type,
        file_name=filename,
        file_path=saved_path,
        uploaded_at=now,
        status=DocumentStatus.VALID,
        issue_date=now.strftime("%Y-%m-%d"),
        expiry_date="2026-12-31",
        extracted_fields=extracted_res["extracted_fields"],
        extracted_text=extracted_res["full_text"][:2000],  # Snippet preview
        provenance_map=extracted_res["provenance_map"],
        file_format=ext.upper(),
        file_size=len(content_bytes),
        classification_confidence=confidence
    )

    if shipment_id not in store.documents:
        store.documents[shipment_id] = []
    
    # Overwrite if document of same type exists for remediation
    store.documents[shipment_id] = [d for d in store.documents[shipment_id] if d.document_type != classified_type]
    store.documents[shipment_id].append(doc)

    # Audit Trail Entry
    if shipment_id not in store.audit_events:
        store.audit_events[shipment_id] = []
    store.audit_events[shipment_id].append(
        AuditEvent(
            id=f"AUD-DOC-{uuid.uuid4().hex[:6]}",
            shipment_id=shipment_id,
            event_type="DOCUMENT_UPLOADED",
            agent_name="Document Assembly Agent",
            title=f"Document Uploaded: {filename}",
            description=f"File '{filename}' ({ext.upper()}) uploaded and classified as '{classified_type.value}'. Extracted fields with page provenance.",
            metadata={
                "doc_id": doc_id,
                "file_name": filename,
                "document_type": classified_type.value,
                "extracted_fields_count": len(extracted_res["extracted_fields"])
            },
            timestamp=now
        )
    )

    return doc
