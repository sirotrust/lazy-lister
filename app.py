import streamlit as st
import pandas as pd
from google import genai
from google.genai import types
import random
import time

# --- 1. THE CONNECTION ENGINE ---
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("API Key not found. Check secrets.toml.")

# --- 2. THE MASTER 50-TIP PRO LIBRARY ---
TIP_POOL = {
    "s1": ["Pro Tip: Clean your lens with a microfiber cloth.", "Pro Tip: Shoot at a 45-degree angle.", "Pro Tip: Use Portrait Mode for focus."],
    "s2": ["Pro Tip: Brand + Model + Size in first 3 words.", "Pro Tip: Use sensory words like 'buttery'.", "Pro Tip: List measurements."],
    "s3": ["Pro Tip: Check Solds, then price 10% higher.", "Pro Tip: $24.99 beats $25.00 every time.", "Pro Tip: Free shipping gets 2x visibility."],
    "s4": ["Pro Tip: Relist every 30 days.", "Pro Tip: Use all 80 characters for SEO.", "Pro Tip: Share your closet at 9PM EST."],
    "s5": ["Helpful Suggestion: Thermal Printers pay for themselves.", "Efficiency Upgrade: Scales prevent shipping surcharges.", "Visual Advantage: Lighting kits kill yellow tints."]
}

def get_random_tip(step_id):
    return random.choice(TIP_POOL.get(step_id, ["Syncing..."]))

def analyze_market_logic(img_file, description):
    if not img_file and not description: return "Need data!"
    try:
        parts = [types.Part.from_text(text=f"Market analysis: {description}")]
        if img_file: parts.insert(0, types.Part.from_bytes(data=img_file.getvalue(), mime_type=img_file.type))
        return client.models.generate_content(model="gemini-2.0-flash", contents=parts).text
    except Exception as e: return f"Error: {e}"

def generate_listing(platform, details, style):
    try: return client.models.generate_content(model="gemini-2.0-flash", contents=f"Listing for {platform} ({style}): {details}").text
    except: return "Error generating listing."

def clear_text_callback():
    st.session_state["notes_input"] = ""; st.session_state["listing_out"] = ""

# --- 3. THE ARCHITECTURAL ENGINE (REINFORCED DESIGN LOCK) ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")
st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }

    /* STEP LABELS */
    .step-label { color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; margin-top: 30px; border-bottom: 3px solid #0F172A; display: inline-block; }
    .brand-word { color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }

    /* BOXES */
    .reminder-box, .suggestion-box { padding: 15px; border-radius: 12px; margin: 10px 0; border: 1px solid; }
    .reminder-box { background-color: #FFFBEB !important; border-left: 6px solid #F59E0B !important; border-color: #FEF3C7; }
    .suggestion-box { background-color: #F0F9FF !important; border-left: 6px solid #0EA5E9 !important; border-color: #E0F2FE; }
    .tip-tag { font-weight: 950; font-size: 11px; text-transform: uppercase; display: block; }
    .tip-text { color: #1E293B !important; font-size: 14px; font-weight: 600; }

    /* TEXT AREA */
    [data-testid="stTextArea"] textarea { background-color: #F1F5F9 !important; color: #000000 !important; font-weight: 600 !important; border: 2px solid #CBD5E1 !important; border-radius: 12px !important; }

    /* --- THE ULTIMATE BUTTON FIX --- */
    /* Forces all buttons to be the exact same size and removes white-out */
    .stButton > button {
        width: 100% !important;
        height: 60px !important;
        border-radius: 12px !important;
        font-weight: 950 !important;
        text-transform: uppercase !important;
        color: white !important;
        border: none !important;
        display: block !important;
    }

    /* Brute-force mapping company colors to button labels */
    div[data-testid="column"] button:has(div p:contains("FB")) { background-color: #1877F2 !important; }
    div[data-testid="column"] button:has(div p:contains("EBAY")) { background-color: #002F6C !important; }
    div[data-testid="column"] button:has(div p:contains("CL")) { background-color: #502189 !important; }
    div[data-testid="column"] button:has(div p:contains("POSH")) { background-color: #8C1B2F !important; }
    
    /* Hover states to prevent "White-Out" flickers */
    .stButton > button:hover { color: white !important; opacity: 0.9 !important; }
    .stButton > button:active { color: white !important; transform: scale(0.98) !important; }

    /* FLEX GRID FOR STEPS 3 & 5 (HTML LINKS) */
    .flex-grid { display: flex; flex-wrap: nowrap; gap: 8px; width: 100%; margin: 10px 0; }
    .m-btn {
        flex: 1 !important; height: 60px !important; border-radius: 12px !important; display: flex !important; align-items: center !important; justify-content: center !important;
        text-decoration: none !important; color: white !important; font-weight: 950 !important; font-size: 12px !important; text-transform: uppercase !important; text-align: center !important; line-height: 60px !important;
    }
    #ebay-blue { background-color: #002F6C !important; }
    #amz-brown { background-color: #483332 !important; }
    #google-red { background-color: #CC0000 !important; }
    #posh-maroon { background-color: #8C1B2F !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. UI LAYOUT ---
st.markdown('<div style="margin-top:30px;"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text" style="font-size:18px;">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<p class="step-label">STEP 1: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)
    st.markdown(f'<div class="suggestion-box"><span class="tip-tag" style="color:#0EA5E9;">📸 PRO TIP</span><p class="tip-text">{get_random_tip("s1")}</p></div>', unsafe_allow_html=True)
    img_file = st.camera_input("Scanner", label_visibility="collapsed")
    
    st.markdown('<p class="step-label">STEP 2: <span class="neon-text">DESCRIBE</span></p>', unsafe_allow_html=True)
    st.markdown(f'<div class="reminder-box"><span class="tip-tag" style="color:#F59E0B;">📝 PRO TIP</span><p class="tip-text">{get_random_tip("s2")}</p></div>', unsafe_allow_html=True)
    notes_input = st.text_area("Notes", placeholder="buttery, chunky, structured...", height=150, key="notes_input", label_visibility="collapsed")
    st.button("🗑️ CLEAR DESCRIPTION", use_container_width=True, on_click=clear_text_callback)

with col2:
    st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
    st.markdown(f'<div class="suggestion-box"><span class="tip-tag" style="color:#0EA5E9;">💰 PRO TIP</span><p class="tip-text">{get_random_tip("s3")}</p></div>', unsafe_allow_html=True)
    if st.button("🚀 ANALYZE MARKET", type="primary", use_container_width=True):
        st.session_state.market_analysis = analyze_market_logic(img_file, notes_input)
    if st.session_state.get("market_analysis"): st.info(st.session_state.market_analysis)

    st.markdown(f'''<div class="flex-grid">
        <a href="https://www.ebay.com/sch/i.html?_nkw={st.session_state.get('notes_input', '')}" target="_blank" class="m-btn" id="ebay-blue">EBAY</a>
        <a href="https://www.amazon.com/s?k={st.session_state.get('notes_input', '')}" target="_blank" class="m-btn" id="amz-brown">AMAZON</a>
        <a href="https://www.google.com/search?q={st.session_state.get('notes_input', '')}" target="_blank" class="m-btn" id="google-red">GOOGLE</a>
        <a href="https://poshmark.com/search?query={st.session_state.get('notes_input', '')}" target="_blank" class="m-btn" id="posh-maroon">POSHMARK</a>
    </div>''', unsafe_allow_html=True)

    st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
    st.markdown(f'<div class="reminder-box"><span class="tip-tag" style="color:#F59E0B;">🚀 PRO TIP</span><p class="tip-text">{get_random_tip("s4")}</p></div>', unsafe_allow_html=True)
    selected_style = st.radio("STYLE:", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")
    
    # STEP 4 BUTTONS (REINFORCED)
    p1, p2, p3, p4 = st.columns(4)
    with p1: st.button("FB", on_click=lambda: st.session_state.update({"listing_out": generate_listing("Facebook", notes_input, selected_style)}))
    with p2: st.button("EBAY", on_click=lambda: st.session_state.update({"listing_out": generate_listing("eBay", notes_input, selected_style)}))
    with p3: st.button("CL", on_click=lambda: st.session_state.update({"listing_out": generate_listing("Craigslist", notes_input, selected_style)}))
    with p4: st.button("POSH", on_click=lambda: st.session_state.update({"listing_out": generate_listing("Poshmark", notes_input, selected_style)}))
    
    st.text_area("Output", value=st.session_state.get('listing_out', ''), height=150, key="output_area", label_visibility="collapsed")
    st.button("📋 COPY LISTING", use_container_width=True)

    st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
    st.markdown(f'<div class="suggestion-box"><span class="tip-tag" style="color:#0EA5E9;">🤝 YOUR EXPERT PARTNER</span><p class="tip-text">{get_random_tip("s5")}</p></div>', unsafe_allow_html=True)
    st.markdown('''<div class="flex-grid">
        <a href="YOUR_GOOGLE_LINK" target="_blank" class="m-btn" id="google-red">GOOGLE SHOP</a>
        <a href="YOUR_AMAZON_LINK" target="_blank" class="m-btn" id="amz-brown">AMAZON PRO</a>
    </div>''', unsafe_allow_html=True)

if st.button("🗑️ RESET SESSION", use_container_width=True):
    st.session_state.clear(); st.rerun()
