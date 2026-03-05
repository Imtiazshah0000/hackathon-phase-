import pytest
from uuid import UUID
from ..tools.enricher import RevOpsEnricher
from ..models.leads import LeadBase

@pytest.mark.asyncio
async def test_search_company_info():
    enricher = RevOpsEnricher()
    result = await enricher.search_company_info("Acme Corp")
    assert result["data"]["size"] == "2500"
    assert result["data"]["industry"] == "Manufacturing"

def test_validate_contact():
    enricher = RevOpsEnricher()
    assert enricher.validate_contact("j.doe@acme.corp") is True
    assert enricher.validate_contact("invalid-email") is False

def test_score_lead():
    enricher = RevOpsEnricher()
    lead = LeadBase(
        first_name="John", 
        last_name="Doe", 
        email="j.doe@acme.corp", 
        job_title="VP of Sales", 
        company_name="Acme Corp"
    )
    company_data = {"size": "2500", "industry": "Manufacturing", "revenue": "$100M+"}
    
    result = enricher.score_lead(lead, company_data)
    assert result.score >= 70
    assert result.criteria_met["Decision Maker"] is True
    assert result.criteria_met["High-Value Industry"] is True
