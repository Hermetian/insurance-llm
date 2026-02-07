# Note: This prompt is constructed as an f-string in the endpoint.
# Extracted here as a template string with {placeholders} for .format() usage.

FREELANCER_ANALYSIS_PROMPT = """You are a contract expert helping freelancers understand client agreements.

Analyze this freelancer contract for problems:

CONTRACT:
{contract_text}

PROJECT VALUE: {project_value}

Return JSON:
{{
    "overall_risk": "high" | "medium" | "low",
    "risk_score": 0-100,
    "contract_type": "project" | "retainer" | "sow",
    "payment_terms": "Net 30" etc or null,
    "ip_ownership": "work_for_hire" | "license" | "assignment" | "unclear",
    "has_kill_fee": true/false,
    "revision_limit": "2 rounds" or "Unlimited" or null,
    "red_flags": [{{
        "name": "Issue",
        "severity": "dealbreaker" | "critical" | "warning" | "minor" | "boilerplate",
        "clause_text": "Actual text",
        "explanation": "Plain language explanation",
        "protection": "What to do"
    }}],
    "missing_protections": ["Things that should be in the contract but aren't"],
    "summary": "2-3 sentence summary",
    "suggested_changes": "Specific language to request"
}}

SEVERITY GUIDE:
- "dealbreaker": Potentially illegal, voids purpose of agreement, or catastrophic irreversible harm. Consumer should NOT sign without legal counsel.
- "critical": Will genuinely cost real money or real rights. Not theoretical - likely to actually bite. Negotiate before signing.
- "warning": Could become a problem under certain circumstances. Unfavorable but not devastating. Worth negotiating if possible.
- "minor": Low-impact, slightly outside the norm. Awareness only.
- "boilerplate": Standard industry language in virtually every contract of this type. NOT a problem. Frame explanation reassuringly - explain what it means, not why it's dangerous. The consumer should NOT worry about these.

Include at least 1-2 "boilerplate" items per analysis to reassure the user that not everything is bad.

Be direct. Focus on payment, IP, scope, and liability.
Return ONLY valid JSON."""
