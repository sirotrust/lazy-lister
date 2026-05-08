import streamlit as st
import pandas as pd
import urllib.parse
import random
from datetime import datetime
from google import genai
from google.genai import types

# --- 1. ENGINE & DISCOVERY ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

TIP_LIBRARY = [
    "PRO TIP: Bright, natural light increases sales velocity by 30%.",
    "PRO TIP: Mention flaws early to build buyer trust.",
    "PRO TIP: Check 'Sold' listings for true market value.",
    "PRO TIP: 'Pro' style uses SEO keywords for higher ranking.",
    "PRO TIP: Neutral backgrounds keep focus on the item."
]

if 'inventory' not in st.session_state: st.session_state.inventory = []
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'master_desc': "", 'listing_out': "", 'active_model': None,
        'supply_intel': "", 'tip': random.choice(TIP_LIBRARY)
    }

try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    if st.session_state.app_state['active_model'] is None:
        avail = [m.name for m in client.models.list() if "generateContent" in m.supported_actions]
        target = next((m for m in avail if "1.5-flash" in m), "gemini-1.5-flash")
        st.session_state.app_state['active_model'] = target.replace("models/", "")
    LITE_MODEL = st.session_state.app_state['active_model']
except Exception as e:
    st.error(f"Brain Connection Failed: {str(e)}")

# --- 2. THE WHITE MASTERPIECE CSS ---
st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }

    /* STEP LABELS */
    .brand-word { color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .step-label { color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; margin-top: 30px; border-bottom: 4px solid #0F172A; display: inline-block; }
    .onboarding { color: #475569; font-weight: 600; font-size: 14px; margin: 15px 0; border-left: 4px solid #CBD5E1; padding-left: 10px; }
    .pro-tip { color: #64748B; font-size: 13px; font-weight: 700; margin-bottom: 10px; font-style: italic; }

    /* STEP 4 RADIO VISIBILITY FIX */
    [data-testid="stRadio"] > div { gap: 10px; }
    [data-testid="stRadio"] label {
        color: #0F172A !important; font-weight: 900 !important; background: #F1F5F9; 
        padding: 8px 15px; border-radius: 8px; border: 1px solid #CBD5E1;
    }

    /* TEXT AREA COLOR */
    [data-testid="stTextArea"] textarea {
        background-color: #F1F5F9 !important; color: #0F172A !important; font-weight: 600 !important; border: 2px solid #CBD5E1 !important; border-radius: 12px !important;
    }

    /* BUTTONS */
    .flex-grid { display: flex; flex-wrap: nowrap; gap: 8px; width: 100%; margin: 10px 0; }
    .m-btn {
        flex: 1; height: 60px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
        text-decoration: none; color: #FFFFFF !important; font-weight: 950; font-size: 12px; text-transform: uppercase; border: none;
        cursor: pointer; transition: 0.2s;
    }
    .m-btn:active { transform: scale(0.95); opacity: 0.8; }
    #fb-trig { background-color: #1877F2 !important; }
    #ebay-trig { background-color: #002F6C !important; }
    #cl-trig { background-color: #502189 !important; }
    #posh-trig { background-color: #8C1B2F !important; }
    #google-red { background-color: #CC0000 !important; }
    #amz-brown { background-color: #483332 !important; }
    #viral-neon { background: linear-gradient(45deg, #22d3ee, #002F6C); font-size: 14px; }

    /* HIDDEN SIDEBAR LOGIC */
    [data-testid="stSidebar"] { border-left: 1px solid #E2E8F0; background-color: #F8FAFC !important; }
    div.stButton > button[kind="secondary"] { position: fixed; top: -500px; opacity: 0; pointer-events: none; }
    </style>
""", unsafe_allow_html=True)

# --- 3. JS BRIDGE FIX (SINGLE ID) ---
st.components.v1.html("""
<script>
const doc = window.parent.document;
const trigger = (key) => {
    const btns = Array.from(doc.querySelectorAll('button'));
    const target = btns.find(el => el.innerText.includes(key));
    if (target) target.click();
};
doc.addEventListener('click', (e) => {
    if (e.target.id === 'fb-trig' || e.target.id === 'ebay-trig' || 
        e.target.id === 'cl-trig' || e.target.id === 'posh-trig') {
        trigger('GHOST_' + e.target.id.split('-')[0].toUpperCase());
    }
});
</script>
""", height=0)

# --- 4. 6-STEP UI ---
st.markdown('<div style="margin-top:30px;"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text" style="font-size:18px;">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)
st.markdown('<div class="onboarding">Scan ➜ Analyze ➜ Price ➜ List ➜ Supplies ➜ Log</div>', unsafe_allow_html=True)

# STEP 1: SCAN
st.markdown('<p class="step-label">STEP 1: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)
st.markdown(f'<p class="pro-tip">{st.session_state.app_state["tip"]}</p>', unsafe_allow_html=True)

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

# STEP 2: DESCRIBE & ANALYZE
st.markdown('<p class="step-label">STEP 2: <span class="neon-text">DESCRIBE</span></p>', unsafe_allow_html=True)
notes = st.text_area("Notes", height=80, placeholder="Brand, Size, Condition...", label_visibility="collapsed")

if st.button("🚀 ANALYZE", type="primary", use_container_width=True):
    if 'hero_shot' in st.session_state:
        with st.spinner("Brain Handshake..."):
            part = types.Part.from_bytes(data=st.session_state.hero_shot, mime_type=st.session_state.img_type)
            res = client.models.generate_content(model=LITE_MODEL, contents=[f"Analyze this image + notes: {notes}. Give a 5-word search title.", part])
            st.session_state.app_state['master_desc'] = res.text
            sup_res = client.models.generate_content(model=LITE_MODEL, contents=[f"Suggest 2 packing items for: {res.text}"])
            st.session_state.app_state['supply_intel'] = sup_res.text
            st.session_state.app_state['tip'] = random.choice(TIP_LIBRARY)
            st.rerun()

# STEP 3: PRICE
st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
if st.session_state.app_state['master_desc']: st.info(f"**ID:** {st.session_state.app_state['master_desc']}")

sq = urllib.parse.quote(st.session_state.app_state['master_desc'] if st.session_state.app_state['master_desc'] else notes)
st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.ebay.com/sch/i.html?_nkw={sq}&LH_Sold=1&LH_Complete=1" target="_blank" class="m-btn" id="ebay-trig" style="background:#002F6C !important;">EBAY SOLD</a>
        <a href="https://www.google.com/search?q={sq}+price" target="_blank" class="m-btn" id="google-red">GOOGLE</a>
        <a href="https://poshmark.com/search?query={sq}" target="_blank" class="m-btn" id="posh-trig" style="background:#8C1B2F !important;">POSH</a>
    </div>
''', unsafe_allow_html=True)

# STEP 4: LIST (FIXED RADIO & BRAIN RELAY)
st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
style = st.radio("Style", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")

st.markdown(f'''
    <div class="flex-grid">
        <div class="m-btn" id="fb-trig">FB</div>
        <div class="m-btn" id="ebay-trig">EBAY</div>
        <div class="m-btn" id="cl-trig">CL</div>
        <div class="m-btn" id="posh-trig">POSH</div>
    </div>
''', unsafe_allow_html=True)
st.text_area("Output", value=st.session_state.app_state['listing_out'], height=150, label_visibility="collapsed")

# STEP 5: SUPPLIES
st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
if st.session_state.app_state['supply_intel']: st.success(f"📦 BRAIN: {st.session_state.app_state['supply_intel']}")

# STEP 6: INVENTORY
st.markdown('<p class="step-label">STEP 6: <span class="neon-text">INVENTORY</span></p>', unsafe_allow_html=True)
if st.session_state.inventory:
    st.table(pd.DataFrame(st.session_state.inventory))
    if st.button("🚀 SHARE MY HAUL", use_container_width=True): pass

# --- 5. THE SIDEBAR (GHOST ENGINE) ---
with st.sidebar:
    st.caption("ENGINE ROOM")
    def run_ghost(p):
        st.session_state.app_state['listing_out'] = "🤖 AI IS WRITING YOUR LISTING..."
        ctx = st.session_state.app_state['master_desc'] if st.session_state.app_state['master_desc'] else notes
        res = client.models.generate_content(model=LITE_MODEL, contents=[f"Write a {style} {p} listing: {ctx}"])
        st.session_state.app_state['listing_out'] = res.text
        st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": ctx[:30], "Platform": p})

    if st.button("GHOST_FB"): run_ghost("Facebook Marketplace")
    if st.button("GHOST_EBAY"): run_ghost("eBay")
    if st.button("GHOST_CL"): run_ghost("Craigslist")
    if st.button("GHOST_POSH"): run_ghost("Poshmark")
