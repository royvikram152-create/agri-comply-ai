from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel
import time

class AgentExecutionResult(BaseModel):
    agent_name: str
    status: str  # completed, warning, failed
    findings: List[Dict[str, Any]]
    evidence_ids: List[str]
    warnings: List[str]
    execution_time_ms: float
    metadata: Dict[str, Any]

class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> AgentExecutionResult:
        """
        Execute agent logic on structured input.
        Agents parse, extract, retrieve, or summarize information.
        Agents MUST NOT directly mutate final shipment compliance status.
        """
        pass
