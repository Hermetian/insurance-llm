from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Insurance LLM", description="Pixel-powered insurance document intelligence")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic()

class DocumentInput(BaseModel):
    text: str
    doc_type: Optional[str] = "auto"

class Coverage(BaseModel):
    type: str
    limit: str
    deductible: Optional[str] = None
    notes: Optional[str] = None

class ExtractedPolicy(BaseModel):
    insured_name: Optional[str] = None
    policy_number: Optional[str] = None
    carrier: Optional[str] = None
    effective_date: Optional[str] = None
    expiration_date: Optional[str] = None
    coverages: list[Coverage] = []
    total_premium: Optional[str] = None
    exclusions: list[str] = []
    special_conditions: list[str] = []
    risk_score: Optional[int] = None
    compliance_issues: list[str] = []
    summary: Optional[str] = None

EXTRACTION_PROMPT = """You are an expert insurance document analyst. Extract structured data from this insurance document.

Return a JSON object with these fields:
- insured_name: Name of the insured party
- policy_number: Policy number if present
- carrier: Insurance carrier/company name
- effective_date: Policy start date (format: YYYY-MM-DD if possible)
- expiration_date: Policy end date (format: YYYY-MM-DD if possible)
- coverages: Array of objects with {type, limit, deductible, notes}
- total_premium: Total premium amount
- exclusions: Array of exclusion strings
- special_conditions: Array of special conditions or endorsements
- risk_score: 1-100 score based on coverage adequacy (100 = excellent)
- compliance_issues: Array of potential compliance concerns
- summary: 2-3 sentence summary of the policy

Be thorough but only include information actually present in the document.
If a field isn't present, use null.

Document text:
{document_text}

Return ONLY valid JSON, no markdown formatting."""

@app.get("/")
def read_root():
    return {"status": "online", "message": "Insurance LLM API - Pixel Perfect Coverage Analysis"}

@app.post("/api/extract", response_model=ExtractedPolicy)
async def extract_document(doc: DocumentInput):
    """Extract structured data from insurance document text"""
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": EXTRACTION_PROMPT.format(document_text=doc.text)
                }
            ]
        )

        response_text = message.content[0].text

        # Parse the JSON response
        import json
        # Clean up potential markdown formatting
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        response_text = response_text.strip()

        extracted = json.loads(response_text)
        return ExtractedPolicy(**extracted)

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse LLM response: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/compare")
async def compare_quotes(quotes: list[DocumentInput]):
    """Compare multiple insurance quotes"""
    if len(quotes) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 quotes to compare")

    # Extract each quote
    extracted_quotes = []
    for quote in quotes:
        extracted = await extract_document(quote)
        extracted_quotes.append(extracted)

    # Generate comparison
    comparison_prompt = f"""Compare these {len(extracted_quotes)} insurance quotes and provide a recommendation.

Quotes:
{[q.model_dump() for q in extracted_quotes]}

Provide a JSON response with:
- recommendation: Which quote is best and why (string)
- comparison_table: Array of objects comparing key metrics
- pros_cons: Object with quote index as key, containing pros and cons arrays
- cost_analysis: Premium comparison and value assessment
- risk_assessment: Which provides better risk coverage

Return ONLY valid JSON."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": comparison_prompt}]
        )

        import json
        response_text = message.content[0].text
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]

        return json.loads(response_text.strip())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-proposal")
async def generate_proposal(extracted: ExtractedPolicy):
    """Generate a polished client-ready proposal from extracted data"""

    proposal_prompt = f"""Create a professional insurance proposal summary for a client based on this extracted policy data:

{extracted.model_dump()}

Write a clear, client-friendly proposal that:
1. Summarizes key coverages in plain English
2. Highlights important dates and deadlines
3. Notes any gaps or concerns
4. Provides actionable recommendations

Format as markdown with clear sections. Keep it concise but comprehensive."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[{"role": "user", "content": proposal_prompt}]
        )

        return {"proposal": message.content[0].text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
