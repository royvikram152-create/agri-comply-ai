from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import health, shipments, documents, compliance, agents, approvals, audit
from app.orchestration.orchestrator import orchestrator_instance

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AGRICOMPLY AI - Agentic Export Documentation & Compliance Copilot API"
)

# CORS configuration for React frontend development & deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["Health"])
app.include_router(shipments.router, prefix=settings.API_V1_STR, tags=["Shipments"])
app.include_router(documents.router, prefix=settings.API_V1_STR, tags=["Documents"])
app.include_router(compliance.router, prefix=settings.API_V1_STR, tags=["Compliance & Evidence"])
app.include_router(agents.router, prefix=settings.API_V1_STR, tags=["Agents"])
app.include_router(approvals.router, prefix=settings.API_V1_STR, tags=["Approvals"])
app.include_router(audit.router, prefix=settings.API_V1_STR, tags=["Audit Trail"])

@app.on_event("startup")
def startup_event():
    # Initial pipeline run for seed shipment SHP-MANGO-001
    try:
        orchestrator_instance.run_pipeline("SHP-MANGO-001")
    except Exception as e:
        print(f"Startup pipeline execution info: {e}")

@app.get("/")
def root():
    return {
        "message": "AGRICOMPLY AI Engine Active",
        "docs_url": "/docs",
        "health_url": f"{settings.API_V1_STR}/health"
    }
