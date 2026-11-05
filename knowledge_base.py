# knowledge_base.py
# RAG Knowledge Base - Static policies, schemes, and digital onboarding data
# Retrieved and curated from MSME, PM SVANidhi, ONDC, and fintech portals

KNOWLEDGE_BASE = {
    "msme_schemes": [
        {
            "name": "PM SVANidhi (PM Street Vendor's AtmaNirbhar Nidhi)",
            "description": "Micro-credit scheme for street vendors affected by COVID-19. Provides working capital loans.",
            "loan_amount": "Rs. 10,000 (initial), Rs. 20,000 (2nd loan), Rs. 50,000 (3rd loan)",
            "eligibility": "Street vendors with valid vending certificate or identity card issued by ULB",
            "how_to_apply": "Apply via PM SVANidhi app, CSC centers, or scheduled commercial banks",
            "portal": "https://pmsvanidhi.mohua.gov.in",
            "benefit": "Collateral-free loans, digital transactions incentive up to Rs. 1200/year"
        },
        {
            "name": "MUDRA Yojana (Shishu Category)",
            "description": "Micro-loans for non-corporate, non-farm small/micro enterprises",
            "loan_amount": "Up to Rs. 50,000 (Shishu), Rs. 50,000–5 lakh (Kishore), Rs. 5–10 lakh (Tarun)",
            "eligibility": "Non-farm income generating activities including trading and services",
            "how_to_apply": "Apply at nearest bank, MFI, or via MUDRA app",
            "portal": "https://mudra.org.in",
            "benefit": "No collateral, low interest rates, business growth support"
        },
        {
            "name": "Udyam Registration (MSME Registration)",
            "description": "Free online MSME registration for micro enterprises",
            "eligibility": "Investment up to Rs. 1 crore and turnover up to Rs. 5 crore (micro)",
            "how_to_apply": "Self-register at udyamregistration.gov.in using Aadhaar",
            "portal": "https://udyamregistration.gov.in",
            "benefit": "Access to government schemes, bank credit, tax benefits, priority lending"
        },
        {
            "name": "ONDC (Open Network for Digital Commerce)",
            "description": "Government-backed open digital commerce network connecting buyers & sellers",
            "how_to_apply": "Register via ONDC network apps: Paytm, Meesho, PhonePe, Craftsvilla",
            "benefit": "Reach millions of online buyers without heavy platform fees"
        }
    ],
    "upi_setup_steps": {
        "bhim_upi": [
            "Download BHIM UPI app from Google Play Store / App Store",
            "Register with your mobile number linked to your bank account",
            "Set a 4-digit UPI PIN using your debit card details",
            "Generate your UPI ID (e.g., yourname@upi)",
            "Download and print your QR code from the app",
            "Display QR code prominently at your stall"
        ],
        "google_pay": [
            "Download Google Pay app",
            "Sign in with your Google account",
            "Add your bank account and verify",
            "Create your business profile in 'Business' section",
            "Get your business QR code and print it",
            "Share your UPI ID: yourname@oksbi or @okaxis"
        ],
        "phonepe_for_business": [
            "Download PhonePe for Business app",
            "Register with Aadhaar and PAN",
            "Link your bank account",
            "Create a merchant profile with your shop name",
            "Get your dedicated QR code",
            "Track all payments via the dashboard"
        ]
    },
    "digital_listing_platforms": [
        {
            "platform": "Google Business Profile",
            "category": "Local SEO",
            "cost": "Free",
            "steps": [
                "Go to business.google.com",
                "Click 'Manage Now' and sign in",
                "Enter your business name and category",
                "Add your location / area (e.g., Camp Area, Pune)",
                "Verify via postcard or phone",
                "Add photos, timings, and description"
            ],
            "benefit": "Appear in Google Maps and local search results"
        },
        {
            "platform": "JustDial",
            "category": "Local Directory",
            "cost": "Free basic listing",
            "steps": [
                "Visit justdial.com/free-listing",
                "Enter business name, category, city, area",
                "Add your mobile number",
                "Verify with OTP",
                "Upload photos and business description"
            ],
            "benefit": "Millions of daily local searches on JustDial"
        },
        {
            "platform": "Meesho",
            "category": "E-commerce (ONDC)",
            "cost": "0% commission on most categories",
            "steps": [
                "Download Meesho Supplier app",
                "Register with mobile and PAN/GST",
                "Add product listings with photos",
                "Set prices and packaging details",
                "Start receiving orders"
            ],
            "benefit": "Sell to customers across India, zero commission"
        },
        {
            "platform": "WhatsApp Business",
            "category": "Customer Engagement",
            "cost": "Free",
            "steps": [
                "Download WhatsApp Business app",
                "Set up business profile with name, address, category",
                "Create a product catalog with photos and prices",
                "Set automated greeting and away messages",
                "Share your catalog link with customers"
            ],
            "benefit": "Direct sales channel, customer support, order management"
        }
    ],
    "pricing_tips": {
        "fruits": "Price 5-10% below supermarket rates. Bundle deals (e.g., 1kg + 250g free) attract more buyers.",
        "vegetables": "Early morning fresh stock at premium, afternoon discounts to clear inventory. Seasonal pricing.",
        "street_food": "Combo meals increase avg order value. Rs. 10-20 items drive volume. Rs. 50-100 combos boost revenue.",
        "clothing": "Festival season (Diwali, Eid, Pongal) - premium pricing. Off-season - bundle discounts.",
        "general": "Offer loyalty discounts: 5th purchase free. Display price boards clearly. Accept digital payments for higher trust."
    },
    "local_languages": {
        "marathi": {"greeting": "नमस्कार", "buy": "खरेदी करा", "discount": "सवलत"},
        "hindi": {"greeting": "नमस्ते", "buy": "खरीदें", "discount": "छूट"},
        "tamil": {"greeting": "வணக்கம்", "buy": "வாங்கவும்", "discount": "தள்ளுபடி"},
        "telugu": {"greeting": "నమస్కారం", "buy": "కొనండి", "discount": "తగ్గింపు"},
        "kannada": {"greeting": "ನಮಸ್ಕಾರ", "buy": "ಖರೀದಿಸಿ", "discount": "ರಿಯಾಯಿತಿ"},
        "bengali": {"greeting": "নমস্কার", "buy": "কিনুন", "discount": "ছাড়"}
    },
    "cities_hotspots": {
        "pune": ["Camp Area", "FC Road", "MG Road", "Koregaon Park", "Kothrud", "Hadapsar"],
        "mumbai": ["Dharavi", "Dadar", "Andheri", "Bandra", "Colaba", "Kurla"],
        "delhi": ["Sarojini Nagar", "Chandni Chowk", "Lajpat Nagar", "Connaught Place"],
        "bangalore": ["Commercial Street", "Majestic", "Jayanagar", "Koramangala"],
        "chennai": ["T Nagar", "Pondy Bazaar", "George Town", "Mylapore"],
        "hyderabad": ["Laad Bazaar", "Begum Bazaar", "Abids", "Secunderabad"]
    },
    "qr_code_tips": [
        "Use free QR code generators: paytm.com/business, razorpay.com, or phonepe for business",
        "Laminate your QR code to protect from weather and wear",
        "Display at eye level, ensure good lighting for scanning",
        "Keep a backup screenshot of your QR on your phone",
        "Add your name/shop name below the QR code for trust"
    ]
}


def retrieve_context(query: str) -> str:
    """
    Simple keyword-based retrieval from knowledge base.
    Returns relevant context as a string for RAG augmentation.
    """
    query_lower = query.lower()
    context_parts = []

    # Match schemes
    if any(w in query_lower for w in ["loan", "scheme", "credit", "mudra", "svanidhi", "msme", "money", "fund"]):
        for scheme in KNOWLEDGE_BASE["msme_schemes"]:
            context_parts.append(
                f"SCHEME: {scheme['name']} - {scheme['description']}. "
                f"Benefit: {scheme.get('benefit', '')}. Apply at: {scheme.get('portal', scheme.get('how_to_apply', ''))}"
            )

    # Match UPI / payments
    if any(w in query_lower for w in ["upi", "payment", "qr", "digital payment", "phonepe", "gpay", "bhim", "paytm"]):
        upi = KNOWLEDGE_BASE["upi_setup_steps"]
        context_parts.append(
            f"UPI SETUP: BHIM UPI steps: {', '.join(upi['bhim_upi'][:3])}. "
            f"PhonePe Business: {', '.join(upi['phonepe_for_business'][:3])}. "
            f"QR Tips: {'; '.join(KNOWLEDGE_BASE['qr_code_tips'][:3])}"
        )

    # Match listings / SEO
    if any(w in query_lower for w in ["list", "online", "google", "seo", "visible", "platform", "sell online", "meesho"]):
        for p in KNOWLEDGE_BASE["digital_listing_platforms"]:
            context_parts.append(
                f"PLATFORM: {p['platform']} ({p['category']}) - Cost: {p['cost']}. "
                f"Benefit: {p['benefit']}. Steps: {', '.join(p['steps'][:2])}"
            )

    # Match pricing
    if any(w in query_lower for w in ["price", "pricing", "cost", "rate", "charge", "how much"]):
        for category, tip in KNOWLEDGE_BASE["pricing_tips"].items():
            context_parts.append(f"PRICING TIP ({category}): {tip}")

    # Match city/location
    for city, areas in KNOWLEDGE_BASE["cities_hotspots"].items():
        if city in query_lower:
            context_parts.append(f"HOT SPOTS IN {city.upper()}: {', '.join(areas)}")

    # Match language
    for lang, words in KNOWLEDGE_BASE["local_languages"].items():
        if lang in query_lower:
            context_parts.append(f"LOCAL LANGUAGE ({lang}): {words}")

    # Default fallback - provide general context
    if not context_parts:
        context_parts.append(
            "GENERAL: PM SVANidhi offers Rs.10,000-50,000 loans for street vendors. "
            "UPI via BHIM/PhonePe Business allows digital payments. "
            "List on Google Business Profile for free local SEO. "
            "Register on ONDC via Meesho for online sales. "
            "MSME Udyam registration is free and unlocks government benefits."
        )

    return "\n".join(context_parts)
