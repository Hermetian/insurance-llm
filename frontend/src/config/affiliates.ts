// Affiliate offers configuration
// These are contextual offers shown during document analysis loading

export interface AffiliateOffer {
  id: string
  name: string
  tagline: string
  description: string
  cta: string
  url: string
  logo?: string
  category: string
}

// Map document types to relevant affiliate offers
export const affiliateOffers: Record<string, AffiliateOffer[]> = {
  // Insurance-related documents (COI, insurance_policy)
  insurance: [
    {
      id: 'policygenius',
      name: 'Policygenius',
      tagline: 'Compare insurance quotes in minutes',
      description: 'See if you could save on your insurance. Compare quotes from top carriers.',
      cta: 'Get Free Quotes',
      url: 'https://policygenius.com/?ref=cantheyfuckme',
      category: 'insurance'
    },
    {
      id: 'thezebra',
      name: 'The Zebra',
      tagline: 'Compare car insurance in 5 minutes',
      description: 'The Zebra compares 100+ insurance companies to find you the best rate.',
      cta: 'Compare Rates',
      url: 'https://thezebra.com/?ref=cantheyfuckme',
      category: 'insurance'
    },
    {
      id: 'ethos',
      name: 'Ethos Life',
      tagline: 'Life insurance without the hassle',
      description: 'Get covered in 10 minutes. No medical exams required for most applicants.',
      cta: 'Get a Quote',
      url: 'https://ethos.com/?ref=cantheyfuckme',
      category: 'insurance'
    }
  ],

  // Lease documents
  lease: [
    {
      id: 'zillow',
      name: 'Zillow',
      tagline: 'Find your next place',
      description: 'Looking for a better deal? Browse apartments and rentals in your area.',
      cta: 'Browse Rentals',
      url: 'https://zillow.com/rentals/?ref=cantheyfuckme',
      category: 'rental'
    },
    {
      id: 'apartments',
      name: 'Apartments.com',
      tagline: 'Find the right apartment for you',
      description: 'Millions of apartments. One search. Find deals and move-in specials.',
      cta: 'Search Apartments',
      url: 'https://apartments.com/?ref=cantheyfuckme',
      category: 'rental'
    },
    {
      id: 'lemonade-renters',
      name: 'Lemonade Renters',
      tagline: 'Renters insurance from $5/mo',
      description: 'Get renters insurance in 90 seconds. Instant everything, powered by AI.',
      cta: 'Get Covered',
      url: 'https://lemonade.com/renters/?ref=cantheyfuckme',
      category: 'insurance'
    }
  ],

  // Gym contracts
  gym: [
    {
      id: 'classpass',
      name: 'ClassPass',
      tagline: 'One membership, unlimited options',
      description: 'Access gyms, fitness classes, and wellness experiences near you.',
      cta: 'Try ClassPass Free',
      url: 'https://classpass.com/?ref=cantheyfuckme',
      category: 'fitness'
    },
    {
      id: 'peloton',
      name: 'Peloton App',
      tagline: 'Workout anytime, anywhere',
      description: 'Thousands of classes. No equipment needed for most. Cancel anytime.',
      cta: 'Start Free Trial',
      url: 'https://onepeloton.com/app/?ref=cantheyfuckme',
      category: 'fitness'
    }
  ],

  // Employment contracts
  employment: [
    {
      id: 'legalzoom',
      name: 'LegalZoom',
      tagline: 'Legal help made simple',
      description: 'Need to understand your rights? Get affordable legal advice.',
      cta: 'Talk to a Lawyer',
      url: 'https://legalzoom.com/?ref=cantheyfuckme',
      category: 'legal'
    },
    {
      id: 'rocketlawyer',
      name: 'Rocket Lawyer',
      tagline: 'Legal made simple',
      description: 'Create legal documents, get attorney advice, and protect what matters.',
      cta: 'Get Legal Help',
      url: 'https://rocketlawyer.com/?ref=cantheyfuckme',
      category: 'legal'
    },
    {
      id: 'levels',
      name: 'levels.fyi',
      tagline: 'Know your worth',
      description: 'See what others in your role are making. Negotiate with confidence.',
      cta: 'Check Salaries',
      url: 'https://levels.fyi/?ref=cantheyfuckme',
      category: 'career'
    }
  ],

  // Freelancer contracts
  freelancer: [
    {
      id: 'bonsai',
      name: 'Bonsai',
      tagline: 'Freelance contracts made easy',
      description: 'Create bulletproof contracts, proposals, and invoices in minutes.',
      cta: 'Try Bonsai Free',
      url: 'https://hellobonsai.com/?ref=cantheyfuckme',
      category: 'freelance'
    },
    {
      id: 'rocketlawyer-freelance',
      name: 'Rocket Lawyer',
      tagline: 'Protect your freelance business',
      description: 'Get contract templates, legal advice, and business formation help.',
      cta: 'Get Started',
      url: 'https://rocketlawyer.com/freelance/?ref=cantheyfuckme',
      category: 'legal'
    }
  ],

  // Influencer contracts
  influencer: [
    {
      id: 'klear',
      name: 'Klear',
      tagline: 'Know your worth',
      description: 'Calculate your rates and find brand deals that pay what you deserve.',
      cta: 'Calculate My Rate',
      url: 'https://klear.com/?ref=cantheyfuckme',
      category: 'creator'
    },
    {
      id: 'bonsai-creator',
      name: 'Bonsai for Creators',
      tagline: 'Creator-friendly contracts',
      description: 'Contracts that protect your content and rights. Used by 500K+ creators.',
      cta: 'Get Free Templates',
      url: 'https://hellobonsai.com/creators/?ref=cantheyfuckme',
      category: 'creator'
    }
  ],

  // Timeshare contracts
  timeshare: [
    {
      id: 'timeshare-exit-team',
      name: 'Timeshare Exit',
      tagline: 'Get out of your timeshare',
      description: 'Stuck in a timeshare? Our experts help you exit legally and permanently.',
      cta: 'Get Free Consultation',
      url: 'https://timeshareexit.com/?ref=cantheyfuckme',
      category: 'timeshare'
    },
    {
      id: 'vrbo',
      name: 'VRBO',
      tagline: 'Vacation rentals without commitment',
      description: 'Skip the timeshare trap. Rent vacation homes when YOU want.',
      cta: 'Browse Rentals',
      url: 'https://vrbo.com/?ref=cantheyfuckme',
      category: 'travel'
    }
  ],

  // Default/fallback offers
  default: [
    {
      id: 'legalzoom-default',
      name: 'LegalZoom',
      tagline: 'Legal help made simple',
      description: 'Need legal advice? Get answers from attorneys at affordable prices.',
      cta: 'Talk to a Lawyer',
      url: 'https://legalzoom.com/?ref=cantheyfuckme',
      category: 'legal'
    },
    {
      id: 'nerdwallet',
      name: 'NerdWallet',
      tagline: 'Make smarter money moves',
      description: 'Compare financial products and get personalized recommendations.',
      cta: 'Explore Options',
      url: 'https://nerdwallet.com/?ref=cantheyfuckme',
      category: 'finance'
    }
  ]
}

// Get offers for a specific document type
export function getOffersForDocType(docType: string): AffiliateOffer[] {
  // Map document types to affiliate categories
  const typeMapping: Record<string, string> = {
    coi: 'insurance',
    insurance_policy: 'insurance',
    lease: 'lease',
    gym: 'gym',
    employment: 'employment',
    freelancer: 'freelancer',
    influencer: 'influencer',
    timeshare: 'timeshare'
  }

  const category = typeMapping[docType] || 'default'
  return affiliateOffers[category] || affiliateOffers.default
}

// Get a random offer for rotation
export function getRandomOffer(docType: string): AffiliateOffer {
  const offers = getOffersForDocType(docType)
  return offers[Math.floor(Math.random() * offers.length)]
}
