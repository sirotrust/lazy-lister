import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types
import random

# --- 1. THE BRAIN & STATE ANCHOR ---
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'analysis': "",
        'listing_out': "",
        'photo_buffer': None
    }

if 'notes_input' not in st.session_state:
    st.session_state.notes_input = ""

try:
    google_client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("LEAD DEV: API Handshake Failed. Check secrets.toml.")

# --- 2. THE MASTER 50-TIP NEURAL LIBRARY (ZONE 1) ---
TIP_POOL = {
    "s1": ["Pro Tip: Use the rear-facing lens; it has 40% higher resolution.", "Pro Tip: Lock AE/AF Lock by holding the screen.", "Pro Tip: Natural window light between 10am-2pm is best.", "Pro Tip: Turn on gridlines for perfect leveling.", "Pro Tip: Move closer; never use digital zoom.", "Pro Tip: Clean your lens before every session.", "Pro Tip: Use white backgrounds for AI edge detection.", "Pro Tip: Shoot the care tag for fabric verification.", "Pro Tip: Use white board to reflect light into shadows.", "Pro Tip: Shoot shoes at a 45-degree hero angle."],
    "s2": ["Pro Tip: Place the Brand and Model in the first 3 words.", "Pro Tip: Use words like 'buttery' or 'structured' to sell the feel.", "Pro Tip: Mention 'Smoke-Free' to build buyer trust.", "Pro Tip: List Pit-to-pit, Length, and Sleeve measurements.", "Pro Tip: Use 'texture' keywords like 'slubby'.", "Pro Tip: Define the Vibe: Is it Gorpcore or Minimalist?", "Pro Tip: Find the model code on the internal tag.", "Pro Tip: Disclose pilling early to reduce returns.", "Pro Tip: Use 'Azure' or 'Cobalt' instead of just 'Blue'.", "Pro Tip: Mention hardware quality for premium items."],
    "s3": ["Pro Tip: Check 'Sold' listings, not 'Active' ones.", "Pro Tip: Price 10% high to allow for negotiations.", "Pro Tip: $24.99 converts 15% better than $25.00.", "Pro Tip: Weigh items before pricing for shipping.", "Pro Tip: Cross-reference eBay vs Poshmark for averages.", "Pro Tip: Free Shipping tags increase filter hits by 2x.", "Pro Tip: Price vintage on rarity, not just fashion.", "Pro Tip: Drop prices by 10% on Fridays for paydays.", "Pro Tip: High-demand brands follow strict MSRP logic.", "Pro Tip: High-quality photos justify a 20% price hike."],
    "s4": ["Pro Tip: Max out 80 characters in eBay titles.", "Pro Tip: Relist items every 30 days for 'New' status.", "Pro Tip: Share closet at 9PM EST for peak activity.", "Pro Tip: Use seasonal keywords like 'Summer Essential'.", "Pro Tip: Never use stock photos alone; AI flags them.", "Pro Tip: Put top 5 SEO tags in description footer.", "Pro Tip: Use 'Expert' style for tech listings.", "Pro Tip: Respond within 5 mins on FB Marketplace.", "Pro Tip: Send offers within 10 mins of a 'Like'.", "Pro Tip: Combine shipping to encourage multi-buys."],
    "s5": ["Expert Partner: This Thermal Printer pays for itself.", "Sourcing Secret: Scales prevent shipping surcharges.", "Visual Power: Kill 'Yellow Tint' with lighting kits.", "Boutique Standard: Matte-black mailers win fans.", "Speed Logic: Steamers remove wrinkles 3x faster.", "Professional Edge: Items on mannequins sell 20% faster.", "Mandatory Tool: Accurate measurements for SEO.", "Volume Strategy: Bulk 6-pack tape saves $12.", "Efficiency Pro: Clear bin storage keeps inventory searchable.", "The Pro Finish: Thermal 4x6 labels look corporate."]
}

# --- 3. THE ARCHITECTURAL LOCK (EXPANDED CSS) ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }
    .brand-word { color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .step-label { color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; margin-top: 30px; border-bottom: 4px solid #0F172A; display: inline-block; }
    .reminder-box { background-color: #FFFBEB !important; border-left: 6px solid #F59E0B !important; padding: 15px; border-radius: 12px; margin: 10px 0; }
    .suggestion-box { background-color: #F0F9FF !important; border-left: 6px solid #0EA5E9 !important; padding: 15px; border-radius: 12px; margin: 10px 0; }
    [data-testid="stTextArea"] textarea { background-color: #F8FAFC !important; color: #0F172A !important; font-weight: 600 !important; border: 2px solid #E2E8F0 !important; border-radius: 15px !important; }
    .stButton > button { border-radius: 12px !important; font-weight: 950 !important; text-transform: uppercase !important; height: 50px !important; }
    div[class*="st-key-clear_btn"] button { background-color: #F1F5F9 !important; color: #64748B !important; border: 2px solid #E2E8F0 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. THE JAVASCRIPT BRIDGE ---
st.markdown("""
    <script>
    const doc = window.parent.document;
    window.addEventListener('message', function(event) {
        if (event.data.type === 'trigger_platform') {
            const btns = Array.from(doc.querySelectorAll('button'));
            const target = btns.find(el => el.innerText.includes(event.data.key));
            if (target) target.click();
        }
    });
    </script>
""", unsafe_allow_html=True)

# --- 5. UI EXECUTION ---
st.markdown('<div style="margin-top:30px;"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text" style="font-size:18px;">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)

# STEP 1
st.markdown('<p class="step-label">STEP 1: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)
st.markdown(f'<div class="suggestion-box"><p style="font-size:14px; font-weight:600; margin:0;">{random.choice(TIP_POOL["s1"])}</p></div>', unsafe_allow_html=True)
img_file = st.camera_input("Scanner", label_visibility="collapsed")
if img_file: st.session_state.app_state['photo_buffer'] = img_file

# STEP 2
st.markdown('<p class="step-label">STEP 2: <span class="neon-text">DESCRIBE</span></p>', unsafe_allow_html=True)
st.markdown(f'<div class="reminder-box"><p style="font-size:14px; font-weight:600; margin:0;">{random.choice(TIP_POOL["s2"])}</p></div>', unsafe_allow_html=True)
notes = st.text_area("Notes", key="notes_input", height=100, label_visibility="collapsed")
if st.button("🗑️ CLEAR DESCRIPTION", key="clear_btn", use_container_width=True):
    st.session_state.update({"notes_input": ""})
    st.rerun()

# STEP 3: MARKET ANALYSIS + LINKS
st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
st.markdown(f'<div class="suggestion-box"><p style="font-size:14px; font-weight:600; margin:0;">{random.choice(TIP_POOL["s3"])}</p></div>', unsafe_allow_html=True)

# Analysis Button
analyze_html = """
<button onclick="parent.postMessage({type: 'trigger_platform', key: 'EXECUTE_AI'}, '*')" style="width: 100%; height: 70px; background-color: #CC0000; color: white; border: none; border-radius: 15px; font-weight: 950; font-size: 20px; text-transform: uppercase;">🚀 Analyze Market</button>
"""
components.html(analyze_html, height=85)

# THE 4 MARKET LINKS
market_links_html = f"""
<div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 8px;">
    <a href="https://www.ebay.com/sch/i.html?_nkw={st.session_state.notes_input}" target="_blank" style="height: 60px; background-color: #002F6C; color: white; text-decoration: none; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 11px;">EBAY</a>
    <a href="https://www.amazon.com/s?k={st.session_state.notes_input}" target="_blank" style="height: 60px; background-color: #483332; color: white; text-decoration: none; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 11px;">AMAZON</a>
    <a href="https://www.google.com/search?q={st.session_state.notes_input}" target="_blank" style="height: 60px; background-color: #CC0000; color: white; text-decoration: none; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 11px;">GOOGLE</a>
    <a href="https://poshmark.com/search?query={st.session_state.notes_input}" target="_blank" style="height: 60px; background-color: #8C1B2F; color: white; text-decoration: none; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 11px;">POSH</a>
</div>
"""
components.html(market_links_html, height=75)

if st.button("EXECUTE_AI", type="secondary"):
    if st.session_state.app_state['photo_buffer']:
        parts = [types.Part.from_text(text=f"Market analysis: {st.session_state.notes_input}"), types.Part.from_bytes(data=st.session_state.app_state['photo_buffer'].getvalue(), mime_type=st.session_state.app_state['photo_buffer'].type)]
        st.session_state.app_state['analysis'] = google_client.models.generate_content(model="gemini-2.0-flash-lite-preview-02-05", contents=parts).text

if st.session_state.app_state['analysis']: st.info(st.session_state.app_state['analysis'])

# STEP 4: LISTING PLATFORMS
st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
st.markdown(f'<div class="reminder-box"><p style="font-size:14px; font-weight:600; margin:0;">{random.choice(TIP_POOL["s4"])}</p></div>', unsafe_allow_html=True)

# THE 4 PLATFORM BUTTONS
platform_html = """
<div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 8px;">
    <button onclick="parent.postMessage({type: 'trigger_platform', key: 'PLAT_FB'}, '*')" style="height: 60px; background-color: #1877F2; color: white; border: none; border-radius: 10px; font-weight: 900; font-size: 11px;">FB</button>
    <button onclick="parent.postMessage({type: 'trigger_platform', key: 'PLAT_EBAY'}, '*')" style="height: 60px; background-color: #002F6C; color: white; border: none; border-radius: 10px; font-weight: 900; font-size: 11px;">EBAY</button>
    <button onclick="parent.postMessage({type: 'trigger_platform', key: 'PLAT_CL'}, '*')" style="height: 60px; background-color: #502189; color: white; border: none; border-radius: 10px; font-weight: 900; font-size: 11px;">CL</button>
    <button onclick="parent.postMessage({type: 'trigger_platform', key: 'PLAT_POSH'}, '*')" style="height: 60px; background-color: #8C1B2F; color: white; border: none; border-radius: 10px; font-weight: 900; font-size: 11px;">POSH</button>
</div>
"""
components.html(platform_html, height=75)

if st.button("PLAT_FB"): st.session_state.app_state['listing_out'] = f"FB: {st.session_state.notes_input}"
if st.button("PLAT_EBAY"): st.session_state.app_state['listing_out'] = f"eBay: {st.session_state.notes_input}"
if st.button("PLAT_CL"): st.session_state.app_state['listing_out'] = f"CL: {st.session_state.notes_input}"
if st.button("PLAT_POSH"): st.session_state.app_state['listing_out'] = f"Posh: {st.session_state.notes_input}"

st.text_area("Output", value=st.session_state.app_state['listing_out'], height=150, label_visibility="collapsed")

# STEP 5: PARTNER GRID
st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
st.markdown(f'<div class="suggestion-box"><p style="font-size:14px; font-weight:600; margin:0;">{random.choice(TIP_POOL["s5"])}</p></div>', unsafe_allow_html=True)

supply_html = """
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
    <a href="https://google.com" target="_blank" style="height: 60px; background-color: #CC0000; color: white; text-decoration: none; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-weight: 950; font-size: 14px;">🔍 GOOGLE SHOP</a>
    <a href="https://amazon.com" target="_blank" style="height: 60px; background-color: #483332; color: white; text-decoration: none; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-weight: 950; font-size: 14px;">🛡️ AMAZON PRO</a>
</div>
"""
components.html(supply_html, height=85)

if st.button("🔄 RESET ALL", key="reset_btn", use_container_width=True):
    st.session_state.app_state = {'analysis': "", 'listing_out': "", 'photo_buffer': None}
    st.session_state.update({"notes_input": ""})
    st.rerun()
