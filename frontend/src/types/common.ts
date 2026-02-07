// Document classification result
export interface ClassifyResult {
  document_type: 'coi' | 'lease' | 'gym' | 'timeshare' | 'influencer' | 'freelancer' | 'employment' | 'insurance_policy' | 'auto_purchase' | 'home_improvement' | 'nursing_home' | 'subscription' | 'debt_settlement' | 'contract' | 'unknown'
  confidence: number
  description: string
  supported: boolean
}
