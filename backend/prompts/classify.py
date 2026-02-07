CLASSIFY_PROMPT = """Classify this document into one of these categories:
- "coi" = Certificate of Insurance (ACORD 25 form, insurance certificate, proof of coverage)
- "lease" = Property Lease (rental agreement, commercial lease, residential lease)
- "gym_contract" = Gym/Fitness Membership (gym membership, fitness center contract, health club agreement)
- "employment_contract" = Employment Contract (offer letter, employment agreement, employee handbook with arbitration/non-compete)
- "freelancer_contract" = Freelancer/Contractor Agreement (independent contractor, consulting, freelance, SOW)
- "influencer_contract" = Influencer/Sponsorship (brand deal, sponsorship, content creator agreement, influencer contract)
- "insurance_policy" = Full Insurance Policy (declarations page, policy document, coverage details)
- "timeshare_contract" = Timeshare Contract (vacation ownership, timeshare purchase, resort membership)
- "auto_purchase" = Auto Purchase Contract (vehicle purchase, car buying, dealer agreement, financing)
- "home_improvement" = Home Improvement Contract (contractor agreement, renovation, remodeling, construction)
- "nursing_home" = Nursing Home Agreement (admission agreement, assisted living, skilled nursing, long-term care)
- "subscription" = Subscription/SaaS Agreement (subscription, recurring billing, SaaS terms, membership service)
- "debt_settlement" = Debt Settlement Agreement (debt collection, settlement offer, payment plan, debt relief)
- "contract" = Other Contract (service agreement, vendor contract, NDA, etc.)
- "unknown" = Cannot determine

Look for key indicators:
- COI: "CERTIFICATE OF LIABILITY INSURANCE", "ACORD", "CERTIFICATE HOLDER", "ADDITIONAL INSURED"
- Lease: "LEASE AGREEMENT", "LANDLORD", "TENANT", "RENT", "PREMISES", "TERM"
- Gym: "MEMBERSHIP", "FITNESS", "GYM", "HEALTH CLUB", "CANCEL", "DUES", "MONTHLY FEE"
- Employment: "EMPLOYMENT", "EMPLOYEE", "NON-COMPETE", "ARBITRATION", "AT-WILL", "TERMINATION", "SALARY"
- Freelancer: "INDEPENDENT CONTRACTOR", "FREELANCE", "CONSULTING", "DELIVERABLES", "SOW", "WORK FOR HIRE"
- Influencer: "BRAND", "SPONSOR", "INFLUENCER", "CONTENT", "DELIVERABLES", "USAGE RIGHTS", "EXCLUSIVITY", "CAMPAIGN"
- Insurance Policy: "DECLARATIONS", "POLICY NUMBER", "COVERAGE", "PREMIUM", "ENDORSEMENT"
- Timeshare: "TIMESHARE", "VACATION OWNERSHIP", "RESORT", "INTERVAL", "MAINTENANCE FEE", "DEEDED", "RIGHT TO USE"
- Auto Purchase: "VEHICLE", "DEALER", "VIN", "TRADE-IN", "FINANCING", "MSRP", "DOC FEE", "BUYER'S ORDER"
- Home Improvement: "CONTRACTOR", "RENOVATION", "REMODEL", "LIEN WAIVER", "CHANGE ORDER", "COMPLETION DATE", "SCOPE OF WORK"
- Nursing Home: "ADMISSION", "NURSING", "ASSISTED LIVING", "RESIDENT", "SKILLED NURSING", "RESPONSIBLE PARTY", "FACILITY"
- Subscription: "SUBSCRIPTION", "RECURRING", "AUTO-RENEW", "SAAS", "CANCEL", "BILLING CYCLE", "FREE TRIAL"
- Debt Settlement: "SETTLEMENT", "DEBT", "CREDITOR", "COLLECTION", "PAID IN FULL", "BALANCE", "PAYMENT PLAN"
- Contract: "AGREEMENT", "PARTIES", "TERMS AND CONDITIONS", "WHEREAS"

Return JSON only:
{"type": "coi|lease|insurance_policy|contract|unknown", "confidence": 0.0-1.0, "reason": "brief explanation"}"""

OCR_PROMPT = """Extract ALL text from this document image. This is likely an insurance document, certificate of insurance (COI), policy, lease, or contract.

Return the text exactly as it appears, preserving:
- Line breaks and formatting
- Checkbox status (show as [X] for checked, [ ] for unchecked)
- Tables and columns (use spacing to preserve alignment)
- Headers and section titles
- All numbers, dates, and dollar amounts exactly as written

Do not summarize or interpret - just extract the raw text content."""
