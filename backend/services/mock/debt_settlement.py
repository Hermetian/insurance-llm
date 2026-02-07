from data.states import STATE_DEBT_SOL


def mock_debt_settlement_analysis(contract_text: str, state: str = None, debt_amount: int = None) -> dict:
    """Generate mock debt settlement agreement analysis"""
    text_lower = contract_text.lower()

    red_flags = []
    missing_protections = []
    risk_score = 30

    # Detect settlement type
    if 'credit card' in text_lower:
        settlement_type = "credit_card"
    elif 'medical' in text_lower or 'hospital' in text_lower:
        settlement_type = "medical"
    elif 'student loan' in text_lower:
        settlement_type = "student_loan"
    elif 'mortgage' in text_lower or 'home' in text_lower:
        settlement_type = "mortgage_deficiency"
    elif 'auto' in text_lower or 'vehicle' in text_lower or 'car' in text_lower:
        settlement_type = "auto_deficiency"
    elif 'collection' in text_lower or 'collector' in text_lower:
        settlement_type = "collections"
    else:
        settlement_type = "general"

    has_paid_in_full = False
    has_tax_warning = False
    resets_statute_of_limitations = False

    # Check for missing paid-in-full language
    if 'paid in full' not in text_lower and 'settled in full' not in text_lower and 'satisfaction' not in text_lower:
        red_flags.append({
            "name": "Missing Paid-in-Full Language",
            "severity": "critical",
            "clause_text": "(No 'paid in full' or 'settled in full' language found in agreement)",
            "explanation": "Without explicit language that the debt is settled/paid in full upon payment, the creditor can sell the remaining balance to another collector. You could end up paying twice.",
            "what_to_ask": "INSIST on language stating the debt is 'settled in full' or 'paid in full' and that the creditor waives all rights to collect the remaining balance. Get this in writing BEFORE sending any money."
        })
        missing_protections.append("'Paid in full' or 'settled in full' language")
        risk_score += 20
    else:
        has_paid_in_full = True

    # Check for statute of limitations reset
    if 'statute of limitations' in text_lower and ('reset' in text_lower or 'restart' in text_lower or 'new' in text_lower):
        resets_statute_of_limitations = True
        red_flags.append({
            "name": "Statute of Limitations Reset",
            "severity": "critical",
            "clause_text": "Debtor acknowledges this agreement may reset the statute of limitations...",
            "explanation": "Making a payment or acknowledging the debt can RESTART the clock on the statute of limitations. If your debt was near expiration, this agreement could give them years more to sue you.",
            "what_to_ask": "Check your state's statute of limitations for this type of debt. If the debt is near or past the SOL, making any payment or written acknowledgment could reset it. Consult a consumer attorney."
        })
        risk_score += 25
    elif 'acknowledge' in text_lower and 'debt' in text_lower:
        resets_statute_of_limitations = True
        red_flags.append({
            "name": "Statute of Limitations Reset",
            "severity": "critical",
            "clause_text": "Debtor acknowledges the validity of the debt...",
            "explanation": "Acknowledging the debt in writing can restart the statute of limitations in many states. If this debt is old, you may be giving up a powerful defense.",
            "what_to_ask": "Before acknowledging ANY debt in writing, check if the statute of limitations has expired. If it has, you may have no legal obligation to pay. Consult a consumer attorney."
        })
        risk_score += 25

    # Check for no tax disclosure
    if 'tax' not in text_lower and '1099' not in text_lower and 'irs' not in text_lower:
        red_flags.append({
            "name": "No Tax Disclosure",
            "severity": "warning",
            "clause_text": "(No mention of tax implications found in agreement)",
            "explanation": "Forgiven debt over $600 is reported to the IRS as income on a 1099-C. If you settle $20,000 of debt for $8,000, you may owe income tax on the $12,000 'forgiven.' This can be a surprise tax bill of $2,000-$4,000.",
            "what_to_ask": "Ask the creditor if they will issue a 1099-C. Consult a tax professional about the insolvency exception (IRS Form 982) - if your debts exceeded your assets at the time of settlement, you may not owe taxes."
        })
        missing_protections.append("Tax implication disclosure (1099-C)")
        risk_score += 15
    else:
        has_tax_warning = True

    # Check for illegal upfront fees
    if 'upfront fee' in text_lower or 'advance fee' in text_lower or ('fee' in text_lower and 'before' in text_lower and 'settlement' in text_lower):
        red_flags.append({
            "name": "Illegal Upfront Fees",
            "severity": "critical",
            "clause_text": "Client agrees to pay a program fee before settlement is reached...",
            "explanation": "The FTC's Telemarketing Sales Rule (TSR) PROHIBITS debt settlement companies from charging fees before they actually settle a debt. If they're demanding money upfront, they're likely breaking the law.",
            "what_to_ask": "Refuse to pay any fees until a settlement is reached AND you have agreed to the settlement terms. Report companies demanding upfront fees to the FTC and your state AG."
        })
        missing_protections.append("Compliance with FTC Telemarketing Sales Rule (no advance fees)")
        risk_score += 20

    # Check for right to sell remaining debt
    if ('sell' in text_lower or 'transfer' in text_lower or 'assign' in text_lower) and ('remaining' in text_lower or 'balance' in text_lower or 'debt' in text_lower):
        red_flags.append({
            "name": "Right to Sell Remaining Debt",
            "severity": "warning",
            "clause_text": "Creditor reserves the right to sell, transfer, or assign the remaining balance...",
            "explanation": "Even after settlement, they can sell whatever you didn't pay to a debt buyer. That buyer can then come after you for the difference. This defeats the purpose of settling.",
            "what_to_ask": "Insist the agreement includes language that the creditor waives all rights to the remaining balance and will not sell, transfer, or assign it. Without this, your settlement isn't really settled."
        })
        risk_score += 15

    # Check for no written confirmation
    if 'written' not in text_lower and 'writing' not in text_lower and 'confirmation' not in text_lower:
        red_flags.append({
            "name": "No Written Confirmation",
            "severity": "warning",
            "clause_text": "(No written confirmation requirement found in agreement)",
            "explanation": "Without a requirement for written confirmation that the debt is settled after payment, you have no proof. The creditor or a future buyer could claim you still owe.",
            "what_to_ask": "Insist on written confirmation that the debt is settled in full, sent within 30 days of final payment. Keep this document forever."
        })
        missing_protections.append("Written confirmation of settlement completion")
        risk_score += 10

    # Check for late payment default trap
    if ('late' in text_lower or 'miss' in text_lower) and ('default' in text_lower or 'payment' in text_lower) and ('void' in text_lower or 'null' in text_lower):
        red_flags.append({
            "name": "Late Payment Default Trap",
            "severity": "warning",
            "clause_text": "If any payment is late or missed, this agreement is void and the full original balance becomes due...",
            "explanation": "One late payment and the entire settlement is voided. You owe the full original amount again. Life happens - this gives you zero flexibility.",
            "what_to_ask": "Negotiate a grace period (at least 5-10 days) for late payments. Add language that one late payment triggers a notice, not immediate default."
        })
        risk_score += 10

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
        summary = f"This settlement agreement has {critical_count} critical issue(s) that could leave you worse off than before. "
    else:
        summary = "This settlement agreement has some gaps that should be addressed before you sign. "

    if not has_paid_in_full:
        summary += "CRITICAL: Without 'settled in full' language, they can sell the remaining balance to another collector. "
    if resets_statute_of_limitations:
        summary += "WARNING: This agreement may reset the statute of limitations on your debt. "

    # Add state-specific SOL info
    if state and state.upper() in STATE_DEBT_SOL:
        sol_info = STATE_DEBT_SOL[state.upper()]
        summary += f"\n\n{state.upper()} Statute of Limitations: {sol_info['years']} years. {sol_info.get('notes', '')}"

    # Generate settlement letter
    settlement_letter = f"""SETTLEMENT ACCEPTANCE LETTER TEMPLATE
(Send via Certified Mail - Return Receipt Requested)

Date: [TODAY'S DATE]

To: [CREDITOR/COLLECTOR NAME]
[ADDRESS]

RE: Settlement of Account
Account Number: [ACCOUNT NUMBER]
Original Creditor: [IF DIFFERENT FROM ABOVE]
Original Balance: ${f'{debt_amount:,.2f}' if debt_amount else '[ORIGINAL AMOUNT]'}
Settlement Amount: $[AGREED SETTLEMENT AMOUNT]

Dear Sir/Madam:

This letter confirms the settlement agreement reached on [DATE] regarding the above-referenced account.

TERMS I AM ACCEPTING:
1. I will pay $[SETTLEMENT AMOUNT] as full and final settlement of this debt
2. Payment will be made via [cashier's check/money order] (NEVER give bank account access)
3. Payment schedule: [LUMP SUM DATE or PAYMENT SCHEDULE]

TERMS I REQUIRE (must be confirmed in writing before I send payment):
1. Upon receipt of the settlement amount, the debt is SETTLED IN FULL
2. You will report the account as "Paid in Full" or "Settled" to all credit bureaus
3. You waive all rights to collect the remaining balance
4. You will NOT sell, transfer, or assign the remaining balance to any third party
5. You will provide written confirmation of settlement within 30 days of final payment
6. No further collection activity will occur on this account

IMPORTANT: I will NOT send payment until I receive written confirmation of these terms on your company letterhead.

DO NOT contact me by phone regarding this matter. All communication must be in writing.

Sincerely,

[YOUR NAME]
[YOUR ADDRESS]

KEEP THE CERTIFIED MAIL RECEIPT AND ALL CORRESPONDENCE

---
NOTES FOR YOU (do not include in actual letter):
- NEVER pay by personal check or give bank account access
- Use cashier's check or money order only
- Keep copies of everything for at least 7 years
- Check your credit reports 60 days after settlement
- Consult a tax professional about potential 1099-C income
- If the debt is past the statute of limitations, consider not paying at all"""

    return {
        "overall_risk": overall_risk,
        "risk_score": risk_score,
        "company_name": None,
        "settlement_type": settlement_type,
        "has_paid_in_full": has_paid_in_full,
        "has_tax_warning": has_tax_warning,
        "resets_statute_of_limitations": resets_statute_of_limitations,
        "red_flags": red_flags,
        "missing_protections": missing_protections,
        "summary": summary,
        "settlement_letter": settlement_letter
    }
