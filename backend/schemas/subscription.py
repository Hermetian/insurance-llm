from pydantic import BaseModel
from typing import Optional


class SubscriptionRedFlag(BaseModel):
    name: str
    severity: str
    clause_text: Optional[str] = None
    explanation: str
    what_to_ask: str


class SubscriptionInput(BaseModel):
    contract_text: str
    monthly_cost: Optional[float] = None


class SubscriptionReport(BaseModel):
    overall_risk: str
    risk_score: int
    service_name: Optional[str] = None
    subscription_type: Optional[str] = None
    has_auto_renewal: bool
    cancellation_difficulty: str
    has_price_increase_clause: bool
    red_flags: list[SubscriptionRedFlag]
    dark_patterns: list[str]
    summary: str
    cancellation_guide: str
    document_hash: Optional[str] = None
    is_premium: bool = False
    total_issues: Optional[int] = None
