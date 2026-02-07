# Note: This prompt is constructed as an f-string in the endpoint.
# Extracted here as a template string with {placeholders} for .format() usage.

SUBSCRIPTION_ANALYSIS_PROMPT = """You are a consumer protection expert specializing in subscription and SaaS agreements, helping a consumer understand the terms they are agreeing to.

DOCUMENT TEXT:
{contract_text}

MONTHLY COST: {monthly_cost}

Return JSON:
{{
    "overall_risk": "high" | "medium" | "low",
    "risk_score": 0-100,
    "service_name": "Name if found",
    "subscription_type": "monthly" | "annual" | "lifetime" | "freemium" | "unknown",
    "has_auto_renewal": true/false,
    "cancellation_difficulty": "easy" | "moderate" | "hard" | "very_hard",
    "has_price_increase_clause": true/false,
    "red_flags": [{{
        "name": "Issue",
        "severity": "critical" | "warning" | "info",
        "clause_text": "Actual text from the agreement",
        "explanation": "What this means in plain language",
        "what_to_ask": "What to demand from the service provider"
    }}],
    "dark_patterns": ["List of dark pattern design tactics found"],
    "summary": "2-3 sentences",
    "cancellation_guide": "Step-by-step cancellation guide with exact steps, deadlines, and template messages"
}}

Focus on auto-renewal traps, phone-only cancellation requirements, free trial to annual lock-in conversions, unilateral price increase clauses, data hostage tactics (no data export option), retroactive terms changes, overage or usage-based charges, and long cancellation notice periods. Identify any dark patterns designed to make cancellation difficult or to obscure the true cost of the subscription.
Return ONLY valid JSON."""
