from data.states import STATE_DOC_FEE_CAPS


def mock_auto_purchase_analysis(contract_text: str, state: str = None, vehicle_price: int = None, trade_in_value: int = None) -> dict:
    """Generate mock auto purchase analysis"""
    text_lower = contract_text.lower()

    red_flags = []
    risk_score = 25

    # Detect financing type
    if 'lease' in text_lower:
        financing_type = "lease"
    elif 'cash' in text_lower and 'finance' not in text_lower:
        financing_type = "cash"
    elif 'finance' in text_lower or 'loan' in text_lower or 'apr' in text_lower:
        financing_type = "financing"
    else:
        financing_type = "unknown"

    has_yoyo_financing = False

    # Check for yo-yo financing / spot delivery
    if 'spot delivery' in text_lower or 'conditional' in text_lower or 'subject to financing' in text_lower:
        has_yoyo_financing = True
        red_flags.append({
            "name": "Yo-Yo Financing",
            "severity": "critical",
            "clause_text": "Delivery is conditional and subject to final financing approval...",
            "explanation": "The dealer lets you drive off the lot before financing is final. Days later they call saying 'the deal fell through' and demand worse terms or the car back. This is a classic pressure tactic.",
            "what_to_ask": "Refuse spot delivery. Insist on final financing approval BEFORE taking the vehicle. If they already got you, check your state's yo-yo financing laws."
        })
        risk_score += 25

    # Check for nitrogen tire fill scam
    if 'nitrogen' in text_lower or 'tire fill' in text_lower:
        red_flags.append({
            "name": "Nitrogen Tire Fill Scam",
            "severity": "warning",
            "clause_text": "Premium nitrogen tire inflation service...",
            "explanation": "Dealers charge $200-$500 for nitrogen in tires. Air is already 78% nitrogen. This provides negligible benefit for passenger vehicles.",
            "what_to_ask": "Decline this add-on. It's pure profit for the dealer with virtually no benefit to you."
        })
        risk_score += 10

    # Check for VIN etching markup
    if 'vin etch' in text_lower or 'vin etching' in text_lower:
        red_flags.append({
            "name": "VIN Etching Markup",
            "severity": "warning",
            "clause_text": "Vehicle identification number etching theft deterrent package...",
            "explanation": "Dealers charge $300-$1,000 for VIN etching that costs $30 as a DIY kit. Some states require disclosure that it's optional.",
            "what_to_ask": "Decline it. If you want VIN etching, buy a $30 kit and do it yourself."
        })
        risk_score += 10

    # Check for mandatory arbitration
    if 'arbitration' in text_lower:
        red_flags.append({
            "name": "Mandatory Arbitration",
            "severity": "warning",
            "clause_text": "Any disputes arising from this purchase shall be resolved through binding arbitration...",
            "explanation": "You're giving up your right to sue the dealer in court. Arbitration typically favors repeat-player dealers.",
            "what_to_ask": "Try to strike this clause. If you can't, look for a 30-day opt-out provision."
        })
        risk_score += 10

    # Check for doc fee
    if 'doc fee' in text_lower or 'documentation fee' in text_lower:
        if state and state.upper() in STATE_DOC_FEE_CAPS:
            cap_info = STATE_DOC_FEE_CAPS[state.upper()]
            red_flags.append({
                "name": "Documentation Fee - Check Against State Cap",
                "severity": "critical",
                "clause_text": "Documentation/processing fee...",
                "explanation": f"Your state ({state.upper()}) caps doc fees at ${cap_info['cap']:,}. If the dealer is charging more than this, they're breaking the law.",
                "what_to_ask": f"Verify the doc fee doesn't exceed ${cap_info['cap']:,} ({state.upper()} cap). If it does, demand they reduce it and report them to your state AG."
            })
            risk_score += 15
        else:
            red_flags.append({
                "name": "Documentation Fee",
                "severity": "warning",
                "clause_text": "Documentation/processing fee...",
                "explanation": "Doc fees vary widely. Some states cap them, others don't. Typical range is $75-$700 but some dealers charge over $1,000.",
                "what_to_ask": "Ask what the doc fee covers. Compare to other dealers in your area. This fee is negotiable at many dealerships."
            })
            risk_score += 10

    # Check for dealer markup / ADM
    if 'markup' in text_lower or 'adm' in text_lower or 'market adjustment' in text_lower:
        red_flags.append({
            "name": "Dealer Markup / ADM",
            "severity": "warning",
            "clause_text": "Additional dealer markup / market adjustment...",
            "explanation": "The dealer is adding a markup above MSRP. This is especially common on high-demand vehicles. It's legal but negotiable.",
            "what_to_ask": "Walk away. Check other dealers. Use online buying services. Dealer markups are pure profit with zero added value."
        })
        risk_score += 15

    # Check for GAP insurance
    if 'gap insurance' in text_lower or 'gap waiver' in text_lower:
        red_flags.append({
            "name": "GAP Insurance at Dealer",
            "severity": "minor",
            "clause_text": "Guaranteed Asset Protection (GAP) coverage...",
            "explanation": "GAP insurance itself is useful if you owe more than the car is worth. But dealers mark it up 200-300%. Your regular insurer or credit union offers the same thing for $20-$50/year.",
            "what_to_ask": "Don't buy GAP from the dealer. Get it from your auto insurance company or credit union for a fraction of the cost."
        })
        risk_score += 5

    # Check for extended warranty / packed products
    if 'extended warranty' in text_lower or 'service contract' in text_lower:
        red_flags.append({
            "name": "Packed Products",
            "severity": "warning",
            "clause_text": "Extended vehicle service contract / protection plan...",
            "explanation": "The F&I office often 'packs' the payment with extras you didn't ask for. The monthly payment quote already includes these add-ons, making you think they're included in the car price.",
            "what_to_ask": "Ask to see the itemized breakdown. Decline all add-ons initially. If you want an extended warranty, shop third-party providers after purchase."
        })
        risk_score += 10

    # Always add boilerplate
    red_flags.append({
        "name": "Standard Odometer Disclosure",
        "severity": "boilerplate",
        "clause_text": None,
        "explanation": "Federal law requires odometer disclosure on all vehicle sales. This is completely standard and protects you as the buyer.",
        "what_to_ask": "No action needed - this is a legal requirement that protects you."
    })
    red_flags.append({
        "name": "Buyer's Order / Purchase Agreement",
        "severity": "boilerplate",
        "clause_text": None,
        "explanation": "The standard buyer's order format listing vehicle details, price, and terms. Every dealership uses this.",
        "what_to_ask": "No action needed - just verify the details match what you agreed to."
    })

    # Cap risk score
    risk_score = min(100, risk_score)

    # Determine overall risk
    if risk_score >= 60:
        overall_risk = "high"
    elif risk_score >= 35:
        overall_risk = "medium"
    else:
        overall_risk = "low"

    # State protections
    state_protections = []
    if state:
        state_upper = state.upper()
        state_protections.append(f"Check {state_upper}'s lemon law protections for new vehicles")
        state_protections.append(f"Check {state_upper}'s used car return/cooling-off rights (if any)")
        if state_upper in STATE_DOC_FEE_CAPS:
            cap_info = STATE_DOC_FEE_CAPS[state_upper]
            state_protections.append(f"{state_upper} caps documentation fees at ${cap_info['cap']:,}")
        state_protections.append(f"File complaints with {state_upper} Attorney General or DMV if dealer violates the law")

    # Generate summary
    critical_count = len([r for r in red_flags if r['severity'] == 'critical'])
    warning_count = len([r for r in red_flags if r['severity'] == 'warning'])

    if critical_count > 0:
        summary = f"This purchase agreement has {critical_count} critical issue(s) that could cost you thousands. "
    else:
        summary = "This purchase agreement has some common dealer tactics to watch for. "

    if has_yoyo_financing:
        summary += "WARNING: This appears to be a spot delivery / yo-yo financing deal. Do NOT sign until financing is final. "
    if warning_count > 0:
        summary += f"There are {warning_count} additional items you should negotiate or decline."

    # Generate demand letter
    letter_items = []
    for rf in red_flags:
        if rf['severity'] in ('critical', 'warning'):
            letter_items.append(f"- {rf['name']}: {rf['what_to_ask']}")

    demand_letter = f"""RE: Vehicle Purchase Agreement - Objections and Requested Modifications

Dear Dealer/Finance Manager,

I have reviewed the purchase agreement and identified the following issues that must be addressed before I will proceed:

ISSUES IDENTIFIED:
{chr(10).join(letter_items) if letter_items else '- No critical issues identified'}

DEMANDS:
1. Remove all add-on products I did not explicitly request
2. Provide an itemized breakdown of ALL fees
3. Confirm final financing terms BEFORE delivery
4. Reduce documentation fee to a reasonable amount
5. Remove any dealer markup above MSRP

I am prepared to purchase this vehicle at a fair price with transparent terms. If these issues cannot be resolved, I will take my business elsewhere.

Please provide a revised purchase agreement within 24 hours.

Sincerely,
[Your Name]
[Date]

NOTE: Keep a copy of this letter and all documents. Record conversations if legal in your state (check one-party vs two-party consent)."""

    return {
        "overall_risk": overall_risk,
        "risk_score": risk_score,
        "dealer_name": None,
        "vehicle_description": None,
        "financing_type": financing_type,
        "has_yoyo_financing": has_yoyo_financing,
        "total_junk_fees": None,
        "red_flags": red_flags,
        "state_protections": state_protections,
        "summary": summary,
        "demand_letter": demand_letter
    }
