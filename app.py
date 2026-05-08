import streamlit as st
import pandas as pd
import random
from datetime import datetime
from google import genai
from google.genai import types

# --- 1. THE BRAIN & STATE ANCHOR ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'app_state' not in st.session_state:
    st.session_state.app_state = {'analysis': "", 'listing_out': "", 'style': "Pro"}

# Google Client Handshake (Final Stable Handshake)
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    # FIXED MODEL STRING TO PREVENT 404
    LITE_MODEL = "models/gemini-1.5-flash-latest"
except Exception:
    st.error("LEAD DEV: API Handshake Failed.")

# --- 2. MASTERPIECE CSS (RESTORATION FROM ARCH1) ---
st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }

    /* ZONE 1-4: STEP DESIGN */
    [data-testid="stRadio"] label, [data-testid="stRadio"] label p, [data-testid="stWidgetLabel"] p {
        color: #0F172A !important; font-weight: 800 !important; opacity: 1 !important;
    }
    [data-testid="stTable"] td, [data-testid="stTable"] th {
        color: #0F172A !important; background-color: #F8FAFC !important; font-weight: 600 !important; border: 1px solid #E2E8F0 !important;
    }
    [data-testid="stTextArea"] textarea {
        background-color: #F1F5F9 !important; color: #0F172A !important; font-weight: 600 !important; border: 2px solid #CBD5E1 !important; border-radius: 12px !important;
    }

    /* ZONE 5: BRANDING & BUTTONS */
    .brand-word { color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .step-label { color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; margin-top: 30px; border-bottom: 4px solid #0F172A; display: inline-block; }
    .flex-grid { display: flex; flex-wrap: nowrap; gap: 8px; width: 100%; margin: 10px 0; }
    .m-btn {
        flex: 1; height: 60px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
        text-decoration: none; color: #FFFFFF !important; font-weight: 950; font-size: 11px; text-transform: uppercase; border: none; cursor: pointer;
    }
    #ebay-blue { background-color: #002F6C !important; }
    #amz-brown { background-color: #483332 !important; }
    #google-red { background-color: #CC0000 !important; }
    #posh-maroon { background-color: #8C1B2F !important; }
    #fb-blue { background-color: #1877F2 !important; }
    #cl-purple { background-color: #502189 !important; }

    /* ZONE D: SIDEBAR HIDER (ENGINE ROOM) */
    [data-testid="stSidebar"] { display: none !important; }
    
    /* BUFFER ZONE SPACING */
    .buffer-box { margin: 100px 0; border-top: 1px solid #F1F5F9; border-bottom: 1px solid #F1F5F9; padding: 40px 0; }
    </style>
""", unsafe_allow_html=True)

# --- 3. THE JAVASCRIPT BRIDGE ---
st.components.v1.html("""
<script>
const doc = window.parent.document;
const trigger = (key) => {
    const btns = Array.from(doc.querySelectorAll('button'));
    const target = btns.find(el => el.innerText.includes(key));
    if (target) target.click();
};
doc.addEventListener('click', (e) => {
    if (e.target.id === 'fb-blue') trigger('GHOST_FB');
    if (e.target.id === 'ebay-blue') trigger('GHOST_EBAY');
    if (e.target.id === 'cl-purple') trigger('GHOST_CL');
    if (e.target.id === 'posh-maroon') trigger('GHOST_POSH');
});
</script>
""", height=0)

# --- 4. ZONE A & B: CORE WORK AREA ---
st.markdown('<div style="margin-top:30px;"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text" style="font-size:18px;">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)

# STEP 1: SCAN
st.markdown('<p class="step-label">STEP 1: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)
if 'hero_shot' not in st.session_state:
    img_file = st.camera_input("Scanner", label_visibility="collapsed")
    if img_file:
        st.session_state.hero_shot = img_file.getvalue()
        st.session_state.img_type = img_file.type
        st.rerun()
else:
    st.image(st.session_state.hero_shot, use_container_width=True)
    if st.button("📸 RETAKE PHOTO", use_container_width=True):
        del st.session_state.hero_shot
        st.rerun()

# STEP 2: DESCRIBE
st.markdown('<p class="step-label">STEP 2: <span class="neon-text">DESCRIBE</span></p>', unsafe_allow_html=True)
notes = st.text_area("Notes", key="notes_input", height=100, placeholder="Brand, Size, Condition...", label_visibility="collapsed")

# STEP 3: PRICE
st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
if st.button("🚀 ANALYZE MARKET", type="primary", use_container_width=True):
    if 'hero_shot' in st.session_state:
        with st.spinner("Brain Processing..."):
            part = types.Part.from_bytes(data=st.session_state.hero_shot, mime_type=st.session_state.img_type)
            response = client.models.generate_content(model=LITE_MODEL, contents=[notes, part])
            st.session_state.app_state['analysis'] = response.text
if st.session_state.app_state['analysis']: st.info(st.session_state.app_state['analysis'])

st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.ebay.com/sch/i.html?_nkw={notes}" target="_blank" class="m-btn" id="ebay-blue">EBAY</a>
        <a href="https://www.amazon.com/s?k={notes}" target="_blank" class="m-btn" id="amz-brown">AMAZON</a>
        <a href="https://www.google.com/search?q={notes}" target="_blank" class="m-btn" id="google-red">GOOGLE</a>
        <a href="https://poshmark.com/search?query={notes}" target="_blank" class="m-btn" id="posh-maroon">POSH</a>
    </div>
''', unsafe_allow_html=True)

# STEP 4: LIST
st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
style = st.radio("Style", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")
st.session_state.app_state['style'] = style

st.markdown(f'''
    <div class="flex-grid">
        <a href="#" class="m-btn" id="fb-blue">FB</a>
        <a href="#" class="m-btn" id="ebay-blue">EBAY</a>
        <a href="#" class="m-btn" id="cl-purple">CL</a>
        <a href="#" class="m-btn" id="posh-maroon">POSH</a>
    </div>
''', unsafe_allow_html=True)

st.text_area("Output", value=st.session_state.app_state['listing_out'], height=150, label_visibility="collapsed")

# STEP 5: SUPPLIES
st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
st.markdown('''
    <div class="flex-grid">
        <a href="https://google.com" target="_blank" class="m-btn" id="google-red">GOOGLE SHOP</a>
        <a href="https://amazon.com" target="_blank" class="m-btn" id="amz-brown">AMAZON PRO</a>
    </div>
''', unsafe_allow_html=True)

# --- 5. ZONE C: THE BUFFER ZONE (FUTURE AFFILIATES) ---
st.markdown('<div class="buffer-box">', unsafe_allow_html=True)
st.write("&nbsp;") 
st.write("&nbsp;")
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. ZONE D: INVENTORY LOG ---
st.divider()
st.table(pd.DataFrame(st.session_state.inventory) if st.session_state.inventory else pd.DataFrame({"Item": ["Log Ready..."], "Platform": ["--"], "Date": ["--"]}))

# --- 7. THE ENGINE ROOM (INVISIBLE SIDEBAR) ---
with st.sidebar:
    def run_ghost(p):
        with st.spinner(f"Writing {p}..."):
            res = client.models.generate_content(model=LITE_MODEL, contents=[f"Write a {st.session_state.app_state['style']} {p} listing: {notes}"])
            st.session_state.app_state['listing_out'] = res.text
            st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": notes[:30], "Platform": p})

    if st.button("GHOST_FB"): run_ghost("Facebook")
    if st.button("GHOST_EBAY"): run_ghost("eBay")
    if st.button("GHOST_CL"): run_ghost("Craigslist")
    if st.button("GHOST_POSH"): run_ghost("Poshmark")
