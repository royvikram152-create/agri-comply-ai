from fastapi import APIRouter
from app.config import settings

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "mode": "DEMO_ZERO_COST",
        "llm_enabled": settings.ENABLE_LOCAL_LLM
    }
