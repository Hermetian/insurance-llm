from pydantic import BaseModel
from typing import Optional


class AutoPurchaseRedFlag(BaseModel):
    name: str
    severity: str
    clause_text: Optional[str] = None
    explanation: str
    what_to_ask: str


class AutoPurchaseInput(BaseModel):
    contract_text: str
    state: Optional[str] = None
    vehicle_price: Optional[float] = None
    trade_in_value: Optional[float] = None


class AutoPurchaseReport(BaseModel):
    overall_risk: str
    risk_score: int
    dealer_name: Optional[str] = None
    vehicle_description: Optional[str] = None
    financing_type: Optional[str] = None
    has_yoyo_financing: bool
    total_junk_fees: Optional[float] = None
    red_flags: list[AutoPurchaseRedFlag]
    state_protections: list[str]
    summary: str
    demand_letter: str
    document_hash: Optional[str] = None
    is_premium: bool = False
    total_issues: Optional[int] = None
