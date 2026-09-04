from typing import Dict, Any

class DocumentParser:
    def parse_text(self, text: str) -> Dict[str, Any]:
        """
        Parses text content of uploaded documents (PDF, TXT, CSV, JSON).
        """
        return {"raw_text": text, "parsed": True}

document_parser = DocumentParser()
