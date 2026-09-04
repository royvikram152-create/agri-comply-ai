import os
import uuid
from typing import Dict, Any, Optional

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "uploads")

class DocumentStorageService:
    """
    Decoupled storage service for uploaded document files.
    - Uses local disk persistence for local development.
    - Uses in-memory byte buffer fallback for serverless (Vercel) runtimes.
    """
    def __init__(self):
        self._memory_store: Dict[str, bytes] = {}
        try:
            os.makedirs(UPLOAD_DIR, exist_ok=True)
        except Exception:
            pass

    def save_file(self, file_id: str, file_name: str, content_bytes: bytes) -> str:
        # Save in memory store
        self._memory_store[file_id] = content_bytes
        
        # Try local disk store if directory writable
        try:
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            safe_name = f"{file_id}_{file_name.replace(' ', '_')}"
            file_path = os.path.join(UPLOAD_DIR, safe_name)
            with open(file_path, "wb") as f:
                f.write(content_bytes)
            return file_path
        except Exception:
            return f"memory://{file_id}"

    def get_file_bytes(self, file_id: str, file_path: Optional[str] = None) -> Optional[bytes]:
        if file_id in self._memory_store:
            return self._memory_store[file_id]
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, "rb") as f:
                    return f.read()
            except Exception:
                pass
        return None

storage_service_instance = DocumentStorageService()
