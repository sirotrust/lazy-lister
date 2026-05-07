import streamlit as st
import pandas as pd
import time
from google import genai

# --- 1. THE CONNECTION ENGINE ---
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("API Key not found. Check your secrets.toml.")

# --- 2. DYNAMIC CONTENT LIBRARY ---
# These will rotate every few seconds
PRO_TIPS = [
    "Branded mailers increase repeat buyer rates by 15%.",
    "Natural lighting between 10am-2pm yields the best photos.",
    "Cross-listing the same item on 3+ platforms doubles sell-through rate.",
    "Ship within 24 hours to boost your seller search ranking.",
    "Always include measurements in descriptions to reduce returns."
]

AI_STRATEGIES = [
    "Exporting weekly CSV data improves profit forecasting by 40%.",
    "AI-optimized titles with 60+ characters rank higher in SEO.",
    "Bundling slow-moving items can clear 25% more inventory monthly.",
    "Price items 5% higher on Poshmark to account for offer-negotiation.",
    "Use 'Expert' style for electronics to minimize technical inquiries."
]

# --- 3. THE ROTATION ENGINE ---
# Uses session state and time to pick a suggestion
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

def get_dynamic_content(content_list):
    # Rotates index every 7 seconds
    elapsed = int(time.time() - st.session_state.start_time)
    index = (elapsed // 7) % len(content_list)
    return content_list[index]

def clear_text_callback():
    st.session_state["notes_input"] = ""
    st.session_state["listing_out"] = ""

# --- 4. ARCHITECTURAL ENGINE (CSS) ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }
    [data-testid="stRadio"] label, [data-testid="stRadio"] label p, [data-testid="stWidgetLabel"] p {
        color: #0F172A !important; font-weight: 800 !important; opacity: 1 !important;
    }
    [data-testid="stTextArea"] textarea {
        background-color: #F1F5F9 !important; color: #000000 !important; 
        font-weight: 600 !important; border: 2px solid #CBD5E1 !important; border-radius: 12px !important;
    }
    .reminder-box { 
        background-color: #FFFBEB !important; border-left: 6px solid #F59E0B !important; 
        padding: 12px; border-radius: 12px; margin: 8px 0; border: 1px solid #FEF3C7;
    }
    .suggestion-box { 
        background-color: #F0F9FF !important; border-left: 6px solid #0EA5E9 !important; 
        padding: 12px; border-radius: 12px; margin: 8px 0; border: 1px solid #E0F2FE;
    }
    .tip-tag { font-weight: 900; font-size: 10px; text-transform: uppercase; display: block; margin-bottom: 2px; }
    .tip-text { color: #1E293B !important; font-size: 13px; font-weight: 600; line-height: 1.3; }
    .header-wrapper { margin-top: 20px; margin-bottom: 30px; }
    .brand-word { color: #0F172A; font-size: 55px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .step-label { color: #0F172A !important; font-weight: 950; font-size: 24px; text-transform: uppercase; margin-top: 20px; border-bottom: 3px solid #0F172A; display: inline-block; }
    .flex-grid { display: flex; flex-wrap: nowrap; gap: 8px; width: 100%; margin: 8px 0; }
    .m-btn {
        flex: 1 !important; height: 55px !important; border-radius: 12px !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        text-decoration: none !important; color: white !important; font-weight: 950 !important; font-size: 11px !important;
        text-transform: uppercase !important; line-height: 55px !important;
    }
    #google-red { background-color: #CC0000 !important; }
    #amz-brown { background-color: #483332 !important; }
    #ebay-blue { background-color: #002F6C !important; }
    #fb-blue { background-color: #1877F2 !important; }
    #cl-purple { background-color: #502189 !important; }
    #posh-maroon { background-color: #8C1B2F !important; }
    
    .stButton > button {
        border-radius: 12px !important; height: 55px !important; font-weight: 950 !important;
        text-transform: uppercase !important; border: none !important; color: white !important; width: 100% !important;
    }
    div[data-testid="column"]:nth-of-type(1) div[data-testid="stButton"] button { background-color: #1877F2 !important; }
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"] button { background-color: #002F6C !important; }
    div[data-testid="column"]:nth-of-type(3) div[data-testid="stButton"] button { background-color: #502189 !important; }
    div[data-testid="column"]:nth-of-type(4) div[data-testid="stButton"] button { background-color: #8C1B2F !important; }
    </style>
""", unsafe_allow_html=True)

# --- 5. UI LAYOUT ---
st.markdown(f'''<div class="header-wrapper"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text" style="font-size:16px;">PREMIUM RESELLER ASSISTANT</span></div>''', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    # STEP 1
    st.markdown('<p class="step-label">STEP 1: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)
    st.markdown(f'''<div class="suggestion-box"><span class="tip-tag" style="color:#0EA5E9;">📦 PRO-TIP</span><p class="tip-text">{get_dynamic_content(PRO_TIPS)}</p></div>''', unsafe_allow_html=True)
    st.camera_input("Scanner", label_visibility="collapsed")
    
    # STEP 2
    st.markdown('<p class="step-label">STEP 2: <span class="neon-text">DESCRIBE</span></p>', unsafe_allow_html=True)
    st.markdown(f'''<div class="reminder-box"><span class="tip-tag" style="color:#F59E0B;">🧠 AI STRATEGY</span><p class="tip-text">{get_dynamic_content(AI_STRATEGIES)}</p></div>''', unsafe_allow_html=True)
    notes_input = st.text_area("Notes", placeholder="buttery, chunky, structured...", height=150, key="notes_input", label_visibility="collapsed")
    st.button("🗑️ CLEAR DESCRIPTION", use_container_width=True, on_click=clear_text_callback)

with col2:
    # STEP 3
    st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
    st.button("🚀 ANALYZE MARKET", type="primary", use_container_width=True)
    st.markdown(f'''<div class="flex-grid">
        <a href="https://www.ebay.com" target="_blank" class="m-btn" id="ebay-blue">EBAY</a>
        <a href="https://www.amazon.com" target="_blank" class="m-btn" id="amz-brown">AMAZON</a>
        <a href="https://www.google.com" target="_blank" class="m-btn" id="google-red">GOOGLE</a>
        <a href="https://poshmark.com" target="_blank" class="m-btn" id="posh-maroon">POSHMARK</a>
    </div>''', unsafe_allow_html=True)

    # STEP 4
    st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
    selected_style = st.radio("STYLE:", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")
    
    # STEP 4 DYNAMIC GRID
    p1, p2, p3, p4 = st.columns(4)
    if p1.button("FB"):
        # API Logic here
        pass
    if p2.button("EBAY"):
        pass
    if p3.button("CL"):
        pass
    if p4.button("POSH"):
        pass

    st.text_area("Output", height=150, key="output_area", label_visibility="collapsed")
    st.button("📋 COPY LISTING", use_container_width=True)

    # STEP 5
    st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
    st.markdown(f'''<div class="flex-grid">
        <a href="https://shopping.google.com" target="_blank" class="m-btn" id="google-red">GOOGLE SHOP</a>
        <a href="https://www.amazon.com" target="_blank" class="m-btn" id="amz-brown">AMAZON PRO</a>
    </div>''', unsafe_allow_html=True)

# FOOTER LOG
st.divider()
st.markdown('<p class="step-label">INVENTORY LOG</p>', unsafe_allow_html=True)
st.table(pd.DataFrame({"Item": ["Scanning..."], "Platform": ["Syncing"], "Price": ["--"]}))

if st.button("🗑️ RESET SESSION", use_container_width=True):
    st.session_state.clear(); st.rerun()
