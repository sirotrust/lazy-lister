import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types
import random

# --- 1. THE BRAIN & STATE ANCHOR ---
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'analysis': "",
        'listing': "",
        'current_tip_s1': None,
        'current_tip_s2': None,
        'current_tip_s3': None,
        'current_tip_s4': None
    }

try:
    google_client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("Lead Dev: Google API Key missing in secrets.toml.")

# --- 2. NEURAL LIBRARY (HARD-CODED) ---
TIP_POOL = {
    "s1": "Pro Tip: Use the rear-facing lens; it has 40% higher resolution.",
    "s2": "Pro Tip: Place the Brand and Model in the first 3 words.",
    "s3": "Pro Tip: Check 'Sold' listings, not 'Active' ones.",
    "s4": "Pro Tip: Max out 80 characters in eBay titles.",
    "s5": "Sourcing Secret: Scales prevent shipping surcharges."
}

# --- 3. THE ARCHITECTURAL LOCK (UI DESIGN) ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }
    .brand-word { color: #0F172A; font-size: 50px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .step-label { color: #0F172A !important; font-weight: 950; font-size: 24px; text-transform: uppercase; margin-top: 25px; border-bottom: 3px solid #0F172A; display: inline-block; }
    .tip-box { background-color: #F0F9FF; border-left: 6px solid #0EA5E9; padding: 12px; border-radius: 8px; margin: 10px 0; color: #1E293B; font-weight: 600; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. THE JAVASCRIPT BRIDGE (THE "SILENT TRIGGER") ---
# This catches clicks from the HTML components and clicks hidden Streamlit buttons
st.markdown("""
    <script>
    const doc = window.parent.document;
    window.addEventListener('message', function(event) {
        if (event.data.type === 'trigger_ai') {
            const btns = Array.from(doc.querySelectorAll('button'));
            const target = btns.find(el => el.innerText.includes(event.data.key));
            if (target) target.click();
        }
    });
    </script>
""", unsafe_allow_html=True)

# --- 5. UI EXECUTION ---
st.markdown('<div style="margin-top:20px;"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text" style="font-size:16px;">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)

# STEP 1: SCAN
st.markdown('<p class="step-label">STEP 1: SCAN</p>', unsafe_allow_html=True)
st.markdown(f'<div class="tip-box">{TIP_POOL["s1"]}</div>', unsafe_allow_html=True)
img_file = st.camera_input("Scanner", label_visibility="collapsed")

# STEP 2: DESCRIBE
st.markdown('<p class="step-label">STEP 2: DESCRIBE</p>', unsafe_allow_html=True)
st.markdown(f'<div class="tip-box" style="background-color:#FFFBEB; border-color:#F59E0B;">{TIP_POOL["s2"]}</div>', unsafe_allow_html=True)
notes = st.text_area("Notes", height=100, placeholder="Brand, Size, Condition...", label_visibility="collapsed")

# STEP 3: PRICE (Isolated Analyze Button)
st.markdown('<p class="step-label">STEP 3: PRICE</p>', unsafe_allow_html=True)
st.markdown(f'<div class="tip-box">{TIP_POOL["s3"]}</div>', unsafe_allow_html=True)

analyze_component = """
<div style="display: flex; gap: 10px;">
    <button onclick="parent.postMessage({type: 'trigger_ai', key: 'RUN_ANALYSIS'}, '*')" 
    style="width: 100%; height: 60px; background-color: #CC0000; color: white; border: none; border-radius: 12px; font-weight: 900; font-size: 18px; cursor: pointer; text-transform: uppercase;">
    🚀 Analyze Market
    </button>
</div>
"""
components.html(analyze_component, height=70)

# Hidden logic triggered by Component
if st.button("RUN_ANALYSIS", list_visibility="hidden"):
    if img_file:
        parts = [types.Part.from_text(text=f"Market Analysis for: {notes}"), 
                 types.Part.from_bytes(data=img_file.getvalue(), mime_type=img_file.type)]
        res = google_client.models.generate_content(model="gemini-2.0-flash-lite-preview-02-05", contents=parts)
        st.session_state.app_state['analysis'] = res.text

if st.session_state.app_state['analysis']:
    st.info(st.session_state.app_state['analysis'])

# STEP 4: LIST (The "Hard Grid" Platform Buttons)
st.markdown('<p class="step-label">STEP 4: LIST</p>', unsafe_allow_html=True)
st.markdown(f'<div class="tip-box" style="background-color:#FFFBEB; border-color:#F59E0B;">{TIP_POOL["s4"]}</div>', unsafe_allow_html=True)

platform_component = """
<div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 8px;">
    <button onclick="parent.postMessage({type: 'trigger_ai', key: 'RUN_FB'}, '*')" style="height: 60px; background-color: #1877F2; color: white; border: none; border-radius: 10px; font-weight: 900; font-size: 12px;">FB</button>
    <button onclick="parent.postMessage({type: 'trigger_ai', key: 'RUN_EBAY'}, '*')" style="height: 60px; background-color: #002F6C; color: white; border: none; border-radius: 10px; font-weight: 900; font-size: 12px;">EBAY</button>
    <button onclick="parent.postMessage({type: 'trigger_ai', key: 'RUN_CL'}, '*')" style="height: 60px; background-color: #502189; color: white; border: none; border-radius: 10px; font-weight: 900; font-size: 12px;">CL</button>
    <button onclick="parent.postMessage({type: 'trigger_ai', key: 'RUN_POSH'}, '*')" style="height: 60px; background-color: #8C1B2F; color: white; border: none; border-radius: 10px; font-weight: 900; font-size: 12px;">POSH</button>
</div>
"""
components.html(platform_component, height=70)

# Hidden triggers for the platforms
if st.button("RUN_FB", list_visibility="hidden"):
    st.session_state.app_state['listing'] = f"FB LISTING: {notes}" # Replace with actual AI call
if st.button("RUN_EBAY", list_visibility="hidden"):
    st.session_state.app_state['listing'] = f"EBAY LISTING: {notes}"
    
st.text_area("Output", value=st.session_state.app_state['listing'], height=150, label_visibility="collapsed")

# STEP 5: SUPPLIES
st.markdown('<p class="step-label">STEP 5: SUPPLIES</p>', unsafe_allow_html=True)
supply_grid = """
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
    <a href="https://google.com" target="_blank" style="height: 50px; background-color: #CC0000; color: white; border-radius: 8px; text-decoration: none; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 12px;">🔍 GOOGLE SHOP</a>
    <a href="https://amazon.com" target="_blank" style="height: 50px; background-color: #483332; color: white; border-radius: 8px; text-decoration: none; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 12px;">🛡️ AMAZON PRO</a>
</div>
"""
components.html(supply_grid, height=70)

if st.button("🔄 RESET ALL", use_container_width=True):
    st.session_state.app_state = {'analysis': "", 'listing': ""}
    st.rerun()
