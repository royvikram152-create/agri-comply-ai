from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
from datetime import datetime, timezone
import uuid

from app.models.document import Document, DocumentType, DocumentStatus
from app.database.store import store

router = APIRouter()

@router.get("/shipments/{shipment_id}/documents", response_model=List[Document])
def list_documents(shipment_id: str):
    return store.documents.get(shipment_id, [])

@router.post("/shipments/{shipment_id}/documents", response_model=Document)
async def upload_document(
    shipment_id: str,
    document_type: str = Form(...),
    file: UploadFile = File(...)
):
    if shipment_id not in store.shipments:
        raise HTTPException(status_code=404, detail="Shipment not found")

    now = datetime.now(timezone.utc)
    doc_id = f"DOC-{uuid.uuid4().hex[:6].upper()}"

    doc = Document(
        id=doc_id,
        shipment_id=shipment_id,
        document_type=DocumentType(document_type) if document_type in DocumentType.__members__ else DocumentType.QUALITY_CERT,
        file_name=file.filename or "uploaded_document.pdf",
        uploaded_at=now,
        status=DocumentStatus.VALID,
        issue_date=now.strftime("%Y-%m-%d"),
        expiry_date="2026-12-31",
        extracted_fields={
            "filename": file.filename,
            "uploaded_by": "Exporter User",
            "content_type": file.content_type
        }
    )

    if shipment_id not in store.documents:
        store.documents[shipment_id] = []
    store.documents[shipment_id].append(doc)

    return doc
