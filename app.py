# app.py
# Street Vendor Digitalization Agent - Main Flask Application
# Powered by IBM Granite (RAG) + Python

import os
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
from knowledge_base import retrieve_context
from granite_client import get_granite_client, build_rag_prompt, generate_with_granite, fallback_response
from vendor_profile import extract_vendor_info, generate_vendor_profile, profile_to_html_card

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "vendor_agent_secret")

# Initialize IBM Granite client once at startup
granite_model = get_granite_client()
if granite_model:
    print("[APP] IBM Granite model connected successfully.")
else:
    print("[APP] Running in fallback mode (IBM Granite not configured).")


# ─────────────────────────────────────────────
# HTML PAGE (inline CSS, light theme + indigo/violet pop)
# ─────────────────────────────────────────────

MAIN_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Street Vendor Digitalization Agent</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: -apple-system, "Segoe UI", system-ui, sans-serif;
      background: #f8f9fc;
      color: #1f2937;
      min-height: 100vh;
    }

    /* ── Header ── */
    header {
      background: #ffffff;
      border-bottom: 1px solid #e5e7eb;
      padding: 0 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 64px;
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0 1px 4px rgba(0,0,0,.06);
    }
    .logo {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 18px;
      font-weight: 700;
      color: #4f46e5;
    }
    .logo span { color: #1f2937; }
    .ibm-badge {
      background: #4f46e5;
      color: #fff;
      font-size: 11px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 20px;
      letter-spacing: .4px;
    }

    /* ── Hero ── */
    .hero {
      background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
      color: #fff;
      padding: 48px 24px 40px;
      text-align: center;
    }
    .hero h1 { font-size: 28px; font-weight: 800; margin-bottom: 10px; }
    .hero p  { font-size: 15px; opacity: .88; max-width: 560px; margin: 0 auto 24px; line-height: 1.6; }
    .hero-chips { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; }
    .chip {
      background: rgba(255,255,255,.18);
      border: 1px solid rgba(255,255,255,.3);
      color: #fff;
      border-radius: 20px;
      padding: 4px 12px;
      font-size: 12px;
    }

    /* ── Main Layout ── */
    .container { max-width: 900px; margin: 0 auto; padding: 28px 16px; }

    /* ── Chat / Query Box ── */
    .query-card {
      background: #ffffff;
      border: 1px solid #e5e7eb;
      border-radius: 14px;
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: 0 2px 8px rgba(0,0,0,.05);
    }
    .query-card h2 { font-size: 16px; font-weight: 700; color: #1f2937; margin-bottom: 14px; }

    .input-row {
      display: flex;
      gap: 10px;
      align-items: flex-start;
      flex-wrap: wrap;
    }
    textarea {
      flex: 1;
      min-width: 240px;
      border: 1.5px solid #d1d5db;
      border-radius: 10px;
      padding: 12px 14px;
      font-size: 14px;
      font-family: inherit;
      resize: vertical;
      min-height: 80px;
      outline: none;
      transition: border-color .2s;
      color: #1f2937;
      background: #fafafa;
    }
    textarea:focus { border-color: #4f46e5; background: #fff; }

    .lang-select {
      border: 1.5px solid #d1d5db;
      border-radius: 10px;
      padding: 10px 12px;
      font-size: 14px;
      font-family: inherit;
      background: #fafafa;
      color: #1f2937;
      outline: none;
      cursor: pointer;
    }
    .lang-select:focus { border-color: #4f46e5; }

    .btn-ask {
      background: #4f46e5;
      color: #fff;
      border: none;
      border-radius: 10px;
      padding: 12px 24px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      transition: background .2s, transform .1s;
      white-space: nowrap;
    }
    .btn-ask:hover  { background: #4338ca; }
    .btn-ask:active { transform: scale(.97); }
    .btn-ask:disabled { background: #a5b4fc; cursor: not-allowed; }

    /* ── Example Queries ── */
    .examples { margin-top: 14px; }
    .examples p { font-size: 12px; color: #6b7280; margin-bottom: 8px; }
    .example-pills { display: flex; flex-wrap: wrap; gap: 7px; }
    .pill {
      background: #ede9fe;
      color: #5b21b6;
      border: 1px solid #ddd6fe;
      border-radius: 20px;
      padding: 4px 12px;
      font-size: 12px;
      cursor: pointer;
      transition: background .15s;
    }
    .pill:hover { background: #ddd6fe; }

    /* ── Response Area ── */
    #response-area { display: none; }

    .response-card {
      background: #fff;
      border: 1px solid #e5e7eb;
      border-radius: 14px;
      padding: 24px;
      margin-bottom: 20px;
      box-shadow: 0 2px 8px rgba(0,0,0,.05);
    }
    .response-card h3 {
      font-size: 15px;
      font-weight: 700;
      color: #4f46e5;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .response-text {
      font-size: 14px;
      line-height: 1.75;
      color: #374151;
      white-space: pre-wrap;
    }

    /* ── Loading Spinner ── */
    .spinner {
      display: none;
      text-align: center;
      padding: 32px;
      color: #6b7280;
      font-size: 14px;
    }
    .spinner-ring {
      width: 36px; height: 36px;
      border: 3px solid #e5e7eb;
      border-top-color: #4f46e5;
      border-radius: 50%;
      animation: spin .7s linear infinite;
      margin: 0 auto 12px;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    /* ── Info Strip ── */
    .info-strip {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 14px;
      margin-bottom: 24px;
    }
    .info-tile {
      background: #fff;
      border: 1px solid #e5e7eb;
      border-radius: 12px;
      padding: 18px;
      text-align: center;
      box-shadow: 0 1px 4px rgba(0,0,0,.04);
    }
    .info-tile .icon { font-size: 28px; margin-bottom: 8px; }
    .info-tile .label { font-size: 13px; font-weight: 600; color: #374151; }
    .info-tile .sub { font-size: 11px; color: #9ca3af; margin-top: 3px; }

    /* ── Schemes Section ── */
    .schemes-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 14px;
      margin-bottom: 24px;
    }
    .scheme-card {
      background: #fff;
      border: 1px solid #e5e7eb;
      border-left: 4px solid #4f46e5;
      border-radius: 10px;
      padding: 16px;
    }
    .scheme-card .s-name { font-weight: 700; color: #1f2937; font-size: 14px; }
    .scheme-card .s-amount { color: #059669; font-size: 13px; margin: 4px 0; font-weight: 600; }
    .scheme-card .s-desc  { color: #6b7280; font-size: 12px; line-height: 1.5; }
    .scheme-card a { color: #4f46e5; font-size: 12px; text-decoration: none; }
    .scheme-card a:hover { text-decoration: underline; }

    /* ── Status Badge ── */
    .model-status {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      color: #6b7280;
    }
    .dot { width: 8px; height: 8px; border-radius: 50%; background: #10b981; }
    .dot.offline { background: #f59e0b; }

    /* ── Footer ── */
    footer {
      text-align: center;
      padding: 24px 16px;
      border-top: 1px solid #e5e7eb;
      color: #9ca3af;
      font-size: 12px;
      margin-top: 12px;
    }

    @media (max-width: 600px) {
      .hero h1 { font-size: 22px; }
      .input-row { flex-direction: column; }
      .btn-ask { width: 100%; }
    }
  </style>
</head>
<body>

<!-- Header -->
<header>
  <div class="logo">🏪 <span>VendorDigi</span> Agent</div>
  <div style="display:flex;align-items:center;gap:12px;">
    <div class="model-status">
      <div class="dot {{ 'offline' if not model_active else '' }}"></div>
      {{ 'IBM Granite Active' if model_active else 'Fallback Mode' }}
    </div>
    <div class="ibm-badge">IBM Granite</div>
  </div>
</header>

<!-- Hero -->
<div class="hero">
  <h1>🛒 Street Vendor Digitalization Agent</h1>
  <p>Powered by IBM Granite AI &amp; RAG — helping local hawkers and micro-entrepreneurs grow digitally, access credit, and boost visibility.</p>
  <div class="hero-chips">
    <span class="chip">📍 Hyperlocal SEO</span>
    <span class="chip">💳 UPI Setup</span>
    <span class="chip">🏛️ MSME Schemes</span>
    <span class="chip">🛒 ONDC Listing</span>
    <span class="chip">🌐 Local Languages</span>
    <span class="chip">📊 Pricing Tips</span>
  </div>
</div>

<div class="container">

  <!-- Info Tiles -->
  <div class="info-strip">
    <div class="info-tile">
      <div class="icon">💰</div>
      <div class="label">PM SVANidhi</div>
      <div class="sub">Loans up to ₹50,000</div>
    </div>
    <div class="info-tile">
      <div class="icon">📱</div>
      <div class="label">UPI Payments</div>
      <div class="sub">QR Code Setup in 5 min</div>
    </div>
    <div class="info-tile">
      <div class="icon">🗺️</div>
      <div class="label">Google Maps Listing</div>
      <div class="sub">Free local visibility</div>
    </div>
    <div class="info-tile">
      <div class="icon">🛍️</div>
      <div class="label">ONDC / Meesho</div>
      <div class="sub">0% commission online sales</div>
    </div>
  </div>

  <!-- Query Box -->
  <div class="query-card">
    <h2>💬 Tell us about your business</h2>
    <div class="input-row">
      <textarea id="vendor-query" placeholder="e.g. I sell fruit in Pune's Camp area and want to grow my business digitally..."></textarea>
      <div style="display:flex;flex-direction:column;gap:8px;">
        <select class="lang-select" id="language-select">
          <option value="English">🇬🇧 English</option>
          <option value="Hindi">🇮🇳 हिंदी</option>
          <option value="Marathi">मराठी</option>
          <option value="Tamil">தமிழ்</option>
          <option value="Telugu">తెలుగు</option>
          <option value="Kannada">ಕನ್ನಡ</option>
          <option value="Bengali">বাংলা</option>
          <option value="Gujarati">ગુજરાતી</option>
        </select>
        <button class="btn-ask" onclick="askAgent()" id="ask-btn">Ask Agent →</button>
      </div>
    </div>

    <div class="examples">
      <p>💡 Try these examples:</p>
      <div class="example-pills">
        <span class="pill" onclick="setQuery(this)">I sell fruit in Pune's Camp area</span>
        <span class="pill" onclick="setQuery(this)">I run a chai stall in Mumbai Dharavi</span>
        <span class="pill" onclick="setQuery(this)">Vegetable vendor in Delhi Sarojini Nagar</span>
        <span class="pill" onclick="setQuery(this)">Fish seller in Chennai T Nagar market</span>
        <span class="pill" onclick="setQuery(this)">Flower vendor in Bangalore Commercial Street</span>
        <span class="pill" onclick="setQuery(this)">I need a loan for my food stall in Hyderabad</span>
      </div>
    </div>
  </div>

  <!-- Loading -->
  <div class="spinner" id="spinner">
    <div class="spinner-ring"></div>
    Analyzing your business and retrieving best digital strategies...
  </div>

  <!-- Response Area -->
  <div id="response-area">
    <div class="response-card" id="ai-response-card">
      <h3>🤖 Agent Recommendation</h3>
      <div class="response-text" id="ai-response-text"></div>
    </div>
    <div id="profile-card-html"></div>
  </div>

  <!-- Static Schemes Reference -->
  <div style="margin-top:8px;">
    <h2 style="font-size:16px;font-weight:700;color:#1f2937;margin-bottom:14px;">🏛️ Key Government Schemes</h2>
    <div class="schemes-grid">
      <div class="scheme-card">
        <div class="s-name">PM SVANidhi</div>
        <div class="s-amount">₹10,000 → ₹20,000 → ₹50,000</div>
        <div class="s-desc">Collateral-free micro loans for street vendors. Digital transactions earn ₹1,200 cashback/year.</div>
        <a href="https://pmsvanidhi.mohua.gov.in" target="_blank">pmsvanidhi.mohua.gov.in →</a>
      </div>
      <div class="scheme-card" style="border-left-color:#059669;">
        <div class="s-name">MUDRA Yojana (Shishu)</div>
        <div class="s-amount">Up to ₹50,000</div>
        <div class="s-desc">Micro loans for non-farm enterprises. No collateral. Low interest rates for micro-businesses.</div>
        <a href="https://mudra.org.in" target="_blank">mudra.org.in →</a>
      </div>
      <div class="scheme-card" style="border-left-color:#7c3aed;">
        <div class="s-name">Udyam (MSME) Registration</div>
        <div class="s-amount">Free Registration</div>
        <div class="s-desc">Free online MSME registration via Aadhaar. Unlocks bank credit, tax benefits, government tenders.</div>
        <a href="https://udyamregistration.gov.in" target="_blank">udyamregistration.gov.in →</a>
      </div>
      <div class="scheme-card" style="border-left-color:#f59e0b;">
        <div class="s-name">ONDC Network</div>
        <div class="s-amount">0% Commission</div>
        <div class="s-desc">Government-backed digital commerce network. Sell online via Meesho, Paytm, PhonePe.</div>
        <a href="https://ondc.org" target="_blank">ondc.org →</a>
      </div>
    </div>
  </div>

</div>

<footer>
  Built with IBM Granite AI &amp; RAG &nbsp;|&nbsp; Empowering Street Vendors Digitally &nbsp;|&nbsp; <strong>VendorDigi Agent</strong>
  <br><span style="color:#c4b5fd;">Made with IBM Bob</span>
</footer>

<script>
  function setQuery(el) {
    document.getElementById('vendor-query').value = el.textContent;
  }

  async function askAgent() {
    const query = document.getElementById('vendor-query').value.trim();
    const lang  = document.getElementById('language-select').value;
    if (!query) { alert('Please describe your business first!'); return; }

    document.getElementById('ask-btn').disabled = true;
    document.getElementById('spinner').style.display = 'block';
    document.getElementById('response-area').style.display = 'none';

    try {
      const res = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, language: lang })
      });
      const data = await res.json();

      document.getElementById('ai-response-text').textContent = data.response || 'No response received.';
      document.getElementById('profile-card-html').innerHTML = data.profile_card || '';
      document.getElementById('response-area').style.display = 'block';

      document.getElementById('response-area').scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (err) {
      alert('Error contacting agent: ' + err.message);
    } finally {
      document.getElementById('ask-btn').disabled = false;
      document.getElementById('spinner').style.display = 'none';
    }
  }

  // Allow Enter+Ctrl to submit
  document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('vendor-query').addEventListener('keydown', function(e) {
      if (e.ctrlKey && e.key === 'Enter') askAgent();
    });
  });
</script>

</body>
</html>
"""


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@app.route("/")
def index():
    return render_template_string(MAIN_PAGE, model_active=granite_model is not None)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True)
    query    = data.get("query", "").strip()
    language = data.get("language", "English")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    # Step 1 – Retrieve context from knowledge base (RAG retrieval)
    context = retrieve_context(query)

    # Step 2 – Generate response via IBM Granite or fallback
    if granite_model:
        prompt   = build_rag_prompt(query, context, language)
        response = generate_with_granite(granite_model, prompt)
        if not response:
            response = fallback_response(query, context)
    else:
        response = fallback_response(query, context)

    # Step 3 – Generate vendor profile card
    vendor_info  = extract_vendor_info(query)
    profile      = generate_vendor_profile(vendor_info)
    profile_card = profile_to_html_card(profile)

    return jsonify({
        "response":     response,
        "profile_card": profile_card,
        "vendor_info":  vendor_info,
        "model_used":   "IBM Granite" if granite_model else "Fallback (Rule-based RAG)"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "model":  "IBM Granite" if granite_model else "Fallback",
        "rag":    "active"
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    print(f"\n[*] Street Vendor Digitalization Agent running on http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
