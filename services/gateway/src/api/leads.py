from fastapi import APIRouter, HTTPException, BackgroundTasks
from shared.models.leads import LeadBase
from ..core.kafka import producer
from shared.tools.enricher import enricher

router = APIRouter()

@router.post("/lead")
async def ingest_lead(lead: LeadBase, background_tasks: BackgroundTasks):
    """
    Primary REST endpoint for incoming leads (Task 2.2).
    """
    # 1. Input Validation (Done via Pydantic model)
    print(f"Received lead: {lead.email}")

    # 2. Initial Enrichment check (Tool Call - ADR-1)
    if not enricher.validate_contact(lead.email):
        raise HTTPException(status_code=400, detail="Invalid lead email format.")

    # 3. Publish to Kafka (ADR-2: Event-Driven Processing)
    # Using background_tasks to ensure low latency for the intake request.
    background_tasks.add_task(producer.publish_lead_ingested, lead.model_dump())

    return {
        "status": "INGESTED",
        "lead": lead.email,
        "message": "Lead is being processed by the Digital FTE."
    }

@router.post("/webhooks/slack")
async def slack_webhook(payload: dict, background_tasks: BackgroundTasks):
    """
    Webhook handler for Slack intake.
    """
    # Placeholder: In Stage 2, this will extract email and company from Slack payload.
    print(f"Slack Webhook received: {payload.get('text')}")
    # ... extraction logic ...
    return {"status": "ACK"}
