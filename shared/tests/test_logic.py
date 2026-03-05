import pytest
from ..tools.logic import revops_logic
from ..models.leads import LeadBase

@pytest.mark.asyncio
async def test_reasoning_flow_auto_qualify():
    # Scenario: High-value lead (VP) from high-growth company (Acme Corp)
    lead = LeadBase(
        first_name="John",
        last_name="Doe",
        email="j.doe@acme.corp",
        job_title="VP of Sales",
        company_name="Acme Corp"
    )
    
    result = await revops_logic.process_lead_reasoning(lead)
    
    assert result["action"] == "AUTO_QUALIFY"
    assert result["score"] >= 70
    assert result["escalate_to_human"] is False

@pytest.mark.asyncio
async def test_reasoning_flow_manual_review():
    # Scenario: Low-level lead from high-growth company
    lead = LeadBase(
        first_name="Jane",
        last_name="Smith",
        email="j.smith@acme.corp",
        job_title="Sales Associate",
        company_name="Acme Corp"
    )
    
    result = await revops_logic.process_lead_reasoning(lead)
    
    assert result["action"] == "MANUAL_REVIEW"
    assert result["score"] >= 40 and result["score"] < 70
    assert result["escalate_to_human"] is True
    assert "Score in review range" in result["escalation_reason"]
