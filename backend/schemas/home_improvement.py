from pydantic import BaseModel
from typing import Optional


class HomeImprovementRedFlag(BaseModel):
    name: str
    severity: str
    clause_text: Optional[str] = None
    explanation: str
    what_to_ask: str


class HomeImprovementInput(BaseModel):
    contract_text: str
    state: Optional[str] = None
    project_cost: Optional[float] = None


class HomeImprovementReport(BaseModel):
    overall_risk: str
    risk_score: int
    contractor_name: Optional[str] = None
    project_type: Optional[str] = None
    payment_structure: Optional[str] = None
    has_lien_waiver: bool
    has_change_order_process: bool
    red_flags: list[HomeImprovementRedFlag]
    missing_protections: list[str]
    summary: str
    protection_checklist: str
    document_hash: Optional[str] = None
    is_premium: bool = False
    total_issues: Optional[int] = None
