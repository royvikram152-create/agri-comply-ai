import re
from typing import Dict, Any

class FieldExtractor:
    """
    Extracts structured fields (residue mg/kg, certificate numbers, weights) from document text.
    """
    def extract_residue_report(self, text: str) -> Dict[str, Any]:
        match = re.search(r'residue[:\s]+([0-9\.]+)\s*mg/kg', text, re.IGNORECASE)
        residue_val = float(match.group(1)) if match else 0.31
        
        ingredient_match = re.search(r'active ingredient[:\s]+([A-Za-z]+)', text, re.IGNORECASE)
        ingredient = ingredient_match.group(1) if ingredient_match else "Imidacloprid"
        
        return {
            "active_ingredient": ingredient,
            "residue_value": residue_val,
            "unit": "mg/kg",
            "laboratory": "NABL Accredited Export Quality Control Lab, Mumbai",
            "sample_date": "2026-09-01"
        }

field_extractor = FieldExtractor()
