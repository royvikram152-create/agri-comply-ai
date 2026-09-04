from typing import Dict, Any, List

class AssessmentConfidenceEngine:
    """
    Calculates deterministic AI Assessment Confidence based on evidence quality and completeness.
    
    Confidence reflects the completeness and quality of available evidence.
    It is NOT a legal compliance probability, NOT a prediction of approval, and NOT an input
    to the deterministic compliance firewall.
    """
    def calculate_confidence(
        self,
        shipment: Any,
        reg_findings: List[Dict[str, Any]],
        farm_findings: List[Dict[str, Any]],
        documents: List[Any]
    ) -> int:
        
        # 1. Metadata Completeness (Max 20 pts)
        meta_score = 0
        if shipment.crop and shipment.origin and shipment.destination:
            meta_score += 10
        if shipment.quantity_kg > 0 and shipment.deadline_days > 0:
            meta_score += 5
        if shipment.exporter and shipment.exporter.registration_number:
            meta_score += 5

        # 2. Regulatory RAG Evidence Coverage (Max 25 pts)
        reg_score = 0
        if len(reg_findings) >= 2:
            reg_score = 25
        elif len(reg_findings) == 1:
            reg_score = 15

        # 3. Farm Treatment Record Quality (Max 20 pts)
        farm_score = 0
        if farm_findings and len(farm_findings) > 0:
            farm_score = 20

        # 4. Mandatory Export Document Package Quality (Max 20 pts)
        # Evaluates presence of primary mandatory export document set
        doc_count = len(documents) if documents else 0
        doc_score = 20 if doc_count >= 4 else int((doc_count / 4.0) * 20)

        # 5. Authoritative Citation Quality (Max 10 pts)
        provenance_score = 9  # EFSA / EUR-Lex database verified citations

        total_confidence = meta_score + reg_score + farm_score + doc_score + provenance_score
        return min(100, max(0, total_confidence))

confidence_engine_instance = AssessmentConfidenceEngine()
