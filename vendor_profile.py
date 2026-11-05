# vendor_profile.py
# Generates a structured digital business profile for a street vendor

import json
from knowledge_base import KNOWLEDGE_BASE


def extract_vendor_info(query: str) -> dict:
    """Parse vendor query to extract business type, location, and language."""
    query_lower = query.lower()

    # Detect product/business type
    business_map = {
        "fruit": "Fruit Vendor", "vegetable": "Vegetable Vendor", "sabzi": "Vegetable Vendor",
        "chai": "Chai/Tea Stall", "tea": "Chai/Tea Stall", "coffee": "Coffee Stall",
        "food": "Street Food Vendor", "snack": "Snack Stall", "vada": "Street Food Vendor",
        "pav": "Street Food Vendor", "biryani": "Food Stall", "juice": "Juice Corner",
        "fish": "Fish Vendor", "meat": "Meat/Poultry Vendor", "chicken": "Meat/Poultry Vendor",
        "flower": "Flower Vendor", "cloth": "Clothing Vendor", "saree": "Saree/Clothing Vendor",
        "garment": "Garment Vendor", "toy": "Toys Vendor", "book": "Book Vendor",
        "stationery": "Stationery Vendor", "electric": "Electronics Vendor",
        "mobile": "Mobile Accessories Vendor", "hardware": "Hardware Shop",
        "pan": "Pan/Tobacco Shop", "grocery": "Grocery Vendor"
    }

    business_type = "Street Vendor"
    for keyword, btype in business_map.items():
        if keyword in query_lower:
            business_type = btype
            break

    # Detect city
    city = "Local City"
    for c in KNOWLEDGE_BASE["cities_hotspots"]:
        if c in query_lower:
            city = c.title()
            break

    # Detect area within city
    area = ""
    for c, areas in KNOWLEDGE_BASE["cities_hotspots"].items():
        if c in query_lower:
            for a in areas:
                if a.lower() in query_lower:
                    area = a
                    break

    # Detect language
    language = "English"
    lang_map = {
        "marathi": "Marathi", "hindi": "Hindi", "tamil": "Tamil",
        "telugu": "Telugu", "kannada": "Kannada", "bengali": "Bengali",
        "gujarati": "Gujarati", "punjabi": "Punjabi"
    }
    for lang_key, lang_name in lang_map.items():
        if lang_key in query_lower:
            language = lang_name
            break

    # Detect category for pricing tips
    category = "general"
    if "fruit" in query_lower:
        category = "fruits"
    elif any(v in query_lower for v in ["vegetable", "sabzi"]):
        category = "vegetables"
    elif any(f in query_lower for f in ["food", "snack", "chai", "vada", "biryani"]):
        category = "street_food"
    elif any(c in query_lower for c in ["cloth", "saree", "garment"]):
        category = "clothing"

    return {
        "business_type": business_type,
        "city": city,
        "area": area or f"{city} Market Area",
        "language": language,
        "category": category,
        "raw_query": query
    }


def generate_vendor_profile(vendor_info: dict) -> dict:
    """Generate a complete digital business profile."""
    business_type = vendor_info["business_type"]
    city = vendor_info["city"]
    area = vendor_info["area"]
    category = vendor_info["category"]

    pricing_tip = KNOWLEDGE_BASE["pricing_tips"].get(
        category, KNOWLEDGE_BASE["pricing_tips"]["general"]
    )

    # Recommend top 2 platforms
    platforms = KNOWLEDGE_BASE["digital_listing_platforms"][:2]

    # Get UPI recommendation
    upi_steps = KNOWLEDGE_BASE["upi_setup_steps"]["phonepe_for_business"][:3]

    # Get relevant schemes
    schemes = KNOWLEDGE_BASE["msme_schemes"][:2]

    profile = {
        "business_name": f"{area} {business_type}",
        "business_type": business_type,
        "location": f"{area}, {city}",
        "category": category.replace("_", " ").title(),
        "suggested_upi_id": f"{business_type.lower().replace(' ', '')}@upi",
        "pricing_tip": pricing_tip,
        "recommended_platforms": [
            {"name": p["platform"], "benefit": p["benefit"], "cost": p["cost"]}
            for p in platforms
        ],
        "upi_quick_start": upi_steps,
        "government_schemes": [
            {"name": s["name"], "amount": s.get("loan_amount", "See portal"), "portal": s.get("portal", s.get("how_to_apply", ""))}
            for s in schemes
        ],
        "qr_tip": KNOWLEDGE_BASE["qr_code_tips"][0],
        "language": vendor_info["language"]
    }

    return profile


def profile_to_html_card(profile: dict) -> str:
    """Convert vendor profile dict to an HTML display card."""
    platforms_html = "".join([
        f'<div style="background:#f0f4ff;border-left:3px solid #4f46e5;padding:8px 12px;margin:6px 0;border-radius:4px;">'
        f'<strong>{p["name"]}</strong> — {p["benefit"]} <span style="color:#7c3aed;font-size:12px;">({p["cost"]})</span></div>'
        for p in profile["recommended_platforms"]
    ])

    schemes_html = "".join([
        f'<div style="background:#f0fff4;border-left:3px solid #059669;padding:8px 12px;margin:6px 0;border-radius:4px;">'
        f'<strong>{s["name"]}</strong><br>'
        f'<span style="color:#065f46;font-size:13px;">Amount: {s["amount"]}</span><br>'
        f'<a href="{s["portal"]}" target="_blank" style="color:#4f46e5;font-size:12px;">{s["portal"]}</a></div>'
        for s in profile["government_schemes"]
    ])

    upi_steps_html = "".join([
        f'<li style="margin:4px 0;color:#374151;">{step}</li>'
        for step in profile["upi_quick_start"]
    ])

    return f"""
<div style="background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:20px;margin:16px 0;">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
    <div style="background:#4f46e5;color:#fff;border-radius:8px;padding:8px 14px;font-size:20px;">🏪</div>
    <div>
      <div style="font-size:18px;font-weight:700;color:#1f2937;">{profile['business_name']}</div>
      <div style="font-size:13px;color:#6b7280;">📍 {profile['location']} &nbsp;|&nbsp; 🏷️ {profile['category']}</div>
    </div>
  </div>

  <div style="background:#fef3c7;border-radius:8px;padding:12px;margin-bottom:14px;">
    <div style="font-weight:600;color:#92400e;margin-bottom:4px;">💡 Pricing Tip</div>
    <div style="color:#78350f;font-size:14px;">{profile['pricing_tip']}</div>
  </div>

  <div style="margin-bottom:14px;">
    <div style="font-weight:600;color:#1f2937;margin-bottom:8px;">🌐 Recommended Digital Platforms</div>
    {platforms_html}
  </div>

  <div style="margin-bottom:14px;">
    <div style="font-weight:600;color:#1f2937;margin-bottom:8px;">💳 UPI Quick Start (PhonePe Business)</div>
    <ol style="margin:0;padding-left:20px;">{upi_steps_html}</ol>
    <div style="margin-top:8px;font-size:13px;color:#6b7280;">Suggested UPI ID: <code style="background:#f3f4f6;padding:2px 6px;border-radius:4px;">{profile['suggested_upi_id']}</code></div>
  </div>

  <div style="margin-bottom:10px;">
    <div style="font-weight:600;color:#1f2937;margin-bottom:8px;">🏛️ Government Schemes for You</div>
    {schemes_html}
  </div>

  <div style="background:#ede9fe;border-radius:8px;padding:10px;font-size:13px;color:#5b21b6;">
    📱 <strong>QR Code Tip:</strong> {profile['qr_tip']}
  </div>
</div>
"""
