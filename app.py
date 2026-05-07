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

# --- 2. THE MASTER 50-TIP NEURAL LIBRARY (PROTECTED) ---
TIP_POOL = {
    "s1": ["Pro Tip: Use the rear-facing lens; it has 40% higher resolution.", "Pro Tip: Lock AE/AF Lock by holding the screen.", "Pro Tip: Natural window light between 10am-2pm is best.", "Pro Tip: Turn on gridlines for perfect leveling.", "Pro Tip: Move closer; never use digital zoom.", "Pro Tip: Clean your lens before every session.", "Pro Tip: Use white backgrounds for AI edge detection.", "Pro Tip: Shoot the care tag for fabric verification.", "Pro Tip: Use white board to reflect light into shadows.", "Pro Tip: Shoot shoes at a 45-degree hero angle."],
    "s2": ["Pro Tip: Place the Brand and Model in the first 3 words.", "Pro Tip: Use words like 'buttery' or 'structured' to sell the feel.", "Pro Tip: Mention 'Smoke-Free' to build buyer trust.", "Pro Tip: List Pit-to-pit, Length, and Sleeve measurements.", "Pro Tip: Use 'texture' keywords like 'slubby'.", "Pro Tip: Define the Vibe: Is it Gorpcore or Minimalist?", "Pro Tip: Find the model code on the internal tag.", "Pro Tip: Disclose pilling early to reduce returns.", "Pro Tip: Use 'Azure' or 'Cobalt' instead of just 'Blue'.", "Pro Tip: Mention hardware quality for premium items."],
    "s3": ["Pro Tip: Check 'Sold' listings, not 'Active' ones.", "Pro Tip: Price 10% high to allow for negotiations.", "Pro Tip: $24.99 converts 15% better than $25.00.", "Pro Tip: Weigh items before pricing for shipping.", "Pro Tip: Cross-reference eBay vs Poshmark for averages.", "Pro Tip: Free Shipping tags increase filter hits by 2x.", "Pro Tip: Price vintage on rarity, not just fashion.", "Pro Tip: Drop prices by 10% on Fridays for paydays.", "Pro Tip: High-demand brands follow strict MSRP logic.", "Pro Tip: High-quality photos justify a 20% price hike."],
    "s4": ["Pro Tip: Max out 80 characters in eBay titles.", "Pro Tip: Relist items every 30 days for 'New' status.", "Pro Tip: Share closet at 9PM EST for peak activity.", "Pro Tip: Use seasonal keywords like 'Summer Essential'.", "Pro Tip: Never use stock photos alone; AI flags them.", "Pro Tip: Put top 5 SEO tags in description footer.", "Pro Tip: Use 'Expert' style for tech listings.", "Pro Tip: Respond within 5 mins on FB Marketplace.", "Pro Tip: Send offers within 10 mins of a 'Like'.", "Pro Tip: Combine shipping to encourage multi-buys."],
    "s5": ["Expert Partner: This Thermal Printer pays for itself. [View Setup]", "Sourcing Secret: Scales prevent shipping surcharges. [Secure Yours]", "Visual Power: Kill 'Yellow Tint' with a curated lighting kit. [See My Set]", "Boutique Standard: Matte-black mailers win repeat fans. [Shop Bulk]", "Speed Logic: Steamers remove wrinkles 3x faster than irons. [View Price]", "Professional Edge: Items on a mannequin sell 20% faster. [Check Forms]", "Mandatory Tool: Accurate measurements are mandatory for SEO. [See Pick]", "Volume Strategy: Bulk 6-pack shipping tape saves $12 monthly. [Stock Up]", "Efficiency Pro: Clear bin storage keeps inventory searchable. [Explore Bins]", "The Pro Finish: Thermal 4x6 labels give every package a corporate look."]
}

def get_random_tip(step_id):
    if f"tip_{step_id}" not in st.session_state:
        st.session_state[f"tip_{step_id}"] = random.choice(TIP_POOL[step_id])
    return st.session_state[f"tip_{step_id}"]

def call_the_brain(prompt, image=None):
    try:
        parts = [types.Part.from_text(text=prompt)]
        if image: parts.insert(0, types.Part.from_bytes(data=image.getvalue(), mime_type=image.type))
        response = google_client.models.generate_content(model="gemini-2.0-flash-lite-preview-02-05", contents=parts)
        return response.text
    except Exception:
        try:
            headers = {"Authorization": f"Bearer {OR_API_KEY}"}
            payload = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=10)
            return res.json()['choices'][0]['message']['content']
        except: return "Service offline."

# --- 3. THE ENGINEERING LOCK (HARD-GRID) ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }
    .brand-word { color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .step-label { color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; margin-top: 30px; border-bottom: 3px solid #0F172A; display: inline-block; }
    
    /* SUGGESTION BOXES */
    .reminder-box, .suggestion-box { padding: 15px; border-radius: 12px; margin: 10px 0; border: 1px solid; }
    .reminder-box { background-color: #FFFBEB !important; border-left: 6px solid #F59E0B !important; border-color: #FEF3C7; }
    .suggestion-box { background-color: #F0F9FF !important; border-left: 6px solid #0EA5E9 !important; border-color: #E0F2FE; }

    /* HARD GRID LOCK FOR STEP 4 & LINKS */
    div[data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: 1fr 1fr 1fr 1fr !important; /* FORCED EQUALITY */
        gap: 8px !important;
    }
    div[data-testid="stHorizontalBlock"] > div {
        width: 100% !important;
        max-width: 100% !important;
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
    }
    
    /* COLORS (STRICT LOCK) */
    div[class*="st-key-analyze_btn"] button { background-color: #CC0000 !important; }
    div[class*="st-key-fb_btn"] button { background-color: #1877F2 !important; }
    div[class*="st-key-ebay_btn"] button { background-color: #002F6C !important; }
    div[class*="st-key-cl_btn"] button { background-color: #502189 !important; }
    div[class*="st-key-posh_btn"] button { background-color: #8C1B2F !important; }
    div[class*="st-key-clear_btn"] button { background-color: #334155 !important; }
    div[class*="st-key-copy_btn"] button { background-color: #059669 !important; }
    div[class*="st-key-reset_btn"] button { background-color: #94A3B8 !important; }

    /* STEP 3 & 5: LINK BUTTON GRID */
    .flex-grid { display: grid !important; grid-template-columns: 1fr 1fr 1fr 1fr !important; gap: 8px !important; width: 100% !important; margin: 10px 0 !important; }
    .m-btn {
        height: 60px !important; 
        border-radius: 12px !important; 
        display: flex !important; 
        align-items: center !important; 
        justify-content: center !important; 
        text-decoration: none !important; 
        color: #FFFFFF !important; 
        font-weight: 950 !important; 
        font-size: 11px !important; 
        text-transform: uppercase !important;
    }
    .c-ebay { background-color: #002F6C !important; }
    .c-amazon { background-color: #483332 !important; }
    .c-google { background-color: #CC0000 !important; }
    .c-posh { background-color: #8C1B2F !important; }

    [data-testid="stTextArea"] textarea { background-color: #F1F5F9 !important; color: #000000 !important; font-weight: 600 !important; border: 2px solid #CBD5E1 !important; border-radius: 12px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. UI EXECUTION ---
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
    <a href="https://www.ebay.com/sch/i.html?_nkw={notes}" target="_blank" class="m-btn c-ebay">EBAY</a>
    <a href="https://www.amazon.com/s?k={notes}" target="_blank" class="m-btn c-amazon">AMAZON</a>
    <a href="https://www.google.com/search?q={notes}" target="_blank" class="m-btn c-google">GOOGLE</a>
    <a href="https://poshmark.com/search?query={notes}" target="_blank" class="m-btn c-posh">POSHMARK</a>
</div>''', unsafe_allow_html=True)

# STEP 4
st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
st.markdown(f'<div class="reminder-box"><span style="font-weight:950; font-size:11px; color:#F59E0B;">🚀 PRO TIP</span><p style="font-size:14px; font-weight:600; color:#1E293B; margin:0;">{get_random_tip("s4")}</p></div>', unsafe_allow_html=True)
style = st.radio("Style", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")

# HARD GRID BUTTON ROW
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

# 2-COLUMN GRID FOR STEP 5
st.markdown(f'''<div class="flex-grid" style="grid-template-columns: 1fr 1fr !important;">
    <a href="YOUR_LINK" target="_blank" class="m-btn c-google">🔍 GOOGLE SHOP</a>
    <a href="YOUR_LINK" target="_blank" class="m-btn c-amazon">🛡️ AMAZON PRO</a>
</div>''', unsafe_allow_html=True)

st.button("🔄 RESET SESSION", key="reset_btn", on_click=lambda: st.session_state.clear())
