import re
from typing import Tuple
from app.models.document import DocumentType

class DocumentClassifierService:
    """
    Heuristic classifier that determines DocumentType based on filename and extracted content keywords.
    """
    def classify(self, filename: str, extracted_text: str = "") -> Tuple[DocumentType, float]:
        name_lower = filename.lower()
        text_lower = extracted_text.lower() if extracted_text else ""
        combined = f"{name_lower} {text_lower}"

        # 1. Residue Test Report
        if any(k in combined for k in ["residue", "pesticide", "lab_test", "laboratory", "nabl", "active_ingredient", "mg/kg", "mrl"]):
            return DocumentType.RESIDUE_TEST_REPORT, 0.95

        # 2. Phytosanitary Certificate
        if any(k in combined for k in ["phytosanitary", "phyto", "plant_protection", "plant health", "nppo", "vapour heat"]):
            return DocumentType.PHYTOSANITARY_CERT, 0.95

        # 3. Commercial Invoice
        if any(k in combined for k in ["invoice", "commercial_invoice", "billing", "unit_price", "total_eur", "total_usd", "buyer", "consignee"]):
            return DocumentType.COMMERCIAL_INVOICE, 0.90

        # 4. Packing List
        if any(k in combined for k in ["packing", "pack_list", "boxes", "cartons", "net_weight", "gross_weight", "pallets"]):
            return DocumentType.PACKING_LIST, 0.90

        # 5. Quality Certificate
        if any(k in combined for k in ["quality", "apeda", "grading", "brix", "globalgap", "class i"]):
            return DocumentType.QUALITY_CERT, 0.85

        # 6. Farm Treatment Record
        if any(k in combined for k in ["farm_record", "spray_log", "treatment_log", "orchard", "pre_harvest"]):
            return DocumentType.FARM_TREATMENT_RECORD, 0.85

        # 7. Certificate of Origin
        if any(k in combined for k in ["origin", "certificate_of_origin", "chamber_of_commerce"]):
            return DocumentType.CERTIFICATE_OF_ORIGIN, 0.85

        return DocumentType.SUPPORTING_DOC, 0.50

classifier_service_instance = DocumentClassifierService()
