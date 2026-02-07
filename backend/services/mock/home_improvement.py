def mock_home_improvement_analysis(contract_text: str, state: str = None, project_cost: int = None) -> dict:
    """Generate mock home improvement contract analysis"""
    text_lower = contract_text.lower()

    red_flags = []
    missing_protections = []
    risk_score = 20

    # Detect project type
    if 'roof' in text_lower:
        project_type = "roofing"
    elif 'kitchen' in text_lower or 'bathroom' in text_lower or 'remodel' in text_lower:
        project_type = "remodel"
    elif 'hvac' in text_lower or 'heating' in text_lower or 'air condition' in text_lower:
        project_type = "hvac"
    elif 'plumb' in text_lower:
        project_type = "plumbing"
    elif 'electr' in text_lower or 'wiring' in text_lower:
        project_type = "electrical"
    elif 'paint' in text_lower:
        project_type = "painting"
    elif 'deck' in text_lower or 'patio' in text_lower or 'fence' in text_lower:
        project_type = "outdoor"
    elif 'addition' in text_lower or 'build' in text_lower:
        project_type = "addition"
    else:
        project_type = "general"

    has_lien_waiver = False
    has_change_order_process = False

    # Check for front-loaded payment
    if ('50%' in text_lower or 'half' in text_lower) and ('upfront' in text_lower or 'deposit' in text_lower or 'down' in text_lower):
        red_flags.append({
            "name": "Front-Loaded Payment",
            "severity": "critical",
            "clause_text": "50% deposit required before work begins...",
            "explanation": "Paying half or more upfront gives the contractor little incentive to finish. If they disappear, you've lost thousands with nothing to show for it. Industry standard is 10-33% deposit.",
            "what_to_ask": "Negotiate to 10-20% deposit, with remaining payments tied to completed milestones. Never pay more than 33% upfront."
        })
        risk_score += 20

    # Check for mandatory arbitration
    if 'arbitration' in text_lower:
        red_flags.append({
            "name": "Mandatory Arbitration",
            "severity": "warning",
            "clause_text": "Any disputes shall be resolved through binding arbitration...",
            "explanation": "You lose your right to sue in court if the contractor does shoddy work. Arbitration costs can be high and typically favors the business.",
            "what_to_ask": "Strike this clause or add an exception for claims under $25,000 (small claims court)."
        })
        risk_score += 10

    # Check for missing completion date
    if 'completion' not in text_lower and 'deadline' not in text_lower and 'finish date' not in text_lower:
        red_flags.append({
            "name": "Missing Completion Date",
            "severity": "warning",
            "clause_text": "(No completion date found in contract)",
            "explanation": "Without a completion date, the contractor can drag the project out indefinitely. 'We'll get to it' can turn into months of delays with no recourse.",
            "what_to_ask": "Insist on a specific completion date with per-day penalties for delays (e.g., $100/day after deadline). Include exceptions only for weather and permit delays."
        })
        missing_protections.append("Specific completion date with delay penalties")
        risk_score += 15

    # Check for no warranty
    if 'warranty' not in text_lower and 'guarantee' not in text_lower:
        red_flags.append({
            "name": "No Warranty",
            "severity": "critical",
            "clause_text": "(No warranty or guarantee language found in contract)",
            "explanation": "Without a written warranty, you have no recourse if the work fails in 6 months. A leaking roof, cracking foundation, or failing HVAC with no warranty means you pay for repairs out of pocket.",
            "what_to_ask": "Demand a minimum 1-year workmanship warranty and ensure manufacturer warranties on materials are passed through to you in writing."
        })
        missing_protections.append("Written workmanship warranty (minimum 1 year)")
        risk_score += 20

    # Check for missing lien waiver
    if 'lien' not in text_lower or 'lien waiver' not in text_lower:
        red_flags.append({
            "name": "Missing Lien Waiver",
            "severity": "critical",
            "clause_text": "(No lien waiver provision found in contract)",
            "explanation": "Without lien waivers, subcontractors and suppliers can put a lien on YOUR HOME if the contractor doesn't pay them - even after you've paid the contractor in full. You could end up paying twice.",
            "what_to_ask": "Require the contractor to provide lien waivers from all subcontractors and suppliers with each payment. Make final payment contingent on receiving all final lien waivers."
        })
        missing_protections.append("Lien waiver requirements with each payment")
        risk_score += 15
    else:
        has_lien_waiver = True

    # Check for no change order process
    if 'change order' not in text_lower:
        red_flags.append({
            "name": "No Change Order Process",
            "severity": "warning",
            "clause_text": "(No change order process found in contract)",
            "explanation": "Without a formal change order process, the contractor can make changes and bill you for extras with no documentation. 'While we were in there...' can add thousands to your bill.",
            "what_to_ask": "Add a clause requiring all changes to be documented in writing with costs BEFORE work begins. No verbal change orders."
        })
        missing_protections.append("Written change order process with pre-approval")
        risk_score += 10
    else:
        has_change_order_process = True

    # Check for missing license/insurance proof
    if 'license' not in text_lower and 'insur' not in text_lower:
        red_flags.append({
            "name": "Missing License/Insurance Proof",
            "severity": "warning",
            "clause_text": "(No reference to contractor license or insurance in contract)",
            "explanation": "A contractor without proper licensing and insurance puts you at risk. If a worker is injured on your property and the contractor has no workers' comp, YOU could be liable.",
            "what_to_ask": "Demand copies of contractor license, general liability insurance, and workers' compensation insurance. Verify them independently with the issuing agencies."
        })
        missing_protections.append("Proof of contractor license, GL insurance, and workers' comp")
        risk_score += 10

    # Always add boilerplate
    red_flags.append({
        "name": "Standard Workmanship Warranty",
        "severity": "boilerplate",
        "clause_text": None,
        "explanation": "The contract includes a standard workmanship warranty covering defects in labor. This is expected in any reputable home improvement contract.",
        "what_to_ask": "No action needed - this is standard. Just note the warranty duration and what it covers."
    })
    red_flags.append({
        "name": "Permit Responsibilities",
        "severity": "boilerplate",
        "clause_text": None,
        "explanation": "The contract specifies who is responsible for pulling building permits. This is standard and important for code compliance.",
        "what_to_ask": "No action needed - just verify the contractor (not you) is responsible for obtaining all required permits."
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

    # Generate summary
    critical_count = len([r for r in red_flags if r['severity'] == 'critical'])
    warning_count = len([r for r in red_flags if r['severity'] == 'warning'])

    if critical_count > 0:
        summary = f"This home improvement contract has {critical_count} critical issue(s) that put your money and your home at risk. "
    else:
        summary = "This contract covers some basics but could use improvement. "

    if missing_protections:
        summary += f"It's missing {len(missing_protections)} important protections that every homeowner should insist on."

    # Generate protection checklist
    protection_checklist = """HOME IMPROVEMENT CONTRACT PROTECTION CHECKLIST:

BEFORE SIGNING:
[ ] Verify contractor license number with your state licensing board
[ ] Verify general liability insurance (minimum $1M per occurrence)
[ ] Verify workers' compensation insurance
[ ] Check BBB, Google reviews, and state complaint records
[ ] Get at least 3 written bids for comparison
[ ] Ask for references from recent similar projects

CONTRACT MUST INCLUDE:
[ ] Detailed scope of work (specific materials, brands, quantities)
[ ] Fixed price or not-to-exceed amount
[ ] Payment schedule tied to milestones (NOT front-loaded)
[ ] Start date AND completion date
[ ] Per-day penalty for delays
[ ] Written change order process
[ ] Workmanship warranty (minimum 1 year)
[ ] Material warranties passed through to you
[ ] Lien waiver requirements with each payment
[ ] Permit responsibility (contractor should pull permits)
[ ] Cleanup and debris removal included

DURING THE PROJECT:
[ ] Get lien waivers with every progress payment
[ ] Document everything with photos/video
[ ] Don't make final payment until punch list is complete
[ ] Get all change orders in writing BEFORE work starts
[ ] Verify permits are posted on site

AFTER COMPLETION:
[ ] Final inspection by building department
[ ] Collect all final lien waivers
[ ] Get warranty documentation in writing
[ ] Keep all records for at least 7 years"""

    return {
        "overall_risk": overall_risk,
        "risk_score": risk_score,
        "contractor_name": None,
        "project_type": project_type,
        "payment_structure": None,
        "has_lien_waiver": has_lien_waiver,
        "has_change_order_process": has_change_order_process,
        "red_flags": red_flags,
        "missing_protections": missing_protections,
        "summary": summary,
        "protection_checklist": protection_checklist
    }
