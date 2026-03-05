from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class LeadBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    job_title: Optional[str] = None
    company_name: Optional[str] = None

class LeadEnrichment(BaseModel):
    lead_id: UUID
    source: str
    extracted_facts: Dict[str, Any]
    raw_data: Optional[Dict[str, Any]] = None

class QualificationScore(BaseModel):
    lead_id: UUID
    score: int = Field(ge=0, le=100)
    reasoning: str
    criteria_met: Dict[str, bool]
