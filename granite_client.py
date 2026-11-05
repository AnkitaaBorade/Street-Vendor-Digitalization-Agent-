# granite_client.py
# IBM Granite LLM integration via ibm-watsonx-ai SDK

import os
from dotenv import load_dotenv

load_dotenv()

# Try to import IBM watsonx SDK; fall back gracefully if not installed
try:
    from ibm_watsonx_ai import APIClient, Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference
    # metanames path changed in v1.3+; try both locations
    try:
        from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
    except ImportError:
        from ibm_watsonx_ai.foundation_models.utils.enums import GenTextParamsMetaNames as GenParams
    IBM_SDK_AVAILABLE = True
except ImportError:
    IBM_SDK_AVAILABLE = False


def get_granite_client():
    """Initialize and return IBM Granite model client."""
    if not IBM_SDK_AVAILABLE:
        return None

    api_key = os.getenv("IBM_API_KEY", "")
    project_id = os.getenv("IBM_PROJECT_ID", "")
    wml_url = os.getenv("IBM_WML_URL", "https://us-south.ml.cloud.ibm.com")
    model_id = os.getenv("GRANITE_MODEL_ID", "ibm/granite-3-8b-instruct")

    if not api_key or api_key == "your_ibm_api_key_here":
        return None

    try:
        credentials = Credentials(url=wml_url, api_key=api_key)
        client = APIClient(credentials=credentials, project_id=project_id)
        model = ModelInference(
            model_id=model_id,
            api_client=client,
            params={
                GenParams.MAX_NEW_TOKENS: 600,
                GenParams.TEMPERATURE: 0.7,
                GenParams.TOP_P: 0.9,
            }
        )
        return model
    except Exception as e:
        print(f"[IBM Granite] Connection error: {e}")
        return None


def generate_with_granite(model, prompt: str) -> str:
    """Generate text using IBM Granite model (chat API)."""
    try:
        # Use chat API (newer, non-deprecated)
        response = model.chat(messages=[{"role": "user", "content": prompt}])
        content = response["choices"][0]["message"]["content"]
        return content.strip() if content else ""
    except Exception:
        # Fallback to generate_text if chat not available
        try:
            response = model.generate_text(prompt=prompt)
            return response.strip() if response else ""
        except Exception as e:
            print(f"[IBM Granite] Generation error: {e}")
            return ""


def build_rag_prompt(vendor_query: str, retrieved_context: str, language: str = "English") -> str:
    """Build a structured RAG prompt for IBM Granite."""
    return f"""You are a helpful Street Vendor Digitalization Agent for India. 
You assist local hawkers and micro-entrepreneurs to grow their business digitally.
Answer in {language} language. Be practical, simple, and actionable.

RETRIEVED CONTEXT (use this to answer):
{retrieved_context}

VENDOR QUERY: {vendor_query}

Provide a clear, structured response with:
1. Immediate actionable steps (2-3 steps)
2. Relevant government scheme or platform recommendation
3. Digital payment / online visibility tip
4. One encouraging closing line

Response:"""


def fallback_response(vendor_query: str, retrieved_context: str) -> str:
    """
    Fallback rule-based response when IBM Granite is not configured.
    Uses retrieved context to generate a helpful response.
    """
    query_lower = vendor_query.lower()

    # Parse vendor info from query
    business_type = "your business"
    location = "your area"

    # Detect business type
    food_items = ["fruit", "vegetable", "food", "snack", "chai", "tea", "juice", "fish", "meat"]
    cloth_items = ["cloth", "saree", "dress", "shirt", "garment", "fabric"]
    for item in food_items:
        if item in query_lower:
            business_type = f"{item} vendor"
            break
    for item in cloth_items:
        if item in query_lower:
            business_type = f"{item} seller"
            break

    # Detect city
    cities = ["pune", "mumbai", "delhi", "bangalore", "chennai", "hyderabad", "kolkata", "ahmedabad"]
    for city in cities:
        if city in query_lower:
            location = city.title()
            break

    response = f"""
**Digital Growth Plan for Your {business_type.title()} in {location}**

---

**Step 1: Get Digitally Visible (Free)**
• Create a **Google Business Profile** at business.google.com — customers searching near {location} will find you
• List on **JustDial** for free at justdial.com/free-listing
• Set up a **WhatsApp Business** profile with your catalog and timings

**Step 2: Accept Digital Payments**
• Download **PhonePe for Business** or **BHIM UPI** — get your QR code printed and laminated
• Display QR code prominently — customers trust digital sellers more
• You earn cashback incentives up to **Rs. 1,200/year** for digital transactions under PM SVANidhi

**Step 3: Access Government Credit**
• Apply for **PM SVANidhi loan** (Rs. 10,000 collateral-free) at pmsvanidhi.mohua.gov.in
• Register on **Udyam (MSME)** for free at udyamregistration.gov.in — unlocks bank loans & schemes
• **MUDRA Yojana** (Shishu) offers up to Rs. 50,000 for micro-businesses

**Step 4: Sell Online**
• Join **ONDC network** via Meesho Supplier app — 0% commission, reach customers across India
• Create product photos using just your phone — good lighting = more sales

---

*You're already running a real business — going digital just means more customers find you! 🚀*

**Relevant Context Retrieved:**
{retrieved_context[:400]}...
"""
    return response.strip()
