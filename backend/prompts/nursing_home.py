# Note: This prompt is constructed as an f-string in the endpoint.
# Extracted here as a template string with {placeholders} for .format() usage.

NURSING_HOME_ANALYSIS_PROMPT = """You are an elder law and nursing home rights expert helping a patient or their family understand a nursing home admission agreement.

DOCUMENT TEXT:
{contract_text}

STATE: {state}

Return JSON:
{{
    "overall_risk": "high" | "medium" | "low",
    "risk_score": 0-100,
    "facility_name": "Name if found",
    "agreement_type": "admission" | "financial" | "combined" | "unknown",
    "has_responsible_party_clause": true/false,
    "has_forced_arbitration": true/false,
    "has_liability_waiver": true/false,
    "red_flags": [{{
        "name": "Issue",
        "severity": "critical" | "warning" | "info",
        "clause_text": "Actual text from the agreement",
        "explanation": "What this means in plain language",
        "what_to_ask": "What to demand from the facility"
    }}],
    "illegal_clauses": ["List of clauses that violate federal or state law"],
    "summary": "2-3 sentences",
    "rights_guide": "Patient/family rights guide with what to demand and who to contact"
}}

Focus on responsible party or guarantor clauses (ILLEGAL under the federal Nursing Home Reform Act, 42 USC 1396r - facilities cannot require a third party to guarantee payment as a condition of admission), forced arbitration agreements, broad liability waivers, discharge or transfer threats, waiver of the 30-day discharge notice requirement, blanket medical consent clauses, personal property disclaimers, and missing grievance processes. Apply {state}-specific nursing home regulations in addition to federal protections.
Return ONLY valid JSON."""
