from typing import Dict, Any, List, Optional
from uuid import UUID
from pydantic import BaseModel
from .enricher import enricher
from ..models.leads import LeadBase, QualificationScore

class AgentPersona:
    NAME = "Alex"
    ROLE = "RevOps Associate"
    SYSTEM_PROMPT = (
        "You are Alex, a RevOps Associate. Your goal is to qualify leads with high precision. "
        "Be concise, objective, and data-driven. Always state the facts found during research."
    )

class RevOpsLogic:
    """Encapsulates the reasoning and escalation logic for the RevOps FTE."""

    ESCALATION_CONDITIONS = [
        "Unclear job title",
        "Conflicting revenue data",
        "Strategic competitor",
        "request for human contact"
    ]

    async def process_lead_reasoning(self, lead: LeadBase) -> Dict[str, Any]:
        """
        Simulates the multi-step reasoning flow:
        Intake -> Research -> Score -> Decision.
        """
        # 1. Research phase (ADR-1: Tool-calling via enricher)
        research_result = await enricher.search_company_info(lead.company_name or "")
        
        # 2. Scoring phase
        score_result = enricher.score_lead(lead, research_result["data"])
        
        # 3. Decision phase
        action = "DISCARD"
        if score_result.score >= 70:
            action = "AUTO_QUALIFY"
        elif score_result.score >= 40:
            action = "MANUAL_REVIEW"

        # 4. Check for Escalation (Human-in-the-loop)
        escalate = False
        reason = None
        if action == "MANUAL_REVIEW":
            escalate = True
            reason = "Score in review range (40-69)."
        elif any(cond in (lead.job_title or "") for cond in self.ESCALATION_CONDITIONS):
            escalate = True
            reason = "Strategic account detection."

        return {
            "lead_id": score_result.lead_id,
            "action": action,
            "score": score_result.score,
            "reasoning": score_result.reasoning,
            "escalate_to_human": escalate,
            "escalation_reason": reason,
            "facts": research_result["data"]
        }

# Global Logic Instance
revops_logic = RevOpsLogic()
