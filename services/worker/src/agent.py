import json
import logging
from typing import Dict, Any, Optional
from uuid import UUID
from openai import AsyncOpenAI
from shared.tools.enricher import enricher
from shared.tools.logic import AgentPersona
from shared.tools.outreach import outreach_orchestrator
from shared.database.repository import db_repo
from shared.tools.security import SecurityGuard, KillSwitch
from shared.models.leads import LeadBase
from .metrics import LEADS_PROCESSED, AUTONOMOUS_OUTREACH, ESCALATIONS, track_token_usage, LEAD_PROCESSING_TIME

logger = logging.getLogger("revops-agent")

class RevOpsAgent:
    """
    OpenAI-driven Digital FTE (Alex). 
    Uses the OpenAI API to reason about leads and make qualification decisions.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = AsyncOpenAI(api_key=api_key)
        self.system_prompt = AgentPersona.SYSTEM_PROMPT

    async def run_autonomous_loop(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        The dynamic reasoning loop for the RevOps Digital FTE (Phase 4: Observable & Secure).
        1. Parse lead & Store Initial State (Persistence).
        2. Research (Tool Call).
        3. Qualify (LLM Reasoning).
        4. Outreach (Tool Call - Guarded by Kill Switch).
        5. Audit (Persistence - PII Masked).
        """
        lead = LeadBase(**lead_data)
        logger.info(f"Agent {AgentPersona.NAME} is processing lead: {lead.email}")

        with LEAD_PROCESSING_TIME.time():
            # Task 2.4: Save Initial Lead Ingest (Audit/Persistence - ADR-3)
            lead_id = await db_repo.save_lead_intake(lead_data)

            # Step 1: Autonomous Research (Simulated Tool Call via SDK)
            # In a full Agents SDK implementation, this would be a tool provided to the assistant.
            # Here we call it explicitly to feed the context.
            research_data = await enricher.search_company_info(lead.company_name or "")
            
            # Task 2.4: Save Enrichment Result (ADR-3)
            await db_repo.save_enrichment(lead_id, "Tavily (Mock)", research_data["data"], research_data)

            # Step 2: Qualification & Reasoning (LLM Call)
            # Construct the context for the LLM
            user_content = f"""
            Lead Information:
            Name: {lead.first_name} {lead.last_name}
            Job Title: {lead.job_title}
            Company: {lead.company_name}
            Email: {lead.email}

            Enrichment Data:
            {json.dumps(research_data["data"], indent=2)}

            Task:
            Evaluate this lead based on the company size, industry, and job title match.
            Decide if we should:
            - AUTO_QUALIFY (High potential, fits ICP)
            - MANUAL_REVIEW (Unsure, borderline)
            - DISCARD (Not a fit)

            Return a JSON object with:
            - action: "AUTO_QUALIFY" | "MANUAL_REVIEW" | "DISCARD"
            - score: integer (0-100)
            - reasoning: string explanation
            - escalate_to_human: boolean
            - escalation_reason: string or null
            """

            try:
                response = await self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": self.system_prompt + "\nResponse must be valid JSON."},
                        {"role": "user", "content": user_content}
                    ],
                    response_format={"type": "json_object"}
                )
                
                content = response.choices[0].message.content
                reasoning_result = json.loads(content)
                
                # Mock token tracking for now
                usage = response.usage
                track_token_usage("gpt-4o", usage.prompt_tokens, usage.completion_tokens)

            except Exception as e:
                logger.error(f"LLM Error: {e}")
                # Fallback to manual review on error
                reasoning_result = {
                    "action": "MANUAL_REVIEW",
                    "score": 0,
                    "reasoning": f"LLM Inference failed: {str(e)}",
                    "escalate_to_human": True,
                    "escalation_reason": "System Error"
                }

            # Task 2.4: Save Qualification Result (ADR-3)
            await db_repo.save_qualification_result(
                lead_id=lead_id,
                score=reasoning_result.get("score", 0),
                reasoning=reasoning_result.get("reasoning", ""),
                criteria={}
            )

            # Step 3: Multi-Channel Outreach (Task 2.3 - Phase 4 Guarded by Kill Switch)
            outreach_status = None
            if not KillSwitch.is_active():
                # Only outreach if qualified
                if reasoning_result.get("action") == "AUTO_QUALIFY":
                    outreach_status = await outreach_orchestrator.dispatch_outreach(lead_data, reasoning_result)
                    if outreach_status:
                        AUTONOMOUS_OUTREACH.labels(channel="EMAIL").inc()
            else:
                logger.warning(f"Outreach SKIPPED for {lead.email} due to active KILL SWITCH.")

            # Step 4: Structured Output for Auditing (ADR-3 - Phase 4: PII Masked)
            masked_metadata = SecurityGuard.mask_pii({
                "model": "gpt-4o",
                "tools_used": ["search_company_info", "openai_chat_completion", "dispatch_outreach"],
                "facts_extracted": research_data["data"],
                "outreach_details": outreach_status
            })

            audit_entry = {
                "lead_id": str(lead_id),
                "step": "QUALIFICATION_AND_OUTREACH",
                "decision": reasoning_result.get("action"),
                "score": reasoning_result.get("score"),
                "reasoning": reasoning_result.get("reasoning"),
                "outreach_sent": bool(outreach_status),
                "metadata": masked_metadata
            }

            # Task 2.4: Final Audit Log entry (ADR-3)
            await db_repo.log_agent_action(lead_id, "FINAL_QUALIFICATION", audit_entry)

            logger.info(f"Decision for {lead.email}: {reasoning_result.get('action')} (Score: {reasoning_result.get('score')})")
            
            # Update Metrics
            LEADS_PROCESSED.labels(status=reasoning_result.get("action", "UNKNOWN")).inc()
            if reasoning_result.get("escalate_to_human"):
                logger.warning(f"ESCALATION TRIGGERED: {reasoning_result.get('escalation_reason')}")
                ESCALATIONS.inc()

            return audit_entry

# Global Agent Instance
# revops_agent = RevOpsAgent(api_key=os.getenv("OPENAI_API_KEY"))
