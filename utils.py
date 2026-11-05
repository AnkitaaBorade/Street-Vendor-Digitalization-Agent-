# utils.py
# Utility helpers for UPI guide, local SEO, and promotional content generation

from knowledge_base import KNOWLEDGE_BASE


def get_upi_guide(platform: str = "phonepe") -> dict:
    """Return step-by-step UPI setup guide for a given platform."""
    platform = platform.lower().replace(" ", "_").replace("for_business", "").strip("_")
    platform_map = {
        "phonepe": "phonepe_for_business",
        "googlepay": "google_pay",
        "gpay": "google_pay",
        "bhim": "bhim_upi",
        "upi": "bhim_upi"
    }
    key = platform_map.get(platform, "bhim_upi")
    steps = KNOWLEDGE_BASE["upi_setup_steps"].get(key, KNOWLEDGE_BASE["upi_setup_steps"]["bhim_upi"])
    return {"platform": key.replace("_", " ").title(), "steps": steps}


def get_seo_tips(city: str, business_type: str) -> list:
    """Generate local SEO tips tailored to city and business type."""
    hotspots = KNOWLEDGE_BASE["cities_hotspots"].get(city.lower(), [])
    areas_str = ", ".join(hotspots[:3]) if hotspots else f"{city} market areas"

    tips = [
        f"Create a Google Business Profile — search '{business_type} near me in {city}' to see your competition",
        f"Use keywords like '{business_type} {city}', '{business_type} {areas_str}' in your business description",
        f"Add your exact stall location pin on Google Maps for customers in {areas_str}",
        "Upload 5+ clear photos of your products and stall — listings with photos get 3x more clicks",
        "Ask happy customers to leave a Google review — even 5 reviews rank you higher locally",
        "Post on local Facebook/WhatsApp groups: 'Fresh fruits available daily at Camp Area, Pune'",
        f"Use WhatsApp Business — set your location to {city} and share daily stock updates as status",
        "Join local vendor communities on Telegram and Facebook for free cross-promotion"
    ]
    return tips


def get_promotional_content(business_type: str, city: str, language: str = "English") -> dict:
    """Generate simple promotional messages for WhatsApp/social media."""
    lang_data = KNOWLEDGE_BASE["local_languages"].get(language.lower(), {})
    greeting  = lang_data.get("greeting", "Hello")
    buy_text  = lang_data.get("buy", "Buy Now")
    discount  = lang_data.get("discount", "Discount")

    messages = {
        "whatsapp_status": f"🛒 Fresh {business_type} available today! Visit us in {city}. Quality guaranteed. {greeting}! 📱 Digital payments accepted.",
        "daily_offer":     f"Today's Special: Buy 1kg {business_type}, get 250g FREE! Limited stock. {buy_text} now! 📍 {city}",
        "upi_promotion":   f"💳 We now accept UPI / QR payments! No change needed. {discount} on digital payments. Scan & Pay! 🙏",
        "festival_offer":  f"🎉 Festival {discount}! Special prices on {business_type} this week. {greeting} to all our valued customers!",
        "opening_message": f"📢 Now open! {business_type.title()} stall at {city}. Fresh stock daily. WhatsApp us for orders. UPI accepted. {greeting}!"
    }

    return {
        "language": language,
        "greeting": greeting,
        "messages": messages,
        "tip": "Post your WhatsApp status daily with stock updates — it's free advertising to all your contacts!"
    }


def get_scheme_eligibility(vendor_type: str, has_aadhaar: bool = True, has_bank_account: bool = True) -> list:
    """Check which government schemes a vendor likely qualifies for."""
    eligible = []

    for scheme in KNOWLEDGE_BASE["msme_schemes"]:
        scheme_name = scheme["name"].lower()
        reasons = []

        if "svanidhi" in scheme_name:
            if has_aadhaar and has_bank_account:
                reasons.append("Street vendor with Aadhaar + bank account qualifies")
        elif "mudra" in scheme_name:
            if has_bank_account:
                reasons.append("Non-farm micro enterprise with bank account qualifies")
        elif "udyam" in scheme_name:
            if has_aadhaar:
                reasons.append("Any micro enterprise owner with Aadhaar can register for free")
        elif "ondc" in scheme_name:
            reasons.append("Any vendor with a mobile phone can join ONDC network")

        if reasons:
            eligible.append({
                "name":        scheme["name"],
                "description": scheme["description"],
                "benefit":     scheme.get("benefit", ""),
                "portal":      scheme.get("portal", scheme.get("how_to_apply", "")),
                "reason":      reasons[0]
            })

    return eligible


def format_markdown_response(text: str) -> str:
    """Convert simple markdown-like text to basic HTML for display."""
    lines   = text.split("\n")
    html    = []
    in_list = False

    for line in lines:
        line = line.strip()
        if not line:
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append("<br>")
            continue

        if line.startswith("**") and line.endswith("**"):
            html.append(f'<strong style="color:#4f46e5;">{line[2:-2]}</strong>')
        elif line.startswith("• ") or line.startswith("- "):
            if not in_list:
                html.append('<ul style="margin:8px 0;padding-left:20px;">')
                in_list = True
            html.append(f'<li style="margin:3px 0;color:#374151;">{line[2:]}</li>')
        elif line.startswith("**") and "**" in line[2:]:
            # Inline bold
            formatted = line.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
            html.append(f'<p style="margin:6px 0;color:#374151;">{formatted}</p>')
        else:
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f'<p style="margin:6px 0;color:#374151;">{line}</p>')

    if in_list:
        html.append("</ul>")

    return "\n".join(html)
