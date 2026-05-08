import streamlit as st
import pandas as pd
import urllib.parse
import random
from datetime import datetime
from google import genai
from google.genai import types

# --- 1. ENGINE ROOM (SELF-HEALING & STATE) ---
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'master_desc': "", 'listing_out': "", 'active_model': None,
        'supply_intel': "", 'tip': "Scan an item to begin."
    }
if 'inventory' not in st.session_state:
    st.session_state.inventory = []

# CALLBACK: The only legal way to clear the text area without a crash 
def clear_text_callback():
    st.session_state.notes_input = ""
    st.session_state.app_state['listing_out'] = ""

# DYNAMIC HANDSHAKE (Fixed 404 Discovery) 
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    if st.session_state.app_state['active_model'] is None:
        # Audit: Explicitly searching for the supported model string
        models = [m.name for m in client.models.list() if "generateContent" in m.supported_actions]
        # Prefer the stable 1.5-flash identifier
        target = next((m for m in models if "gemini-1.5-flash" in m), "gemini-1.5-flash")
        st.session_state.app_state['active_model'] = target.replace("models/", "")
    LITE_MODEL = st.session_state.app_state['active_model']
except Exception as e:
    st.error(f"ENGINE ROOM ERROR: {str(e)}")

# --- 2. WHITE MASTERPIECE CSS (UI LOCK) ---
st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }
    
    /* RADIO VISIBILITY LOCK */
    [data-testid="stRadio"] label, [data-testid="stRadio"] label p {
        color: #0F172A !important; font-weight: 800 !important; opacity: 1 !important;
    }
    
    /* BRANDING & LABELS */
    .brand-word { color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .step-label { color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; margin-top: 30px; border-bottom: 4px solid #0F172A; display: inline-block; }
    
    /* BUTTON GRID */
    .flex-grid { display: flex; flex-wrap: nowrap; gap: 8px; width: 100%; margin: 10px 0; }
    .m-btn {
        flex: 1; height: 60px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
        text-decoration: none; color: #FFFFFF !important; font-weight: 950; font-size: 11px; text-transform: uppercase; border: none;
        cursor: pointer;
    }
    #ebay-blue { background-color: #002F6C !important; }
    #google-red { background-color: #CC0000 !important; }
    #posh-maroon { background-color: #8C1B2F !important; }
    #fb-blue { background-color: #1877F2 !important; }

    /* HIDE GHOST BUTTONS */
    div.stButton > button[kind="secondary"] { position: fixed; top: -500px; opacity: 0; pointer-events: none; }
    </style>
""", unsafe_allow_html=True)

# --- 3. JS BRIDGE ---
st.components.v1.html("""
<script>
const doc = window.parent.document;
const trigger = (key) => {
    const btns = Array.from(doc.querySelectorAll('button'));
    const target = btns.find(el => el.innerText.includes(key));
    if (target) target.click();
};
doc.addEventListener('click', (e) => {
    if (e.target.id === 'fb-trig') trigger('GHOST_FB');
    if (e.target.id === 'ebay-trig') trigger('GHOST_EBAY');
    if (e.target.id === 'posh-trig') trigger('GHOST_POSH');
});
</script>
""", height=0)

# --- 4. THE 6-STEP FLOW ---
st.markdown('<div style="margin-top:30px;"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text" style="font-size:18px;">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)

# STEP 1: SCAN
st.markdown('<p class="step-label">STEP 1: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)
img_file = st.camera_input("Scanner", label_visibility="collapsed")

# STEP 2: DESCRIBE & ANALYZE
st.markdown('<p class="step-label">STEP 2: <span class="neon-text">DESCRIBE</span></p>', unsafe_allow_html=True)
notes = st.text_area("Notes", key="notes_input", height=100, placeholder="Brand, Size, Condition...", label_visibility="collapsed")

col_a, col_b = st.columns(2)
with col_a:
    if st.button("🚀 ANALYZE", type="primary", use_container_width=True):
        if img_file:
            with st.spinner("Brain Handshake..."):
                part = types.Part.from_bytes(data=img_file.getvalue(), mime_type=img_file.type)
                res = client.models.generate_content(model=LITE_MODEL, contents=[f"Analyze: {notes}. Create a 5-word title.", part])
                st.session_state.app_state['master_desc'] = res.text
                sup_res = client.models.generate_content(model=LITE_MODEL, contents=[f"Suggest 2 packing items for: {res.text}"])
                st.session_state.app_state['supply_intel'] = sup_res.text
                st.rerun()
with col_b:
    st.button("🗑️ CLEAR", on_click=clear_text_callback, use_container_width=True)

# STEP 3: PRICE
st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
search_q = urllib.parse.quote(st.session_state.app_state['master_desc'] if st.session_state.app_state['master_desc'] else notes)
st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.ebay.com/sch/i.html?_nkw={search_q}&LH_Sold=1&LH_Complete=1" target="_blank" class="m-btn" id="ebay-blue">EBAY SOLD</a>
        <a href="https://www.google.com/search?q={search_q}+price" target="_blank" class="m-btn" id="google-red">GOOGLE</a>
        <a href="https://poshmark.com/search?query={search_q}" target="_blank" class="m-btn" id="posh-maroon">POSH</a>
    </div>
''', unsafe_allow_html=True)

# STEP 4: LIST (Omni-Share Enabled)
st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
style = st.radio("Style", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")
st.markdown(f'''
    <div class="flex-grid">
        <div class="m-btn" id="fb-blue" id="fb-trig">FB</div>
        <div class="m-btn" id="ebay-blue" id="ebay-trig">EBAY</div>
        <div class="m-btn" id="posh-maroon" id="posh-trig">POSH</div>
    </div>
''', unsafe_allow_html=True)
st.text_area("Output", value=st.session_state.app_state['listing_out'], height=150, label_visibility="collapsed")

# STEP 5: SUPPLIES (Brain Integrated)
st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
if st.session_state.app_state['supply_intel']: st.success(f"📦 BRAIN ADVICE: {st.session_state.app_state['supply_intel']}")

# STEP 6: INVENTORY
st.markdown('<p class="step-label">STEP 6: <span class="neon-text">INVENTORY</span></p>', unsafe_allow_html=True)
if st.session_state.inventory: st.table(pd.DataFrame(st.session_state.inventory))

# --- 5. SIDEBAR GHOSTS ---
with st.sidebar:
    def run_ghost(p):
        ctx = st.session_state.app_state['master_desc'] if st.session_state.app_state['master_desc'] else notes
        res = client.models.generate_content(model=LITE_MODEL, contents=[f"Write a {style} {p} listing: {ctx}"])
        st.session_state.app_state['listing_out'] = res.text
        st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": ctx[:30], "Platform": p})
    
    if st.button("GHOST_FB"): run_ghost("Facebook")
    if st.button("GHOST_EBAY"): run_ghost("eBay")
    if st.button("GHOST_POSH"): run_ghost("Poshmark")
