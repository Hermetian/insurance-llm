# Claudepad - Session Memory

## Session Summaries

### 2026-02-01 - Added Donation Link Infrastructure
Set up donation link with easy configuration:

**Files Created:**
- `frontend/src/config/stripe.ts` - Config with `STRIPE_DONATION_LINK` and `DONATION_ENABLED` toggle
- `MONETIZATION_SETUP.md` - Step-by-step guide for Stripe + affiliate setup

**Changes Made:**
- Footer now has donation link (hidden until enabled) and GitHub link
- Added `footer-links` and `github-link` CSS styles
- Donation link only shows when `DONATION_ENABLED = true`

**To Enable Donations:**
1. Create Stripe Payment Link at dashboard.stripe.com/payment-links
2. Edit `frontend/src/config/stripe.ts`
3. Replace `YOUR_LINK_HERE` with your link
4. Set `DONATION_ENABLED = true`
5. Rebuild and deploy

---

### 2026-02-01 - Simplified to Free + Optional Auth for History
Removed premium/paywall features. App is now completely free with optional sign-in.

**Changes Made:**
- Removed `handleUnlockReport` function and all premium unlock logic
- Removed `userCredits` state and credit-related setters
- Removed premium metadata blocks from all 8 analyze functions
- Removed premium state reset from `resetAll()`
- Kept: auth system for history saving, affiliate offers during loading, donation link

**Current Flow:**
1. Users upload documents (no auth required)
2. See affiliate offers during analysis loading
3. Get full analysis results (no paywall)
4. Optional: Sign in to save analysis history

---

### 2026-02-01 - Monetization + Auth Implementation (Initial)
Implemented full monetization system with authentication:

**Backend Changes:**
- Added User, AuthSession, PremiumUnlock database models
- Added auth endpoints: `/api/auth/signup`, `/api/auth/login`, `/api/auth/logout`, `/api/auth/me`
- Added `/api/user/history` endpoint for viewing past analyses
- Added Stripe endpoints (not currently used): `/api/create-checkout-session`, `/api/stripe-webhook`
- Modified analyze endpoints to track `user_id` on uploads
- Added bcrypt and stripe to requirements.txt

**Frontend Changes:**
- Created `src/config/affiliates.ts` with affiliate offers mapped by document type
- Added auth state management (login/signup/logout flow)
- Added history modal to view past analyses
- Added loading overlay with contextual affiliate offers during analysis
- Added auth modal for login/signup
- Added CSS styles for all new components

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
