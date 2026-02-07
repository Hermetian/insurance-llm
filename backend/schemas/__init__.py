from schemas.common import (
    DocumentInput, Coverage, ExtractedPolicy, FieldConfidence,
    COIData, ExtractionMetadata, ComplianceRequirement, ComplianceReport,
    COIComplianceInput, OCRInput, ClassifyInput, ClassifyResult,
    WaitlistInput, WaitlistResponse
)
from schemas.auth import SignupInput, LoginInput, AuthResponse, UserInfo, CheckoutInput
from schemas.lease import LeaseInsuranceClause, LeaseRedFlag, LeaseAnalysisInput, LeaseAnalysisReport
from schemas.gym import GymRedFlag, GymContractInput, GymContractReport
from schemas.employment import EmploymentRedFlag, EmploymentContractInput, EmploymentContractReport
from schemas.freelancer import FreelancerRedFlag, FreelancerContractInput, FreelancerContractReport
from schemas.influencer import InfluencerRedFlag, InfluencerContractInput, InfluencerContractReport
from schemas.timeshare import TimeshareRedFlag, TimeshareContractInput, TimeshareContractReport
from schemas.insurance_policy import InsurancePolicyRedFlag, InsurancePolicyInput, InsurancePolicyReport
from schemas.auto_purchase import AutoPurchaseRedFlag, AutoPurchaseInput, AutoPurchaseReport
from schemas.home_improvement import HomeImprovementRedFlag, HomeImprovementInput, HomeImprovementReport
from schemas.nursing_home import NursingHomeRedFlag, NursingHomeInput, NursingHomeReport
from schemas.subscription import SubscriptionRedFlag, SubscriptionInput, SubscriptionReport
from schemas.debt_settlement import DebtSettlementRedFlag, DebtSettlementInput, DebtSettlementReport
