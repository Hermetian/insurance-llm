from pydantic import BaseModel
from typing import Optional


class NursingHomeRedFlag(BaseModel):
    name: str
    severity: str
    clause_text: Optional[str] = None
    explanation: str
    what_to_ask: str


class NursingHomeInput(BaseModel):
    contract_text: str
    state: Optional[str] = None


class NursingHomeReport(BaseModel):
    overall_risk: str
    risk_score: int
    facility_name: Optional[str] = None
    agreement_type: Optional[str] = None
    has_responsible_party_clause: bool
    has_forced_arbitration: bool
    has_liability_waiver: bool
    red_flags: list[NursingHomeRedFlag]
    illegal_clauses: list[str]
    summary: str
    rights_guide: str
    document_hash: Optional[str] = None
    is_premium: bool = False
    total_issues: Optional[int] = None
