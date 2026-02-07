def mock_subscription_analysis(contract_text: str, monthly_cost: int = None) -> dict:
    """Generate mock subscription/terms of service analysis"""
    text_lower = contract_text.lower()

    red_flags = []
    dark_patterns = []
    risk_score = 20

    # Detect subscription type
    if 'saas' in text_lower or 'software' in text_lower or 'platform' in text_lower:
        subscription_type = "saas"
    elif 'stream' in text_lower or 'entertainment' in text_lower or 'content' in text_lower:
        subscription_type = "streaming"
    elif 'gym' in text_lower or 'fitness' in text_lower or 'membership' in text_lower:
        subscription_type = "membership"
    elif 'box' in text_lower or 'delivery' in text_lower or 'subscription box' in text_lower:
        subscription_type = "subscription_box"
    elif 'cloud' in text_lower or 'storage' in text_lower or 'hosting' in text_lower:
        subscription_type = "cloud_service"
    else:
        subscription_type = "general"

    has_auto_renewal = False
    has_price_increase_clause = False
    cancellation_difficulty = "easy"
    difficulty_score = 0

    # Check for auto-renewal trap
    if 'auto-renew' in text_lower or 'automatically renew' in text_lower or 'auto renewal' in text_lower:
        has_auto_renewal = True
        red_flags.append({
            "name": "Auto-Renewal Trap",
            "severity": "warning",
            "clause_text": "Your subscription will automatically renew at the then-current price...",
            "explanation": "Your subscription keeps charging you unless you actively cancel. Many services make this hard to find and even harder to turn off.",
            "what_to_ask": "Set a calendar reminder before renewal date. Check if you can disable auto-renewal in account settings. Many states now require clear disclosure and easy cancellation."
        })
        dark_patterns.append("Auto-renewal buried in terms")
        risk_score += 10
        difficulty_score += 1

    # Check for phone-only cancellation
    if ('phone' in text_lower and 'cancel' in text_lower) or 'call to cancel' in text_lower:
        red_flags.append({
            "name": "Phone-Only Cancellation",
            "severity": "critical",
            "clause_text": "To cancel your subscription, you must call our customer service line...",
            "explanation": "Forcing you to call to cancel is a classic retention tactic. They'll put you on hold, transfer you, and hit you with save offers. The FTC's 'click-to-cancel' rule requires cancellation to be as easy as sign-up.",
            "what_to_ask": "Check if the FTC click-to-cancel rule applies (effective 2025). File a complaint at ftc.gov if they make cancellation unreasonably difficult."
        })
        dark_patterns.append("Phone-only cancellation (retention gauntlet)")
        risk_score += 20
        difficulty_score += 3

    # Check for free trial to annual lock-in
    if 'free trial' in text_lower and ('annual' in text_lower or 'yearly' in text_lower):
        red_flags.append({
            "name": "Free Trial to Annual Lock-in",
            "severity": "critical",
            "clause_text": "After your free trial, you will be automatically enrolled in an annual subscription...",
            "explanation": "The free trial converts to a YEARLY commitment, not monthly. Miss the cancellation window and you're locked in for a full year. This is intentionally deceptive.",
            "what_to_ask": "Cancel before the trial ends if you're not sure. Set a reminder for 1 day before trial expiration. Check if you can switch to monthly billing."
        })
        dark_patterns.append("Free trial auto-converts to annual commitment")
        risk_score += 20
        difficulty_score += 2

    # Check for unilateral price increases
    if 'price' in text_lower and ('increase' in text_lower or 'change' in text_lower) and ('any time' in text_lower or 'unilateral' in text_lower):
        has_price_increase_clause = True
        red_flags.append({
            "name": "Unilateral Price Increases",
            "severity": "warning",
            "clause_text": "We reserve the right to change pricing at any time...",
            "explanation": "They can raise your price whenever they want. Combined with auto-renewal, you might not notice until you see a higher charge on your card.",
            "what_to_ask": "Look for a clause requiring advance notice of price changes. Many states require 30-day notice. If no notice required, monitor your statements closely."
        })
        dark_patterns.append("Price increases without meaningful consent")
        risk_score += 15

    # Check for data hostage
    if 'export' not in text_lower and 'download your data' not in text_lower:
        red_flags.append({
            "name": "Data Hostage",
            "severity": "warning",
            "clause_text": "(No data export or download provision found in terms)",
            "explanation": "There's no mention of being able to export or download your data. If you cancel, you could lose years of content, files, or history. They're holding your data hostage to keep you subscribed.",
            "what_to_ask": "Before committing, verify you can export your data. Check if there's an API or export tool. Regularly back up anything important."
        })
        dark_patterns.append("No data portability - lock-in through data hostage")
        risk_score += 10
        difficulty_score += 1

    # Check for retroactive terms changes
    if 'modify' in text_lower and 'terms' in text_lower and ('any time' in text_lower or 'retroactive' in text_lower):
        red_flags.append({
            "name": "Retroactive Terms Changes",
            "severity": "warning",
            "clause_text": "We may modify these terms at any time. Continued use constitutes acceptance...",
            "explanation": "They can change the rules whenever they want, and just using the service means you 'agreed.' They could add fees, remove features, or change your rights with no real consent.",
            "what_to_ask": "Look for a requirement to notify you of changes (email, not just posting on their website). Check if material changes give you a right to cancel without penalty."
        })
        dark_patterns.append("Retroactive terms changes with passive acceptance")
        risk_score += 10

    # Check for overage charges
    if 'overage' in text_lower or 'excess usage' in text_lower:
        red_flags.append({
            "name": "Overage Charges",
            "severity": "info",
            "clause_text": "Usage exceeding plan limits will be billed at the overage rate...",
            "explanation": "If you go over your plan limits, you get charged extra - sometimes at very high rates. This is common with cloud services, APIs, and data plans.",
            "what_to_ask": "Ask about overage rates and whether you can set usage alerts or hard caps. Some services will let you set a spending limit."
        })
        risk_score += 5

    # Check for long cancellation notice period
    if 'notice' in text_lower and ('30 day' in text_lower or '60 day' in text_lower or '90 day' in text_lower) and 'cancel' in text_lower:
        if '90 day' in text_lower:
            notice_period = "90-day"
            risk_add = 10
        elif '60 day' in text_lower:
            notice_period = "60-day"
            risk_add = 10
        else:
            notice_period = "30-day"
            risk_add = 10

        red_flags.append({
            "name": "Long Cancellation Notice Period",
            "severity": "warning",
            "clause_text": f"Cancellation requires {notice_period} written notice before renewal date...",
            "explanation": f"You must give {notice_period} notice to cancel. Miss the window and you're auto-renewed for another term. This is designed to make you forget and keep paying.",
            "what_to_ask": f"Set a calendar reminder {notice_period} before your renewal date. Send cancellation via email AND certified mail to create a paper trail."
        })
        dark_patterns.append(f"{notice_period} cancellation notice window")
        risk_score += risk_add
        difficulty_score += 2

    # Calculate cancellation difficulty
    if difficulty_score >= 5:
        cancellation_difficulty = "very_hard"
    elif difficulty_score >= 3:
        cancellation_difficulty = "hard"
    elif difficulty_score >= 1:
        cancellation_difficulty = "moderate"
    else:
        cancellation_difficulty = "easy"

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
        summary = f"This subscription has {critical_count} critical issue(s) designed to keep you paying. "
    else:
        summary = "This subscription has some common gotchas you should be aware of. "

    if cancellation_difficulty in ('hard', 'very_hard'):
        summary += f"Cancellation difficulty is rated '{cancellation_difficulty}' - they've made it intentionally difficult to leave. "
    if dark_patterns:
        summary += f"We found {len(dark_patterns)} dark pattern(s) designed to trap you."

    # Generate cancellation guide
    cancellation_guide = f"""STEP-BY-STEP CANCELLATION GUIDE:

BEFORE YOU CANCEL:
1. Export/download ALL your data (files, history, contacts, etc.)
2. Screenshot your account settings and billing history
3. Check your renewal date and any notice requirements
4. Look for a cancellation link in Account Settings > Subscription/Billing
5. Document everything

TO CANCEL:
"""
    if cancellation_difficulty in ('hard', 'very_hard'):
        cancellation_guide += """6. Try online cancellation first (Account > Settings > Cancel)
7. If forced to call: Note the date, time, and representative's name
8. State clearly: "I want to cancel my subscription effective immediately"
9. Do NOT accept retention offers or 'pause' options unless you truly want them
10. Ask for a cancellation confirmation number
11. Follow up with written confirmation via email

IF THEY MAKE IT DIFFICULT:
12. Send cancellation via certified mail to their registered business address
13. Contact your credit card company to dispute future charges
14. File a complaint with the FTC at ftc.gov/complaint
15. File a complaint with your state Attorney General
16. Leave a detailed review about the cancellation experience
"""
    else:
        cancellation_guide += """6. Navigate to Account > Settings > Subscription
7. Click 'Cancel Subscription' or 'End Membership'
8. Complete any cancellation survey (optional)
9. Screenshot the cancellation confirmation
10. Verify you receive a confirmation email
"""

    cancellation_guide += f"""
AFTER CANCELLATION:
- Monitor your bank/credit card for unauthorized charges
- If charged after cancellation, dispute with your card issuer
- Keep cancellation confirmation for at least 1 year
- Check that your data is actually deleted (if desired) per their privacy policy

CANCELLATION DIFFICULTY RATING: {cancellation_difficulty.upper().replace('_', ' ')}"""

    return {
        "overall_risk": overall_risk,
        "risk_score": risk_score,
        "service_name": None,
        "subscription_type": subscription_type,
        "has_auto_renewal": has_auto_renewal,
        "cancellation_difficulty": cancellation_difficulty,
        "has_price_increase_clause": has_price_increase_clause,
        "red_flags": red_flags,
        "dark_patterns": dark_patterns,
        "summary": summary,
        "cancellation_guide": cancellation_guide
    }
