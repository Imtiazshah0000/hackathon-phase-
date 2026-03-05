import httpx
import json
from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime
from ..models.leads import LeadBase, QualificationScore

class RevOpsEnricher:
    """Modular tools for lead enrichment and scoring."""

    async def search_company_info(self, company_name: str, domain: Optional[str] = None) -> Dict[str, Any]:
        """
        MOCK: Searches for company information. 
        In Stage 2, this will call Tavily or a similar search API.
        """
        # Simulated search result
        mock_data = {
            "Acme Corp": {"size": "2500", "industry": "Manufacturing", "revenue": "$100M+"},
            "CyberDyne Systems": {"size": "800", "industry": "AI & Robotics", "revenue": "$50M+"}
        }
        
        # Default for unknown companies
        result = mock_data.get(company_name, {"size": "Unknown", "industry": "Unknown", "revenue": "Unknown"})
        return {"source": "MockSearch", "data": result}

    def validate_contact(self, email: str) -> bool:
        """Simple syntax and domain check for contact validation."""
        return "@" in email and "." in email.split("@")[-1]

    def score_lead(self, lead: LeadBase, company_data: Dict[str, Any]) -> QualificationScore:
        """
        Applies basic qualification logic based on job title and company size.
        """
        score = 0
        criteria = {"High-Value Industry": False, "Decision Maker": False, "Scaleable Size": False}

        # 1. Check Job Title (Decision Maker)
        dm_keywords = ["VP", "Director", "Head", "Chief", "CEO", "CTO"]
        if lead.job_title and any(kw in lead.job_title for kw in dm_keywords):
            score += 40
            criteria["Decision Maker"] = True

        # 2. Check Industry
        target_industries = ["AI & Robotics", "Manufacturing", "SaaS"]
        if company_data.get("industry") in target_industries:
            score += 30
            criteria["High-Value Industry"] = True

        # 3. Check Size
        size = company_data.get("size", "0")
        if size.isdigit() and int(size) > 500:
            score += 30
            criteria["Scaleable Size"] = True
        elif "M" in company_data.get("revenue", ""): # Handles "$100M+"
            score += 30
            criteria["Scaleable Size"] = True

        reasoning = f"Lead qualified with score {score} based on {', '.join([k for k, v in criteria.items() if v])}."
        
        return QualificationScore(
            lead_id=UUID(int=0), # Placeholder for actual lead ID
            score=score,
            reasoning=reasoning,
            criteria_met=criteria
        )

# Global Instance for Tool Injection
enricher = RevOpsEnricher()
