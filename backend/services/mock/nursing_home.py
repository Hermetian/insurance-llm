def mock_nursing_home_analysis(contract_text: str, state: str = None) -> dict:
    """Generate mock nursing home agreement analysis"""
    text_lower = contract_text.lower()

    red_flags = []
    illegal_clauses = []
    risk_score = 40  # Inherently high stakes

    # Detect agreement type
    if 'assisted living' in text_lower:
        agreement_type = "assisted_living"
    elif 'memory care' in text_lower or 'dementia' in text_lower or 'alzheimer' in text_lower:
        agreement_type = "memory_care"
    elif 'skilled nursing' in text_lower or 'snf' in text_lower:
        agreement_type = "skilled_nursing"
    elif 'hospice' in text_lower:
        agreement_type = "hospice"
    elif 'rehab' in text_lower or 'rehabilitation' in text_lower:
        agreement_type = "rehabilitation"
    else:
        agreement_type = "nursing_home"

    has_responsible_party_clause = False
    has_forced_arbitration = False
    has_liability_waiver = False

    # Check for illegal responsible party / guarantor clause
    if 'responsible party' in text_lower or 'guarantor' in text_lower or 'guarantee payment' in text_lower:
        has_responsible_party_clause = True
        clause = {
            "name": "Illegal Responsible Party Clause",
            "severity": "critical",
            "clause_text": "A responsible party/guarantor must sign and agree to be personally liable for all charges...",
            "explanation": "Federal law (Nursing Home Reform Act) PROHIBITS facilities from requiring a third party to guarantee payment as a condition of admission. This is flat-out illegal. They're trying to make family members personally liable for bills.",
            "what_to_ask": "Refuse to sign as guarantor. Tell them this violates 42 CFR 483.15(a)(3). You can sign as the resident's representative (authorized to manage their funds) without being personally liable."
        }
        red_flags.append(clause)
        illegal_clauses.append("Responsible Party / Personal Guarantee — violates 42 CFR 483.15(a)(3). Facilities cannot require third-party guarantee of payment as condition of admission. Refuse to sign.")
        risk_score += 25

    # Check for forced arbitration
    if 'arbitration' in text_lower:
        has_forced_arbitration = True
        red_flags.append({
            "name": "Forced Arbitration",
            "severity": "critical",
            "clause_text": "All disputes, including claims of negligence, abuse, or wrongful death, shall be resolved through binding arbitration...",
            "explanation": "If the facility neglects or abuses your loved one, you can't sue them in court. CMS tried to ban this in 2016 but the rule was reversed. You can still refuse to sign it.",
            "what_to_ask": "Refuse to sign the arbitration agreement. It is ALWAYS separate and ALWAYS optional - they cannot deny admission for refusing. If they try, report them."
        })
        risk_score += 15

    # Check for broad liability waiver
    if 'waiver of liability' in text_lower or 'hold harmless' in text_lower or 'not responsible for' in text_lower:
        has_liability_waiver = True
        red_flags.append({
            "name": "Broad Liability Waiver",
            "severity": "critical",
            "clause_text": "The facility shall not be responsible for injuries, illness, or death resulting from...",
            "explanation": "The facility is trying to shield itself from liability for its own negligence. Nursing homes have a legal duty of care that cannot be waived by contract.",
            "what_to_ask": "Strike this clause. A facility's duty of care is non-waivable under federal and state law. If they refuse, this is a major red flag about their care quality."
        })
        risk_score += 15

    # Check for improper discharge threat
    if 'discharge' in text_lower and ('immediately' in text_lower or 'without notice' in text_lower):
        red_flags.append({
            "name": "Improper Discharge Threat",
            "severity": "warning",
            "clause_text": "Facility reserves the right to discharge resident immediately...",
            "explanation": "Federal law requires 30 days written notice before discharge (with very limited exceptions for safety). Immediate discharge clauses violate resident rights.",
            "what_to_ask": "Strike this clause. Cite 42 CFR 483.15(c) - facilities must provide 30-day written notice and a safe discharge plan. You have the right to appeal."
        })
        risk_score += 10

    # Check for 30-day notice waiver
    if '30-day' in text_lower and 'waive' in text_lower:
        red_flags.append({
            "name": "30-Day Notice Waiver",
            "severity": "warning",
            "clause_text": "Resident waives the right to 30-day written notice of discharge...",
            "explanation": "They're asking you to waive a federal right. The 30-day notice requirement exists to protect residents from being dumped without a safe plan.",
            "what_to_ask": "Do NOT waive this right. It is a federal protection under 42 CFR 483.15(c)(4). Cross this out and initial."
        })
        risk_score += 10

    # Check for blanket medical consent
    if 'consent to all' in text_lower or 'blanket consent' in text_lower or 'any and all treatment' in text_lower:
        red_flags.append({
            "name": "Blanket Medical Consent",
            "severity": "warning",
            "clause_text": "Resident consents to any and all treatments deemed necessary by the facility...",
            "explanation": "This attempts to bypass informed consent requirements. Every medical treatment requires separate, informed consent. A blanket waiver is not valid.",
            "what_to_ask": "Strike this clause. Insist on individual informed consent for each treatment. This is both a legal right and a medical ethics requirement."
        })
        risk_score += 10

    # Check for missing grievance process
    if 'grievance' not in text_lower and 'complaint' not in text_lower:
        red_flags.append({
            "name": "Missing Grievance Process",
            "severity": "warning",
            "clause_text": "(No grievance or complaint process found in agreement)",
            "explanation": "Federal law requires every facility to have a grievance process. If it's not in the contract, the facility may not be taking complaints seriously.",
            "what_to_ask": "Ask for the facility's written grievance policy. It must exist under federal law. If they can't produce one, this is a serious compliance concern."
        })
        risk_score += 10

    # Check for personal property disclaimer
    if 'personal property' in text_lower and ('not responsible' in text_lower or 'disclaim' in text_lower):
        red_flags.append({
            "name": "Personal Property Disclaimer",
            "severity": "info",
            "clause_text": "Facility is not responsible for loss of personal property...",
            "explanation": "While facilities aren't usually liable for minor personal items, they have a duty to safeguard resident property and must maintain an inventory.",
            "what_to_ask": "Ask about their personal property inventory process. Label all items. Keep an inventory with photos. Don't bring valuables."
        })
        risk_score += 5

    # Cap risk score
    risk_score = min(100, risk_score)

    # Determine overall risk
    if risk_score >= 60:
        overall_risk = "high"
    elif risk_score >= 35:
        overall_risk = "medium"
    else:
        overall_risk = "low"

    # Generate summary
    critical_count = len([r for r in red_flags if r['severity'] == 'critical'])

    if critical_count > 0:
        summary = f"This agreement has {critical_count} critical issue(s), including potentially illegal clauses. "
    else:
        summary = "This agreement has some concerning provisions that should be addressed. "

    if has_responsible_party_clause:
        summary += "IMPORTANT: The responsible party/guarantor clause is ILLEGAL under federal law. Do not sign it. "
    if has_forced_arbitration:
        summary += "The arbitration clause is optional - you can refuse without affecting admission."

    # Generate rights guide
    rights_guide = """NURSING HOME RESIDENT & FAMILY RIGHTS GUIDE:

FEDERAL RIGHTS (Cannot Be Waived by Contract):
- Right to be free from abuse, neglect, and exploitation
- Right to 30-day written notice before discharge
- Right to appeal a discharge decision
- Right to a safe discharge plan
- Right to informed consent for all medical treatments
- Right to file grievances without retaliation
- Right to privacy and dignity
- Right to manage personal funds (or designate a representative)
- Right to access medical records
- Right NOT to have a family member required as financial guarantor

WHAT TO DO IF RIGHTS ARE VIOLATED:
1. Document everything (dates, times, witnesses, photos)
2. File a grievance with the facility in writing
3. Contact your State Long-Term Care Ombudsman
4. File a complaint with your state health department
5. Report to CMS (Centers for Medicare & Medicaid Services)
6. Contact an elder law attorney

KEY CONTACTS:
- Eldercare Locator: (800) 677-1116
- State Ombudsman: Search at ltcombudsman.org
- Medicare: (800) MEDICARE (633-4227)
- Adult Protective Services: Contact your state APS

BEFORE SIGNING THE AGREEMENT:
[ ] Cross out any responsible party/guarantor clause
[ ] Refuse to sign the arbitration agreement (it's always optional)
[ ] Strike any liability waivers for facility negligence
[ ] Verify the grievance process is documented
[ ] Ask for a copy of the most recent state inspection report
[ ] Check the facility on Medicare's Care Compare (medicare.gov/care-compare)
[ ] Visit unannounced at different times of day before committing
[ ] Talk to other residents' family members"""

    return {
        "overall_risk": overall_risk,
        "risk_score": risk_score,
        "facility_name": None,
        "agreement_type": agreement_type,
        "has_responsible_party_clause": has_responsible_party_clause,
        "has_forced_arbitration": has_forced_arbitration,
        "has_liability_waiver": has_liability_waiver,
        "red_flags": red_flags,
        "illegal_clauses": illegal_clauses,
        "summary": summary,
        "rights_guide": rights_guide
    }
