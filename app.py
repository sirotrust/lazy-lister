import streamlit as st
from google import genai
from google.genai import types
import requests
import random

# --- 1. THE CONNECTION ENGINE ---
try:
    google_client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    OR_API_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception as e:
    st.error("Lead Dev: Check API Keys in secrets.toml.")

# --- 2. THE MASTER 50-TIP NEURAL LIBRARY (PROTECTED GLOBAL ASSET) ---
TIP_POOL = {
    "s1": [
        "Pro Tip: Use the rear-facing lens; it has 40% higher resolution than the selfie camera.",
        "Pro Tip: Lock your focus (AE/AF Lock) by holding the screen to prevent 'breathing' shots.",
        "Pro Tip: Natural window light between 10am-2pm yields the most color-accurate photos.",
        "Pro Tip: Turn on gridlines for perfect leveling.",
        "Pro Tip: Move closer; never use digital zoom.",
        "Pro Tip: Clean your lens with a microfiber cloth before every session.",
        "Pro Tip: Use white backgrounds to help the AI detect item edges instantly.",
        "Pro Tip: Capture a dedicated shot of the 'Care Tag' for fabric content.",
        "Pro Tip: Use a white poster board as a reflector to bounce light into shadows.",
        "Pro Tip: Shoot shoes at a 45-degree hero angle for the best presentation."
    ],
    "s2": [
        "Pro Tip: Place the Brand Name and Model in the first 3 words of your description.",
        "Pro Tip: Use sensory words like 'buttery,' 'chunky,' or 'structured' to sell the feel.",
        "Pro Tip: Mention 'Smoke-Free' or 'Pet-Free' status for buyer trust.",
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
        "Pro Tip: Free Shipping tags increase filter hits by 2x.",
        "Pro Tip: Price vintage based on decade and rarity, not just fashion.",
        "Pro Tip: Drop prices by 10% on Fridays when buyers receive paychecks.",
        "Pro Tip: High-demand brands follow very strict MSRP-based resale logic.",
        "Pro Tip: High-quality photos justify a 20% price hike."
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
        "Pro Tip: Send 'Offers to Likers' within 10 mins of a 'Like'."
    ],
    "s5": [
        "Expert Partner: Stop overpaying for ink. This Thermal Printer pays for itself. [View Setup]",
        "Sourcing Secret: Eliminate 'Underweight' surcharges with a precision scale. [Secure Yours]",
        "Visual Power: Kill 'Yellow Tint' in your photos with a curated lighting kit. [See My Set]",
        "Boutique Standard: Buyers notice quality mailers. Matte-black wins fans. [Shop Bulk]",
        "Speed Logic: Handheld fabric steamers remove wrinkles 3x faster than irons. [View Price]",
        "Professional Edge: Items on a mannequin sell 20% faster. [Check Forms]",
        "Mandatory Tool: Accurate measurements are mandatory for SEO. [See Pick]",
        "Volume Strategy: Bulk 6-pack shipping tape saves $12 monthly. [Stock Up Now]",
        "Efficiency Pro: Clear bin storage keeps inventory searchable. [Explore Bins]",
        "The Pro Finish: Thermal 4x6 labels give every package a corporate look. [Shop Labels]"
    ]
}

def get_random_tip(step_id):
    if f"tip_{step_id}" not in st.session_state:
        st.session_state[f"tip_{step_id}"] = random.choice(TIP_POOL[step_id])
    return st.session_state[f"tip_{step_id}"]

# --- 3. THE DUAL-ENGINE BRAIN ---
def call_the_brain(prompt, image=None):
    try:
        parts = [types.Part.from_text(text=prompt)]
        if image: parts.insert(0, types.Part.from_bytes(data=image.getvalue(), mime_type=image.type))
        # TARGETING FLASH-LITE FOR 1,000 REQ/DAY
        response = google_client.models.generate_content(model="gemini-2.0-flash-lite-preview-02-05", contents=parts)
        return response.text
    except Exception:
        try:
            headers = {"Authorization": f"Bearer {OR_API_KEY}"}
            payload = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=10)
            return res.json()['choices'][0]['message']['content']
        except: return "Connection lost. Retry."

# --- 4. THE ENGINEERING LOCK (AGGRESSIVE FLEX GEOMETRY) ---
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

    /* STEP 4: GEOMETRIC EQUALITY LOCK */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 8px !important;
        width: 100% !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        flex: 1 1 0% !important; /* Force identical growth/shrink and base */
        min-width: 0 !important;
        width: 25% !important;
    }

    /* BUTTONS: NUCLEAR OVERRIDE */
    .stButton > button { 
        border-radius: 12px !important; 
        height: 60px !important; 
        font-weight: 950 !important; 
        text-transform: uppercase !important; 
        color: #FFFFFF !important; 
        width: 100% !important; 
        border: none !important;
        display: block !important;
    }

    /* COLOR LOCK (DATA-TESTID SELECTOR) */
    div[class*="st-key-analyze_btn"] button { background-color: #CC0000 !important; }
    div[class*="st-key-fb_btn"] button { background-color: #1877F2 !important; }
    div[class*="st-key-ebay_btn"] button { background-color: #002F6C !important; }
    div[class*="st-key-cl_btn"] button { background-color: #502189 !important; }
    div[class*="st-key-posh_btn"] button { background-color: #8C1B2F !important; }
    div[class*="st-key-clear_btn"] button { background-color: #334155 !important; }
    div[class*="st-key-copy_btn"] button { background-color: #059669 !important; }
    div[class*="st-key-reset_btn"] button { background-color: #94A3B8 !important; }

    /* STEP 3 & 5: EXTERNAL GRID */
    .flex-grid { display: flex !important; flex-wrap: nowrap !important; gap: 8px !important; width: 100% !important; margin: 10px 0 !important; }
    .m-btn {
        flex: 1 !important; height: 60px !important; border-radius: 12px !important; display: flex !important; align-items: center !important; justify-content: center !important;
        text-decoration: none !important; color: #FFFFFF !important; font-weight: 950 !important; font-size: 11px !important; text-transform: uppercase !important;
    }
    .c-eb-blue { background-color: #002F6C !important; }
    .c-az-brown { background-color: #483332 !important; }
    .c-go-red { background-color: #CC0000 !important; }
    .c-pm-maroon { background-color: #8C1B2F !important; }

    [data-testid="stTextArea"] textarea { background-color: #F1F5F9 !important; color: #000000 !important; font-weight: 600 !important; border: 2px solid #CBD5E1 !important; border-radius: 12px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 5. UI LAYOUT ---
st.markdown('<div style="margin-top:30px;"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text" style="font-size:18px;">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)

# STEP 1
st.markdown('<p class="step-label">STEP 1: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)
st.markdown(f'<div class="suggestion-box"><span style="font-weight:950; font-size:11px; color:#0EA5E9;">📸 PRO TIP</span><p style="font-size:14px; font-weight:600; color:#1E293B; margin:0;">{get_random_tip("s1")}</p></div>', unsafe_allow_html=True)
img_file = st.camera_input("Scanner", label_visibility="collapsed")

# STEP 2
st.markdown('<p class="step-label">STEP 2: <span class="neon-text">DESCRIBE</span></p>', unsafe_allow_html=True)
st.markdown(f'<div class="reminder-box"><span style="font-weight:950; font-size:11px; color:#F59E0B;">📝 PRO TIP</span><p style="font-size:14px; font-weight:600; color:#1E293B; margin:0;">{get_random_tip("s2")}</p></div>', unsafe_allow_html=True)
notes = st.text_area("Notes", key="notes_input", height=150, placeholder="brand, size, condition...", label_visibility="collapsed")
st.button("🗑️ CLEAR DESCRIPTION", key="clear_btn", on_click=lambda: st.session_state.update({"notes_input": ""}))

# STEP 3
st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
st.markdown(f'<div class="suggestion-box"><span style="font-weight:950; font-size:11px; color:#0EA5E9;">💰 PRO TIP</span><p style="font-size:14px; font-weight:600; color:#1E293B; margin:0;">{get_random_tip("s3")}</p></div>', unsafe_allow_html=True)
if st.button("🚀 ANALYZE MARKET", key="analyze_btn"):
    st.session_state.market_analysis = call_the_brain(f"Analysis for: {notes}", img_file)

if st.session_state.get("market_analysis"): st.info(st.session_state.market_analysis)

st.markdown(f'''<div class="flex-grid">
    <a href="https://www.ebay.com/sch/i.html?_nkw={notes}" target="_blank" class="m-btn c-eb-blue">EBAY</a>
    <a href="https://www.amazon.com/s?k={notes}" target="_blank" class="m-btn c-az-brown">AMAZON</a>
    <a href="https://www.google.com/search?q={notes}" target="_blank" class="m-btn c-go-red">GOOGLE</a>
    <a href="https://poshmark.com/search?query={notes}" target="_blank" class="m-btn c-pm-maroon">POSHMARK</a>
</div>''', unsafe_allow_html=True)

# STEP 4
st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
st.markdown(f'<div class="reminder-box"><span style="font-weight:950; font-size:11px; color:#F59E0B;">🚀 PRO TIP</span><p style="font-size:14px; font-weight:600; color:#1E293B; margin:0;">{get_random_tip("s4")}</p></div>', unsafe_allow_html=True)
style = st.radio("Style", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")

# ABSOLUTE GEOMETRIC GRID
c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("📱 FB", key="fb_btn"): st.session_state.listing_out = call_the_brain(f"Write FB listing for: {notes}")
with c2: 
    if st.button("📦 EBAY", key="ebay_btn"): st.session_state.listing_out = call_the_brain(f"Write eBay listing for: {notes}")
with c3: 
    if st.button("🏘️ CL", key="cl_btn"): st.session_state.listing_out = call_the_brain(f"Write Craigslist listing for: {notes}")
with c4: 
    if st.button("👗 POSH", key="posh_btn"): st.session_state.listing_out = call_the_brain(f"Write Poshmark listing for: {notes}")

st.text_area("Output", value=st.session_state.get("listing_out", ""), height=150, label_visibility="collapsed")
st.button("📋 COPY LISTING", key="copy_btn")

# STEP 5
st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
st.markdown(f'<div class="suggestion-box"><span style="font-weight:950; font-size:11px; color:#0EA5E9;">🤝 YOUR PARTNER</span><p style="font-size:14px; font-weight:600; color:#1E293B; margin:0;">{get_random_tip("s5")}</p></div>', unsafe_allow_html=True)
st.markdown('''<div class="flex-grid">
    <a href="YOUR_LINK" target="_blank" class="m-btn c-go-red">🔍 GOOGLE SHOP</a>
    <a href="YOUR_LINK" target="_blank" class="m-btn c-az-brown">🛡️ AMAZON PRO</a>
</div>''', unsafe_allow_html=True)

st.button("🔄 RESET SESSION", key="reset_btn", on_click=lambda: st.session_state.clear())
