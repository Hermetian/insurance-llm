# INSURANCE.EXE

> *messy docs → clean data* | pixel perfect coverage analysis

A retro-styled AI-powered insurance document intelligence tool. Feed it messy COIs, quotes, policy summaries, and email forwards — get structured data and polished client proposals in minutes.

Built for the forward-deployed AI engineers at [Fulcrum Tech](https://withfulcrum.com).

![Williamsburg 2015 vibes](https://img.shields.io/badge/aesthetic-williamsburg%202015-ff6b6b?style=flat-square)
![Python](https://img.shields.io/badge/python-3.11+-4ecdc4?style=flat-square)
![TypeScript](https://img.shields.io/badge/typescript-5.0+-4ecdc4?style=flat-square)

## What It Does

1. **Paste messy insurance documents** - COIs, quotes, policy renewals, forwarded emails
2. **AI extracts structured data** - policy info, coverages, limits, exclusions, compliance issues
3. **Generate polished proposals** - client-ready summaries in plain English
4. **Risk scoring** - automated coverage adequacy assessment

## The Stack

- **Frontend**: React + TypeScript + Vite
- **Backend**: Python + FastAPI
- **AI**: Claude (Anthropic API)
- **Aesthetic**: Williamsburg 2015 pixel art (Press Start 2P, VT323, CRT scanlines)

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Set your Anthropic API key
export ANTHROPIC_API_KEY=your_key_here

# Run the server
python main.py
```

Backend runs at `http://localhost:8080`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/extract` | POST | Extract structured data from document text |
| `/api/compare` | POST | Compare multiple insurance quotes |
| `/api/generate-proposal` | POST | Generate client-ready proposal from extracted data |

## Sample Documents

The app includes three sample documents to demo:

1. **Messy COI Email** - Forwarded certificate with casual notes
2. **Scanned Quote PDF (OCR)** - Commercial property quote with formatting artifacts
3. **Policy Renewal Notice** - Coverage changes and exclusions

## Why This Exists

Insurance brokers spend hours manually extracting data from messy documents. This tool demonstrates how AI can:

- Parse unstructured insurance documents
- Extract coverage details, limits, and exclusions
- Flag compliance issues automatically
- Generate professional client communications

*"We went from waiting days for mediocre outsourced work to standout proposals in minutes."*

## License

MIT
