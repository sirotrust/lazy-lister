import streamlit as st
import pandas as pd
from google import genai
from google.genai import types
import random

# --- 1. THE CONNECTION ENGINE (THE BRAIN) ---
# This only wakes up when called by the Analysis or Listing functions
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("API Key not found. Check secrets.toml.")

# --- 2. THE MASTER 50-TIP NEURAL LIBRARY (LOCAL STORAGE) ---
# Zero Quota: These 50 tips live in your app memory, not the API.
TIP_POOL = {
    "s1": [
        "Pro Tip: Use the rear-facing lens; it has 40% higher resolution than the selfie camera.",
        "Pro Tip: Lock focus (AE/AF Lock) by holding the screen to prevent 'breathing' shots.",
        "Pro Tip: Natural window light between 10am-2pm yields the most color-accurate photos.",
        "Pro Tip: Turn on camera gridlines to ensure your products are perfectly level.",
        "Pro Tip: Physically move closer to the item; never use digital zoom.",
        "Pro Tip: Clean your lens with a microfiber cloth before every session.",
        "Pro Tip: Use white backgrounds to help the AI detect item edges instantly.",
        "Pro Tip: Capture a dedicated shot of the 'Care Tag' for fabric content.",
        "Pro Tip: Use a white poster board as a reflector to bounce light into shadows.",
        "Pro Tip: Shoot shoes at a 45-degree 'hero' angle for the best presentation."
    ],
    "s2": [
        "Pro Tip: Place the Brand Name and Model in the first 3 words of your description.",
        "Pro Tip: Use sensory words like 'buttery,' 'chunky,' or 'structured' to sell the feel.",
        "Pro Tip: Mention 'Smoke-Free' or 'Pet-Free' status for buyer confidence.",
        "Pro Tip: List three mandatory measurements: Pit-to-pit, Length, and Sleeve.",
        "Pro Tip: Use 'texture' keywords like 'slubby' or 'brushed' for SEO.",
        "Pro Tip: Describe the 'Vibe'—is it Gorpcore, Dark Academia, or Minimalist?",
        "Pro Tip: Find the model code on the internal tag for professional data.",
        "Pro Tip: Disclose pilling or fading early; it reduces return rates by 30%.",
        "Pro Tip: Be specific with colors; 'Cobalt' ranks better than just 'Blue'.",
        "Pro Tip: Mention 'Stitch Detail' or 'Quality Hardware' for premium pricing."
    ],
    "s3": [
        "Pro Tip: Check 'Sold' listings only; active prices are just 'wishes'.",
        "Pro Tip: Price 10-15% higher than average to allow room for negotiations.",
        "Pro Tip: Items at $24.99 sell significantly faster than flat $25.00.",
        "Pro Tip: Calculate shipping costs before pricing to protect margins.",
        "Pro Tip: Cross-reference eBay vs. Poshmark for a true market average.",
        "Pro Tip: Free Shipping tags increase listing visibility by over 2x.",
        "Pro Tip: Price vintage based on decade and rarity, not just fashion.",
        "Pro Tip: Drop prices by 10% on Fridays when buyers receive paychecks.",
        "Pro Tip: High-demand brands follow very strict MSRP-based resale logic.",
        "Pro Tip: High-quality photos allow you to price 20% higher than rivals."
    ],
    "s4": [
        "Pro Tip: Use all 80 characters in eBay titles; avoid empty space.",
        "Pro Tip: Relist items every 30 days to keep 'New Listing' status.",
        "Pro Tip: Share your Poshmark closet at 9PM EST during peak hours.",
        "Pro Tip: Include seasonal keywords like 'Summer Essential' for SEO.",
        "Pro Tip: Never use stock photos alone; platforms de-prioritize them.",
        "Pro Tip: Copy-paste your top 5 SEO tags into the description footer.",
        "Pro Tip: Offer 'Combined Shipping' to encourage multi-item orders.",
        "Pro Tip: Use 'Expert' style for tech to show technical knowledge.",
        "Pro Tip: On Facebook, respond within 5 mins to keep your 'Badge'.",
        "Pro Tip: Send 'Offers to Likers' within 10 mins to double conversion."
    ],
    "s5": [
        "Helpful Suggestion: Stop overpaying for ink. This Thermal Printer pays for itself in 3 months.",
        "Efficiency Upgrade: Eliminate 'Underweight' surcharges with a high-precision digital scale.",
        "Visual Advantage: Kill the 'Yellow Tint' in your photos with a curated lighting kit.",
        "Boutique Standard: Buyers notice quality mailers. These matte-black mailers earn repeat customers.",
        "Speed Strategy: Handheld fabric steamers remove wrinkles 3x faster than traditional irons.",
        "Reseller Essential: Items on a mannequin sell 20% faster than 'flat-lays.'",
        "Precision Tool: Accurate measurements are mandatory for SEO. Retractable tape is a must-have.",
        "Workflow Secret: Bulk 6-pack shipping tape saves $12 monthly over single-rolls.",
        "Organization Pro: Clear bin storage keeps inventory dust-free and searchable.",
        "Pro-Level Finish: Thermal 4x6 labels give every package a professional look."
    ]
}

def get_random_tip(step_id):
    """Pulls advice from local memory. Uses zero API tokens."""
    return random.choice(TIP_POOL.get(step_id, ["Synchronizing market intelligence..."]))

# --- 3. BRAIN LOGIC (API ACTIVE ONLY ON TAP) ---
def analyze_market_logic(img_file, description):
    if not img_file and not description: return "Need data!"
    try:
        content_parts = []
        if img_file:
            content_parts.append(types.Part.from_bytes(data=img_file.getvalue(), mime_type=img_file.type))
        prompt = "Expert Reseller Analysis. Provide: Value and SEO Keywords."
        content_parts.append(types.Part.from_text(text=prompt))
        return client.models.generate_content(model="gemini-2.0-flash", contents=content_parts).text
    except Exception as e:
        if "429" in str(e): return "Brain is resting. Try again in 60 seconds."
        return f"Brain Error: {str(e)}"

def generate_listing(platform, details, style):
    try:
        prompt = f"Write a {platform} listing in {style} style: {details}"
        return client.models.generate_content(model="gemini-2.0-flash", contents=prompt).text
    except: return "Brain connection lost. Retry."

# --- 4. THE ARCHITECTURAL ENGINE (UNIFIED HTML/CSS DESIGN LOCK) ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")
st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }
    .brand-word { color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .step-label { color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; margin-top: 30px; border-bottom: 3px solid #0F172A; display: inline-block; }
    .reminder-box, .suggestion-box { padding: 15px; border-radius: 12px; margin: 10px 0; border: 1px solid; }
    .reminder-box { background-color: #FFFBEB !important; border-left: 6px solid #F59E0B !important; border-color: #FEF3C7; }
    .suggestion-box { background-color: #F0F9FF !important; border-left: 6px solid #0EA5E9 !important; border-color: #E0F2FE; }
    .flex-grid { display: flex; flex-wrap: nowrap; gap: 8px; width: 100%; margin: 10px 0; }
    .m-btn {
        flex: 1 !important; height: 60px !important; border-radius: 12px !important; display: flex !important; align-items: center !important; justify-content: center !important;
        text-decoration: none !important; color: white !important; font-weight: 950 !important; font-size: 12px !important; text-transform: uppercase !important; line-height: 60px !important; border: none !important; cursor: pointer !important;
    }
    .fb-blue { background-color: #1877F2 !important; }
    .ebay-blue { background-color: #002F6C !important; }
    .cl-purple { background-color: #502189 !important; }
    .posh-maroon { background-color: #8C1B2F !important; }
    .google-red { background-color: #CC0000 !important; }
    .amz-brown { background-color: #483332 !important; }
    .utility-clear { background-color: #334155 !important; }
    .utility-copy { background-color: #059669 !important; }
    .utility-reset { background-color: #94A3B8 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 5. UI LAYOUT ---
st.markdown('<div style="margin-top:30px;"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text" style="font-size:18px;">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<p class="step-label">STEP 1: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)
    st.markdown(f'<div class="suggestion-box"><span class="tip-tag" style="color:#0EA5E9; font-weight:900; font-size:11px;">📸 PRO TIP</span><p class="tip-text" style="font-size:14px; font-weight:600; color:#1E293B;">{get_random_tip("s1")}</p></div>', unsafe_allow_html=True)
    img_file = st.camera_input("Scanner", label_visibility="collapsed")
    
    st.markdown('<p class="step-label">STEP 2: <span class="neon-text">DESCRIBE</span></p>', unsafe_allow_html=True)
    st.markdown(f'<div class="reminder-box"><span class="tip-tag" style="color:#F59E0B; font-weight:900; font-size:11px;">📝 PRO TIP</span><p class="tip-text" style="font-size:14px; font-weight:600; color:#1E293B;">{get_random_tip("s2")}</p></div>', unsafe_allow_html=True)
    notes_input = st.text_area("Notes", placeholder="buttery, chunky, structured...", height=150, key="notes_input", label_visibility="collapsed")
    
    st.markdown(f'<div class="flex-grid"><a href="/?action=clear" target="_self" class="m-btn utility-clear">🗑️ CLEAR DESCRIPTION</a></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
    st.markdown(f'<div class="suggestion-box"><span class="tip-tag" style="color:#0EA5E9; font-weight:900; font-size:11px;">💰 PRO TIP</span><p class="tip-text" style="font-size:14px; font-weight:600; color:#1E293B;">{get_random_tip("s3")}</p></div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="flex-grid"><a href="/?action=analyze" target="_self" class="m-btn google-red">🚀 ANALYZE MARKET</a></div>', unsafe_allow_html=True)
    if st.session_state.get("market_analysis"): st.info(st.session_state.market_analysis)

    st.markdown(f'''<div class="flex-grid">
        <a href="https://www.ebay.com/sch/i.html?_nkw={notes_input}" target="_blank" class="m-btn ebay-blue">EBAY</a>
        <a href="https://www.amazon.com/s?k={notes_input}" target="_blank" class="m-btn amz-brown">AMAZON</a>
        <a href="https://www.google.com/search?q={notes_input}" target="_blank" class="m-btn google-red">GOOGLE</a>
        <a href="https://poshmark.com/search?query={notes_input}" target="_blank" class="m-btn posh-maroon">POSHMARK</a>
    </div>''', unsafe_allow_html=True)

    st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
    st.markdown(f'<div class="reminder-box"><span class="tip-tag" style="color:#F59E0B; font-weight:900; font-size:11px;">🚀 PRO TIP</span><p class="tip-text" style="font-size:14px; font-weight:600; color:#1E293B;">{get_random_tip("s4")}</p></div>', unsafe_allow_html=True)
    selected_style = st.radio("STYLE:", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")
    
    st.markdown(f'''<div class="flex-grid">
        <a href="/?platform=Facebook" target="_self" class="m-btn fb-blue">📱 FB</a>
        <a href="/?platform=eBay" target="_self" class="m-btn ebay-blue">📦 EBAY</a>
        <a href="/?platform=Craigslist" target="_self" class="m-btn cl-purple">🏘️ CL</a>
        <a href="/?platform=Poshmark" target="_self" class="m-btn posh-maroon">👗 POSH</a>
    </div>''', unsafe_allow_html=True)

    st.text_area("Output", value=st.session_state.get('listing_out', ''), height=150, key="output_area", label_visibility="collapsed")
    st.markdown(f'<div class="flex-grid"><a href="/?action=copy" target="_self" class="m-btn utility-copy">📋 COPY LISTING</a></div>', unsafe_allow_html=True)

    st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
    st.markdown(f'<div class="suggestion-box"><span class="tip-tag" style="color:#0EA5E9; font-weight:900; font-size:11px;">🤝 YOUR PARTNER</span><p class="tip-text" style="font-size:14px; font-weight:600; color:#1E293B;">{get_random_tip("s5")}</p></div>', unsafe_allow_html=True)
    st.markdown('''<div class="flex-grid">
        <a href="YOUR_LINK" target="_blank" class="m-btn google-red">🔍 GOOGLE SHOP</a>
        <a href="YOUR_LINK" target="_blank" class="m-btn amz-brown">🛡️ AMAZON PRO</a>
    </div>''', unsafe_allow_html=True)

st.markdown(f'<div class="flex-grid" style="margin-top:50px;"><a href="/?action=reset" target="_self" class="m-btn utility-reset">🔄 RESET SESSION</a></div>', unsafe_allow_html=True)

# --- THE BRAIN BRIDGE ---
params = st.query_params
if "action" in params:
    act = params["action"]
    if act == "clear": st.session_state.notes_input = ""; st.rerun()
    if act == "analyze": st.session_state.market_analysis = analyze_market_logic(img_file, notes_input)
    if act == "reset": st.session_state.clear(); st.rerun()
    st.query_params.clear()

if "platform" in params:
    st.session_state.listing_out = generate_listing(params["platform"], notes_input, selected_style)
    st.query_params.clear()
