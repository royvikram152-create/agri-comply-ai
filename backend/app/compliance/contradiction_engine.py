from typing import List, Dict, Any
from app.models.document import Document, DocumentType
from app.models.shipment import Shipment
from app.models.compliance import SeverityLevel

NO_EXTRACT_MSG = "Could not extract this field from uploaded evidence."

class ContradictionEngine:
    """
    Deterministic cross-document contradiction detector.
    Audits structured evidence across uploaded documents for numerical, textual, and batch discrepancies.
    """

    def detect_contradictions(self, shipment: Shipment, documents: List[Document]) -> List[Dict[str, Any]]:
        findings = []

        if not documents:
            return findings

        # 1. Quantity Contradictions across Invoice, Packing List, Phyto, Shipment
        qty_map: Dict[str, float] = {}
        for doc in documents:
            fields = doc.extracted_fields or {}
            qty = fields.get("quantity_kg")
            if isinstance(qty, (int, float)) and qty > 0:
                qty_map[f"{doc.document_type.value} ({doc.file_name})"] = float(qty)

        if len(qty_map) >= 2:
            base_label, base_qty = list(qty_map.items())[0]
            for other_label, other_qty in list(qty_map.items())[1:]:
                if abs(base_qty - other_qty) > 1.0:  # Tolerance threshold 1 kg
                    findings.append({
                        "id": "CRIT-DOC-CONTRADICTION-QTY",
                        "severity": SeverityLevel.CRITICAL,
                        "title": "Cross-Document Quantity Contradiction",
                        "status": "FAIL",
                        "message": f"Quantity discrepancy detected between documents! '{base_label}' specifies {base_qty} kg whereas '{other_label}' specifies {other_qty} kg.",
                        "metadata": {
                            "expected_quantity": base_qty,
                            "observed_quantity": other_qty,
                            "source_1": base_label,
                            "source_2": other_label
                        }
                    })
                    break

        # 2. Commodity / Product Mismatch (e.g. Shipment Crop vs Document Product)
        shipment_crop = shipment.crop.strip().lower()
        for doc in documents:
            fields = doc.extracted_fields or {}
            doc_prod = fields.get("product")
            if doc_prod and doc_prod != NO_EXTRACT_MSG and isinstance(doc_prod, str):
                doc_prod_lower = doc_prod.strip().lower()
                if doc_prod_lower not in shipment_crop and shipment_crop not in doc_prod_lower:
                    findings.append({
                        "id": "CRIT-DOC-CONTRADICTION-PROD",
                        "severity": SeverityLevel.CRITICAL,
                        "title": f"Commodity Mismatch ({doc.file_name})",
                        "status": "FAIL",
                        "message": f"Document product '{doc_prod}' contradicts registered shipment commodity '{shipment.crop}'!",
                        "metadata": {
                            "shipment_crop": shipment.crop,
                            "document_product": doc_prod,
                            "file_name": doc.file_name
                        }
                    })

        # 3. Batch / Lot Identifier Mismatch across Certificates
        batch_map: Dict[str, str] = {}
        for doc in documents:
            fields = doc.extracted_fields or {}
            batch = fields.get("batch_id")
            if batch and batch != NO_EXTRACT_MSG and isinstance(batch, str):
                batch_map[doc.file_name] = batch.strip()

        if len(batch_map) >= 2:
            base_file, base_batch = list(batch_map.items())[0]
            for other_file, other_batch in list(batch_map.items())[1:]:
                if base_batch.lower() != other_batch.lower():
                    findings.append({
                        "id": "CRIT-DOC-CONTRADICTION-BATCH",
                        "severity": SeverityLevel.CRITICAL,
                        "title": "Batch / Lot ID Contradiction",
                        "status": "FAIL",
                        "message": f"Batch identifier mismatch between uploaded documents! '{base_file}' cites batch '{base_batch}' whereas '{other_file}' cites batch '{other_batch}'.",
                        "metadata": {
                            "batch_1": f"{base_file}: {base_batch}",
                            "batch_2": f"{other_file}: {other_batch}"
                        }
                    })
                    break

        return findings

contradiction_engine_instance = ContradictionEngine()
