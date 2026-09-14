from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="AI SRE Copilot",
    version="0.1.0",
    description="Incident investigation API for cloud-native systems.",
)

class IncidentRequest(BaseModel):
    title: str
    service: str
    severity: str = "warning"
    description: str = ""

class InvestigationResponse(BaseModel):
    incident: str
    status: str
    next_steps: list[str]

@app.get("/health")
def health():
    return {"status": "healthy", "service": "ai-sre-copilot"}

@app.post("/api/v1/incidents/investigate", response_model=InvestigationResponse)
def investigate(request: IncidentRequest):
    # MVP placeholder. Future versions will call observability adapters,
    # Kubernetes, GitHub and an LLM investigator.
    return InvestigationResponse(
        incident=request.title,
        status="queued",
        next_steps=[
            "Collect Kubernetes workload state",
            "Query Prometheus metrics",
            "Inspect logs and traces",
            "Correlate recent deployments",
        ],
    )
