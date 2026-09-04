from fastapi import APIRouter
from app.orchestration.orchestrator import orchestrator_instance

router = APIRouter()

@router.get("/agents")
def list_agents():
    return [
        {
            "name": orchestrator_instance.exporter_agent.name,
            "description": orchestrator_instance.exporter_agent.description,
            "role": "Exporter Interaction Agent",
            "type": "NATURAL_LANGUAGE_PARSER",
            "status": "ACTIVE"
        },
        {
            "name": orchestrator_instance.regulatory_agent.name,
            "description": orchestrator_instance.regulatory_agent.description,
            "role": "Regulatory Retrieval Agent",
            "type": "BM25_RAG_RETRIEVER",
            "status": "ACTIVE"
        },
        {
            "name": orchestrator_instance.farm_agent.name,
            "description": orchestrator_instance.farm_agent.description,
            "role": "Farm Record Check Agent",
            "type": "DETERMINISTIC_CHECKER",
            "status": "ACTIVE"
        },
        {
            "name": orchestrator_instance.document_agent.name,
            "description": orchestrator_instance.document_agent.description,
            "role": "Document Assembly Agent",
            "type": "CROSS_DOC_VALIDATOR",
            "status": "ACTIVE"
        },
        {
            "name": orchestrator_instance.gap_agent.name,
            "description": orchestrator_instance.gap_agent.description,
            "role": "Gap Reporting Agent",
            "type": "REMEDIATION_RANKER",
            "status": "ACTIVE"
        }
    ]
