import json
import logging
from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime
from ..models.leads import LeadBase
from .logic import AgentPersona

# Configure basic logging for outreach audit
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("outreach-service")

class SlackNotifier:
    """Handles internal notifications to the RevOps team."""
    
    async def send_notification(self, lead_email: str, score: int, reason: str, channel: str = "#revops-alerts"):
        """Sends a structured alert to Slack for high-value leads or escalations."""
        message = {
            "channel": channel,
            "text": f"*New Qualified Lead Detected*",
            "attachments": [
                {
                    "fields": [
                        {"title": "Lead", "value": lead_email, "short": True},
                        {"title": "Score", "value": str(score), "short": True},
                        {"title": "Reasoning", "value": reason, "short": False}
                    ]
                }
            ]
        }
        # In a real scenario, use Slack Webhook or WebClient
        logger.info(f"[SLACK] Notification sent for {lead_email} to {channel}")
        return True

class EmailDispatcher:
    """Handles external outreach to leads."""
    
    def format_outreach_email(self, first_name: str, company_name: str) -> str:
        """Formats an email following the 'Alex' persona (concise & professional)."""
        return (
            f"""Subject: Scalable Revenue Operations for {company_name}

Hi {first_name},

I've been researching {company_name}'s recent growth in the industry. Our team has developed a framework specifically for companies of your scale to optimize lead qualification workflows.

Do you have 10 minutes next Tuesday for a brief introduction?

Best regards,

{AgentPersona.NAME}
{AgentPersona.ROLE}"""
        )

    async def send_lead_email(self, lead: LeadBase):
        """Sends an outreach email to the lead."""
        body = self.format_outreach_email(lead.first_name or "there", lead.company_name or "your company")
        # In a real scenario, use SendGrid, Mailgun, or SMTP
        logger.info(f"[EMAIL] Outreach sent to {lead.email}")
        return {"to": lead.email, "body": body, "sent_at": datetime.now().isoformat()}

class OutreachOrchestrator:
    """Orchestrates multi-channel outreach based on agent decisions."""
    
    def __init__(self):
        self.slack = SlackNotifier()
        self.email = EmailDispatcher()

    async def dispatch_outreach(self, lead_data: Dict[str, Any], decision: Dict[str, Any]):
        """
        Main entry point for triggering outreach (Task 2.3).
        """
        lead = LeadBase(**lead_data)
        
        # 1. Internal Notification (Slack)
        if decision["action"] == "AUTO_QUALIFY" or decision["escalate_to_human"]:
            await self.slack.send_notification(
                lead_email=lead.email,
                score=decision["score"],
                reason=decision["reasoning"]
            )

        # 2. External Outreach (Email)
        if decision["action"] == "AUTO_QUALIFY":
            email_status = await self.email.send_lead_email(lead)
            
            # 3. Log to Audit (ADR-3: Interaction table)
            logger.info(f"[AUDIT] Logged interaction for {lead.email}: OUTBOUND EMAIL")
            return email_status
        
        return None

# Global Orchestrator Instance
outreach_orchestrator = OutreachOrchestrator()
