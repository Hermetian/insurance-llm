from pydantic import BaseModel
from typing import Optional


class DebtSettlementRedFlag(BaseModel):
    name: str
    severity: str
    clause_text: Optional[str] = None
    explanation: str
    what_to_ask: str


class DebtSettlementInput(BaseModel):
    contract_text: str
    state: Optional[str] = None
    debt_amount: Optional[float] = None


class DebtSettlementReport(BaseModel):
    overall_risk: str
    risk_score: int
    company_name: Optional[str] = None
    settlement_type: Optional[str] = None
    has_paid_in_full: bool
    has_tax_warning: bool
    resets_statute_of_limitations: bool
    red_flags: list[DebtSettlementRedFlag]
    missing_protections: list[str]
    summary: str
    settlement_letter: str
    document_hash: Optional[str] = None
    is_premium: bool = False
    total_issues: Optional[int] = None
