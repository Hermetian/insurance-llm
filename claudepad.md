# Claudepad - Session Memory

## Session Summaries

### 2026-02-01 - Monetization + Auth Implementation
Implemented full monetization system with authentication:

**Backend Changes:**
- Added User, AuthSession, PremiumUnlock database models
- Added auth endpoints: `/api/auth/signup`, `/api/auth/login`, `/api/auth/logout`, `/api/auth/me`
- Added Stripe endpoints: `/api/create-checkout-session`, `/api/stripe-webhook`, `/api/unlock-report`, `/api/check-unlock/{hash}`
- Modified all analyze endpoints to include `document_hash`, `is_premium`, and `total_issues` fields
- Added bcrypt and stripe to requirements.txt

**Frontend Changes:**
- Created `src/config/affiliates.ts` with affiliate offers mapped by document type
- Added auth state management (login/signup/logout flow)
- Added auth header to header with user email, credits badge, login/signup/logout buttons
- Added loading overlay with contextual affiliate offers during analysis
- Added auth modal for login/signup
- Added premium upsell banner that appears after analysis
- Added CSS styles for all new components

**Monetization Flow:**
1. Free users see affiliate offers during loading
2. Free users get summary (risk score + top 3 issues) after analysis
3. Premium upsell banner prompts for $3 unlock or sign up
4. Authenticated users can purchase credits via Stripe
5. Credits persist to account for future unlocks

---

## Key Findings

### API Structure
- All analyze endpoints return reports with `document_hash`, `is_premium`, and `total_issues`
- Auth uses Bearer token in Authorization header
- Session token stored in localStorage

### Document Types Supported
- COI (Certificate of Insurance)
- Lease
- Gym contracts
- Employment contracts
- Freelancer contracts
- Influencer contracts
- Timeshare contracts
- Insurance policies

### Environment Variables Needed
```
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
DATABASE_URL=postgresql://...
```

### Affiliate Partners (Placeholder URLs)
- Insurance: Policygenius, The Zebra, Ethos
- Legal: LegalZoom, Rocket Lawyer
- Rental: Zillow, Apartments.com
- Fitness: ClassPass, Peloton
- Freelance: Bonsai
- Creator: Klear

URLs need to be updated with actual affiliate tracking links once signed up with partners.
