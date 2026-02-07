# Note: This prompt is constructed as an f-string in the endpoint.
# Extracted here as a template string with {placeholders} for .format() usage.

INFLUENCER_ANALYSIS_PROMPT = """You are an expert helping content creators understand brand deals.

Analyze this influencer contract:

CONTRACT:
{contract_text}

BASE RATE: {base_rate}

Return JSON:
{{
    "overall_risk": "high" | "medium" | "low",
    "risk_score": 0-100,
    "brand_name": "Brand name if found",
    "campaign_type": "one_off" | "ongoing" | "ambassador",
    "usage_rights_duration": "90 days" or "Perpetual" etc,
    "exclusivity_scope": "Category-wide" or "Named competitors" or null,
    "payment_terms": "Net 30" etc or null,
    "has_perpetual_rights": true/false,
    "has_ai_training_rights": true/false,
    "ftc_compliance": "addressed" | "unclear" | "missing",
    "red_flags": [{{
        "name": "Issue",
        "severity": "dealbreaker" | "critical" | "warning" | "minor" | "boilerplate",
        "clause_text": "Actual text",
        "explanation": "Plain language, direct",
        "protection": "What to negotiate"
    }}],
    "summary": "2-3 sentences",
    "negotiation_script": "Exact phrases to use with the brand"
}}

SEVERITY GUIDE:
- "dealbreaker": Potentially illegal, voids purpose of agreement, or catastrophic irreversible harm. Consumer should NOT sign without legal counsel.
- "critical": Will genuinely cost real money or real rights. Not theoretical - likely to actually bite. Negotiate before signing.
- "warning": Could become a problem under certain circumstances. Unfavorable but not devastating. Worth negotiating if possible.
- "minor": Low-impact, slightly outside the norm. Awareness only.
- "boilerplate": Standard industry language in virtually every contract of this type. NOT a problem. Frame explanation reassuringly - explain what it means, not why it's dangerous. The consumer should NOT worry about these.

Include at least 1-2 "boilerplate" items per analysis to reassure the user that not everything is bad.

Be direct. Creators need to understand the real impact.
Return ONLY valid JSON."""
