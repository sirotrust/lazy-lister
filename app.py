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

# Google Client Handshake
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    LITE_MODEL = "gemini-2.0-flash-lite-preview"
except Exception:
    st.error("LEAD DEV: API Handshake Failed.")

# --- 2. THE MASTERPIECE CSS (RESTORED 1-FOR-1) ---
st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }

    /* ZONE 1: RADIO & LABEL VISIBILITY */
    [data-testid="stRadio"] label, [data-testid="stRadio"] label p, [data-testid="stWidgetLabel"] p {
        color: #0F172A !important; font-weight: 800 !important; opacity: 1 !important;
    }

    /* ZONE 2: TABLE CONTRAST */
    [data-testid="stTable"] td, [data-testid="stTable"] th {
        color: #0F172A !important; background-color: #F8FAFC !important; font-weight: 600 !important; border: 1px solid #E2E8F0 !important;
    }

    /* ZONE 3: TEXT INPUTS */
    [data-testid="stTextArea"] textarea {
        background-color: #F1F5F9 !important; color: #0F172A !important; -webkit-text-fill-color: #0F172A !important;
        font-weight: 600 !important; border: 2px solid #CBD5E1 !important; border-radius: 12px !important;
    }

    /* ZONE 4: BRANDING */
    .brand-word { color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .step-label { color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; margin-top: 30px; border-bottom: 4px solid #0F172A; display: inline-block; }

    /* ZONE 5: BUTTON GRID LOCK & IDs */
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
    
    /* GHOST TRIGGER STYLING (HIDDEN AT BOTTOM) */
    div.stButton > button[kind="secondary"] {
        position: fixed; bottom: -100px; left: 0; width: 1px !important; height: 1px !important; opacity: 0 !important; pointer-events: none;
    }
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
    // Intercept clicks on original HTML IDs to fire Ghost Triggers
    if (e.target.id === 'fb-blue') trigger('GHOST_FB');
    if (e.target.id === 'ebay-blue') trigger('GHOST_EBAY');
    if (e.target.id === 'cl-purple') trigger('GHOST_CL');
    if (e.target.id === 'posh-maroon') trigger('GHOST_POSH');
});
</script>
""", height=0)

# --- 4. UI EXECUTION (RESTORED MASTERPIECE) ---
st.markdown('<div style="margin-top:30px;"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text" style="font-size:18px;">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)

# STEP 1: SCAN (Battery Release Logic)
st.markdown('<p class="step-label">STEP 1: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)
if 'hero_shot' not in st.session_state:
    img_file = st.camera_input("Scanner", label_visibility="collapsed")
    if img_file:
        st.session_state.hero_shot = img_file.getvalue()
        st.session_state.img_type = img_file.type
        st.rerun()
else:
    # Camera is now released; show preview only
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
            # Data Transformer for Google API
            part = types.Part.from_bytes(data=st.session_state.hero_shot, mime_type=st.session_state.img_type)
            response = client.models.generate_content(model=LITE_MODEL, contents=[notes, part])
            st.session_state.app_state['analysis'] = response.text

if st.session_state.app_state['analysis']:
    st.info(st.session_state.app_state['analysis'])

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
style_choice = st.radio("Style", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")
st.session_state.app_state['style'] = style_choice

st.markdown(f'''
    <div class="flex-grid">
        <a href="#" class="m-btn" id="fb-blue">FB</a>
        <a href="#" class="m-btn" id="ebay-blue">EBAY</a>
        <a href="#" class="m-btn" id="cl-purple">CL</a>
        <a href="#" class="m-btn" id="posh-maroon">POSH</a>
    </div>
''', unsafe_allow_html=True)

st.text_area("Output", value=st.session_state.app_state['listing_out'], height=150, label_visibility="collapsed")

# --- 5. THE GHOST TRIGGERS (REMOTE) ---
def run_ghost(p):
    with st.spinner(f"Writing {p} Listing..."):
        prompt = f"Write a {st.session_state.app_state['style']} {p} listing based on these notes: {notes}"
        res = client.models.generate_content(model=LITE_MODEL, contents=[prompt])
        st.session_state.app_state['listing_out'] = res.text
        st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": notes[:30], "Platform": p})

if st.button("GHOST_FB", type="secondary"): run_ghost("Facebook")
if st.button("GHOST_EBAY", type="secondary"): run_ghost("eBay")
if st.button("GHOST_CL", type="secondary"): run_ghost("Craigslist")
if st.button("GHOST_POSH", type="secondary"): run_ghost("Poshmark")

# INVENTORY LOG
st.divider()
st.table(pd.DataFrame(st.session_state.inventory) if st.session_state.inventory else pd.DataFrame({"Item": ["Log Empty..."], "Platform": ["--"], "Date": ["--"]}))
