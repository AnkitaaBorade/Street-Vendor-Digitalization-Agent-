# app.py
# Street Vendor Digitalization Agent — Streamlit UI
# Deploy FREE on Streamlit Cloud (share.streamlit.io)

import os
import streamlit as st
from dotenv import load_dotenv
from knowledge_base import retrieve_context, KNOWLEDGE_BASE
from granite_client import get_granite_client, build_rag_prompt, generate_with_granite, fallback_response
from vendor_profile import extract_vendor_info, generate_vendor_profile

# Load .env locally; on Streamlit Cloud secrets come from st.secrets
load_dotenv()

# Push st.secrets into os.environ so existing modules (granite_client etc.) work unchanged
for _k in ["IBM_API_KEY", "IBM_PROJECT_ID", "IBM_WML_URL", "GRANITE_MODEL_ID"]:
    if _k not in os.environ:
        try:
            os.environ[_k] = st.secrets[_k]
        except Exception:
            pass

# ── Page config ───────────────────────────────────────────
st.set_page_config(
    page_title="Street Vendor Digitalization Agent",
    page_icon="🏪",
    layout="wide"
)

# ── Inline CSS ────────────────────────────────────────────
st.markdown("""
<style>
  /* Global */
  [data-testid="stAppViewContainer"] { background: #f8f9fc; }
  [data-testid="stHeader"] { background: #ffffff; border-bottom: 1px solid #e5e7eb; }

  /* Hero banner */
  .hero {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    color: white;
    padding: 32px 28px;
    border-radius: 14px;
    text-align: center;
    margin-bottom: 24px;
  }
  .hero h1 { font-size: 26px; font-weight: 800; margin: 0 0 8px; }
  .hero p  { font-size: 14px; opacity: .9; margin: 0 0 14px; }
  .chips   { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; }
  .chip {
    background: rgba(255,255,255,.18);
    border: 1px solid rgba(255,255,255,.3);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 12px;
  }
  .status-pill {
    display: inline-block;
    background: rgba(255,255,255,.2);
    border: 1px solid rgba(255,255,255,.4);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 12px;
    margin-top: 8px;
  }

  /* Info tiles */
  .tile-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px; }
  .tile {
    flex: 1; min-width: 140px;
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
  }
  .tile .t-icon  { font-size: 26px; }
  .tile .t-label { font-size: 13px; font-weight: 600; color: #374151; margin-top: 6px; }
  .tile .t-sub   { font-size: 11px; color: #9ca3af; }

  /* Response card */
  .resp-card {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px;
    margin-top: 16px;
  }
  .resp-card h3 { color: #4f46e5; font-size: 15px; margin-bottom: 10px; }

  /* Profile card */
  .prof-card {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px;
  }

  /* Scheme cards */
  .scheme { border-left: 4px solid #4f46e5; background: #fff; border-radius: 8px; padding: 14px; margin-bottom: 10px; border: 1px solid #e5e7eb; }
  .scheme.green  { border-left-color: #059669; }
  .scheme.purple { border-left-color: #7c3aed; }
  .scheme.amber  { border-left-color: #f59e0b; }
  .scheme .s-name   { font-weight: 700; color: #1f2937; font-size: 14px; }
  .scheme .s-amount { color: #059669; font-size: 13px; font-weight: 600; margin: 3px 0; }
  .scheme .s-desc   { color: #6b7280; font-size: 12px; }

  /* Pricing tip box */
  .tip-box { background: #fef3c7; border-radius: 8px; padding: 12px; margin: 10px 0; }
  .tip-box .tip-label { font-weight: 600; color: #92400e; font-size: 13px; }
  .tip-box .tip-text  { color: #78350f; font-size: 13px; }

  /* QR tip */
  .qr-tip { background: #ede9fe; border-radius: 8px; padding: 10px 14px; font-size: 13px; color: #5b21b6; margin-top: 10px; }

  /* Example pills */
  .stButton > button {
    background: #ede9fe;
    color: #5b21b6;
    border: 1px solid #ddd6fe;
    border-radius: 20px;
    font-size: 12px;
    padding: 4px 14px;
    width: 100%;
  }
  .stButton > button:hover { background: #ddd6fe; }

  /* Ask button */
  div[data-testid="stButton"] > button[kind="primary"] {
    background: #4f46e5;
    color: white;
    border-radius: 10px;
    font-weight: 600;
    border: none;
    width: 100%;
    padding: 12px;
  }

  footer { visibility: hidden; }
  .custom-footer { text-align:center; color:#9ca3af; font-size:12px; margin-top:24px; padding-top:16px; border-top:1px solid #e5e7eb; }
</style>
""", unsafe_allow_html=True)


# ── Init Granite (cached so it runs once) ─────────────────
@st.cache_resource
def load_model():
    return get_granite_client()

granite_model = load_model()
model_label   = "IBM Granite Active" if granite_model else "Fallback Mode"


# ── Hero ──────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <h1>Street Vendor Digitalization Agent</h1>
  <p>Powered by IBM Granite AI &amp; RAG — helping local hawkers and micro-entrepreneurs grow digitally,
     access credit, and boost visibility in the hyperlocal economy.</p>
  <div class="chips">
    <span class="chip">Hyperlocal SEO</span>
    <span class="chip">UPI Setup</span>
    <span class="chip">MSME Schemes</span>
    <span class="chip">ONDC Listing</span>
    <span class="chip">Local Languages</span>
    <span class="chip">Pricing Tips</span>
  </div>
  <div><span class="status-pill">{model_label}</span></div>
</div>
""", unsafe_allow_html=True)


# ── Info tiles ────────────────────────────────────────────
st.markdown("""
<div class="tile-row">
  <div class="tile"><div class="t-icon">💰</div><div class="t-label">PM SVANidhi</div><div class="t-sub">Loans up to Rs.50,000</div></div>
  <div class="tile"><div class="t-icon">📱</div><div class="t-label">UPI Payments</div><div class="t-sub">QR Setup in 5 min</div></div>
  <div class="tile"><div class="t-icon">🗺️</div><div class="t-label">Google Maps</div><div class="t-sub">Free local visibility</div></div>
  <div class="tile"><div class="t-icon">🛍️</div><div class="t-label">ONDC/Meesho</div><div class="t-sub">0% commission sales</div></div>
</div>
""", unsafe_allow_html=True)


# ── Input area ────────────────────────────────────────────
col_in, col_lang = st.columns([3, 1])
with col_in:
    vendor_query = st.text_area(
        "Tell us about your business",
        placeholder="e.g. I sell fruit in Pune's Camp area and want to grow my business digitally...",
        height=100,
        key="query"
    )
with col_lang:
    language = st.selectbox(
        "Response Language",
        ["English", "Hindi", "Marathi", "Tamil", "Telugu", "Kannada", "Bengali", "Gujarati"]
    )

# ── Example pills ─────────────────────────────────────────
st.markdown("**Try these examples:**")
ex_cols = st.columns(3)
examples = [
    "I sell fruit in Pune's Camp area",
    "I run a chai stall in Mumbai Dharavi",
    "Vegetable vendor in Delhi Sarojini Nagar",
    "Fish seller in Chennai T Nagar market",
    "Flower vendor in Bangalore Commercial Street",
    "I need a loan for my food stall in Hyderabad"
]
for i, ex in enumerate(examples):
    with ex_cols[i % 3]:
        if st.button(ex, key=f"ex_{i}"):
            st.session_state["query"] = ex
            st.rerun()

st.markdown("")

ask_clicked = st.button("Ask Agent →", type="primary")


# ── Agent logic ───────────────────────────────────────────
if ask_clicked and vendor_query.strip():
    with st.spinner("Analyzing your business and retrieving best digital strategies..."):
        context = retrieve_context(vendor_query)

        if granite_model:
            prompt   = build_rag_prompt(vendor_query, context, language)
            response = generate_with_granite(granite_model, prompt)
            if not response:
                response = fallback_response(vendor_query, context)
        else:
            response = fallback_response(vendor_query, context)

        vendor_info = extract_vendor_info(vendor_query)
        profile     = generate_vendor_profile(vendor_info)

    # ── Response tabs ──────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["Agent Recommendation", "Your Digital Profile", "Government Schemes"])

    with tab1:
        st.markdown(f"""<div class="resp-card"><h3>Agent Recommendation</h3></div>""", unsafe_allow_html=True)
        st.markdown(response)

    with tab2:
        st.markdown(f"""
<div class="prof-card">
  <h3 style="font-size:17px;font-weight:700;color:#1f2937;margin-bottom:4px;">{profile['business_name']}</h3>
  <p style="color:#6b7280;font-size:13px;margin-bottom:14px;">📍 {profile['location']} &nbsp;|&nbsp; {profile['category']}</p>
</div>
""", unsafe_allow_html=True)

        st.markdown("**Pricing Tip**")
        st.info(profile['pricing_tip'])

        st.markdown("**Recommended Platforms**")
        for p in profile['recommended_platforms']:
            st.markdown(f"- **{p['name']}** ({p['cost']}) — {p['benefit']}")

        st.markdown("**UPI Quick Start (PhonePe Business)**")
        for i, step in enumerate(profile['upi_quick_start'], 1):
            st.markdown(f"{i}. {step}")
        st.code(profile['suggested_upi_id'], language=None)

        st.markdown("**Government Schemes**")
        for s in profile['government_schemes']:
            st.markdown(f"- **{s['name']}** — {s['amount']}  \n  {s['portal']}")

        st.markdown(f"""<div class="qr-tip">📱 <strong>QR Tip:</strong> {profile['qr_tip']}</div>""", unsafe_allow_html=True)

    with tab3:
        st.markdown("""
<div class="scheme">
  <div class="s-name">PM SVANidhi</div>
  <div class="s-amount">Rs.10,000 → Rs.20,000 → Rs.50,000</div>
  <div class="s-desc">Collateral-free micro loans for street vendors. Digital transactions earn Rs.1,200 cashback/year.</div>
</div>
<div class="scheme green">
  <div class="s-name">MUDRA Yojana (Shishu)</div>
  <div class="s-amount">Up to Rs.50,000</div>
  <div class="s-desc">Micro loans for non-farm enterprises. No collateral. Low interest rates.</div>
</div>
<div class="scheme purple">
  <div class="s-name">Udyam (MSME) Registration</div>
  <div class="s-amount">Free Registration</div>
  <div class="s-desc">Free online registration via Aadhaar. Unlocks bank credit, tax benefits, government tenders.</div>
</div>
<div class="scheme amber">
  <div class="s-name">ONDC Network</div>
  <div class="s-amount">0% Commission</div>
  <div class="s-desc">Government-backed digital commerce. Sell via Meesho, Paytm, PhonePe.</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
| Portal | Link |
|--------|------|
| PM SVANidhi | https://pmsvanidhi.mohua.gov.in |
| MUDRA | https://mudra.org.in |
| Udyam Registration | https://udyamregistration.gov.in |
| ONDC | https://ondc.org |
""")

elif ask_clicked and not vendor_query.strip():
    st.warning("Please describe your business first!")


# ── Static schemes section (always visible) ───────────────
with st.expander("View All Government Schemes", expanded=False):
    st.markdown("""
**PM SVANidhi** — [pmsvanidhi.mohua.gov.in](https://pmsvanidhi.mohua.gov.in)
Collateral-free loans Rs.10,000–50,000 for street vendors. Digital payment incentive Rs.1,200/year.

**MUDRA Yojana** — [mudra.org.in](https://mudra.org.in)
Up to Rs.50,000 (Shishu), Rs.5 lakh (Kishore), Rs.10 lakh (Tarun). No collateral.

**Udyam Registration** — [udyamregistration.gov.in](https://udyamregistration.gov.in)
Free MSME registration. Aadhaar-based. Unlocks priority lending and government schemes.

**ONDC** — [ondc.org](https://ondc.org)
Sell online at 0% commission via Meesho, PhonePe, Paytm on the government's open network.
""")


st.markdown("""
<div class="custom-footer">
  Built with IBM Granite AI &amp; RAG &nbsp;|&nbsp; Empowering Street Vendors Digitally<br>
  <span style="color:#c4b5fd;">Made with IBM Bob</span>
</div>
""", unsafe_allow_html=True)
