import json
import logging
import os
from typing import Dict, Any, List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

# Setup logging for DB operations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("database-repo")

class RevOpsRepository:
    """Encapsulates all PostgreSQL operations for the Digital FTE (ADR-3)."""

    def __init__(self):
        # Default to a local DB if env var is not set
        self.db_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/revops_db")
        self.engine = create_async_engine(self.db_url, echo=False)
        self.AsyncSessionLocal = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_db(self):
        async with self.AsyncSessionLocal() as session:
            yield session

    async def save_lead_intake(self, lead_data: Dict[str, Any]) -> UUID:
        """Saves a new lead ingested via Gateway."""
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                # 1. Upsert Company
                company_name = lead_data.get("company_name")
                company_id = None
                if company_name:
                    result = await session.execute(
                        text("INSERT INTO companies (name) VALUES (:name) ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name RETURNING id"),
                        {"name": company_name}
                    )
                    company_id = result.scalar()

                # 2. Insert Lead
                result = await session.execute(
                    text("""
                        INSERT INTO leads (first_name, last_name, email, job_title, company_id, source)
                        VALUES (:first_name, :last_name, :email, :job_title, :company_id, :source)
                        RETURNING id
                    """),
                    {
                        "first_name": lead_data.get("first_name"),
                        "last_name": lead_data.get("last_name"),
                        "email": lead_data.get("email"),
                        "job_title": lead_data.get("job_title"),
                        "company_id": company_id,
                        "source": "API_GATEWAY"
                    }
                )
                lead_id = result.scalar()
                logger.info(f"[DB] Lead saved: {lead_data['email']} (ID: {lead_id})")
                return lead_id

    async def save_enrichment(self, lead_id: UUID, source: str, facts: Dict[str, Any], raw: Dict[str, Any]):
        """Saves research findings from the Agent Worker."""
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                await session.execute(
                    text("""
                        INSERT INTO enrichments (lead_id, source, extracted_facts, raw_data)
                        VALUES (:lead_id, :source, :facts, :raw)
                    """),
                    {
                        "lead_id": lead_id,
                        "source": source,
                        "facts": json.dumps(facts),
                        "raw": json.dumps(raw)
                    }
                )
                logger.info(f"[DB] Enrichment saved for {lead_id} from {source}")
        return True

    async def save_qualification_result(self, lead_id: UUID, score: int, reasoning: str, criteria: Dict[str, bool]):
        """Saves the final qualification decision and reasoning."""
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                await session.execute(
                    text("""
                        INSERT INTO qualification_results (lead_id, score, reasoning, criteria_met)
                        VALUES (:lead_id, :score, :reasoning, :criteria)
                    """),
                    {
                        "lead_id": lead_id,
                        "score": score,
                        "reasoning": reasoning,
                        "criteria": json.dumps(criteria)
                    }
                )
                logger.info(f"[DB] Qualification saved for {lead_id} with score {score}")
        return True

    async def log_agent_action(self, lead_id: UUID, step: str, audit_data: Dict[str, Any]):
        """Saves a detailed audit log of an agent's reasoning step (ADR-3)."""
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                await session.execute(
                    text("""
                        INSERT INTO agent_audit_logs (lead_id, step_name, details)
                        VALUES (:lead_id, :step, :details)
                    """),
                    {
                        "lead_id": lead_id,
                        "step": step,
                        "details": json.dumps(audit_data)
                    }
                )
                logger.info(f"[AUDIT] Logged {step} for {lead_id}")
        return True

# Global Repository Instance
db_repo = RevOpsRepository()
