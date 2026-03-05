from fastapi import FastAPI
from .api.leads import router as leads_router
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="RevOps Digital FTE Gateway",
    description="Primary Intake Service for Autonomous Lead Operations (Stage 2: Specialization)",
    version="1.0.0"
)

# 1. Register API Routers
app.include_router(leads_router, prefix="/api/v1", tags=["Leads"])

# 2. Health Check & Monitoring (ADR-4: Kubernetes Readiness)
@app.get("/health")
async def health_check():
    """
    Health check endpoint for Liveness/Readiness probes.
    """
    return {
        "status": "UP",
        "timestamp": datetime.now().isoformat(),
        "service": "revops-gateway"
    }

@app.get("/")
async def root():
    """Root info endpoint."""
    return {
        "message": "RevOps Digital FTE Gateway is active.",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    from .agent import RevOpsAgent
