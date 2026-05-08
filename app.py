import streamlit as st
import pandas as pd
import urllib.parse
import random
import time
from datetime import datetime
from google import genai
from google.genai import types

# --- 1. THE ENGINE ROOM (SELF-HEALING & STATE) ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

# TIP LIBRARY (STATIC ROTATION)
TIP_LIBRARY = [
    "PRO TIP: Bright, natural light increases sales velocity by 30%.",
    "PRO TIP: Check 'Sold' listings on eBay for true market value.",
    "PRO TIP: SEO is king; use 'Pro' style for higher search rankings.",
    "PRO TIP: Mention flaws early to build buyer trust.",
    "PRO TIP: Consistent daily listings signal algorithms to boost your store."
]

if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'master_desc': "", 'listing_out': "", 'active_model': None,
        'supply_tips': "", 'session_tip': random.choice(TIP_LIBRARY)
    }

# DYNAMIC HANDSHAKE (Resolving 404 Errors)
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    if st.session_state.app_state['active_model'] is None:
        # Audit server for active Flash model identifiers
        available = [m.name for m in client.models.list() if "generateContent" in m.supported_actions]
        target = next((m for m in available if "flash" in m), "gemini-1.5-flash")
        st.session_state.app_state['active_model'] = target.replace("models/", "")
    LITE_MODEL = st.session_state.app_state['active_model']
except Exception as e:
    st.error(f"ENGINE ROOM ERROR: Handshake Failed. {str(e)}")

# --- 2. WHITE MASTERPIECE UI (CSS LOCK) ---
st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }

    /* LABEL & TEXT VISIBILITY */
    [data-testid="stRadio"] label, [data-testid="stRadio"] label p, [data-testid="stWidgetLabel"] p {
        color: #0F172A !important; font-weight: 800 !important; opacity: 1 !important;
    }
    [data-testid="stTextArea"] textarea {
        background-color: #F1F5F9 !important; color: #0F172A !important; font-weight: 600 !important; border: 2px solid #CBD5E1 !important;
    }

    /* BRANDING & SEQUENTIAL STEPS */
    .brand-word { color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .step-label { color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; margin-top: 30px; border-bottom: 4px solid #0F172A; display: inline-block; }
    .onboarding { color: #475569; font-weight: 600; font-size: 14px; margin: 15px 0; border-left: 4px solid #CBD5E1; padding-left: 10px; }
    .pro-tip { color: #64748B; font-size: 13px; font-weight: 700; margin-bottom: 10px; font-style: italic; }

    /* BUTTON GRID & BRAND COLORS */
    .flex-grid { display: flex; flex-wrap: nowrap; gap: 8px; width: 100%; margin: 10px 0; }
    .m-btn {
        flex: 1; height: 60px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
        text-decoration: none; color: #FFFFFF !important; font-weight: 950; font-size: 11px; text-transform: uppercase; border: none;
    }
    #ebay-blue { background-color: #002F6C !important; }
    #amz-brown { background-color: #483332 !important; }
    #google-red { background-color: #CC0000 !important; }
    #posh-maroon { background-color: #8C1B2F !important; }
    #fb-blue { background-color: #1877F2 !important; }
    #cl-purple { background-color: #502189 !important; }
    #viral-neon { background: linear-gradient(45deg, #22d3ee, #002F6C); font-size: 13px; font-weight: 950; color: #FFFFFF !important; cursor: pointer; }

    /* SIDEBAR & GHOST TRACE */
    [data-testid="stSidebar"] { border-left: 1px solid #E2E8F0; background-color: #F8FAFC !important; }
    div.stButton > button[kind="secondary"] { position: fixed; top: -500px; opacity: 0; pointer-events: none; }
    </style>
""", unsafe_allow_html=True)

# --- 3. THE JS OMNI-SHARE BRIDGE ---
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
    if (e.target.id === 'cl-trig') trigger('GHOST_CL');
    if (e.target.id === 'posh-trig') trigger('GHOST_POSH');
});
</script>
""", height=0)

# --- 4. THE 6-STEP FLOW ---
st.markdown('<div style="margin-top:30px;"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text" style="font-size:18px;">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)
st.markdown('<div class="onboarding">Scan ➜ Analyze ➜ Price ➜ List ➜ Supplies ➜ Log & Share</div>', unsafe_allow_html=True)

# STEP 1: SCAN (WITH AUTO-PURGE)
st.markdown('<p class="step-label">STEP 1: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)
st.markdown(f'<p class="pro-tip">{st.session_state.app_state["session_tip"]}</p>', unsafe_allow_html=True)

if 'hero_shot' not in st.session_state:
    img_file = st.camera_input("Scanner", label_visibility="collapsed")
    if img_file:
        st.session_state.hero_shot = img_file.getvalue()
        st.session_state.img_type = img_file.type
        st.rerun()
else:
    st.image(st.session_state.hero_shot, use_container_width=True)
    if st.button("📸 NEW SCAN (PURGE PREVIOUS)", use_container_width=True):
        # AUTO-PURGE: Reset sandbox without crashing widgets
        del st.session_state.hero_shot
        st.session_state.app_state['master_desc'] = ""
        st.session_state.app_state['listing_out'] = ""
        st.session_state.app_state['supply_tips'] = ""
        st.session_state.app_state['session_tip'] = random.choice(TIP_LIBRARY)
        st.rerun()

# STEP 2: DESCRIBE & ANALYZE
st.markdown('<p class="step-label">STEP 2: <span class="neon-text">ANALYZE</span></p>', unsafe_allow_html=True)
notes = st.text_area("Notes", height=100, placeholder="Brand, Condition, Flaws...", label_visibility="collapsed")

if st.button("🚀 RUN BRAIN ANALYSIS", type="primary", use_container_width=True):
    if 'hero_shot' in st.session_state:
        with st.spinner("AI Dissecting..."):
            try:
                part = types.Part.from_bytes(data=st.session_state.hero_shot, mime_type=st.session_state.img_type)
                res = client.models.generate_content(model=LITE_MODEL, contents=[f"Analyze image + notes: {notes}. Provide a 5-word title.", part])
                st.session_state.app_state['master_desc'] = res.text
                # Step 5 Logic: Intelligence-Aware Supply Suggestion
                sup_res = client.models.generate_content(model=LITE_MODEL, contents=[f"Suggest 2 specific packing items for: {res.text}"])
                st.session_state.app_state['supply_tips'] = sup_res.text
                st.rerun()
            except Exception as e:
                if "503" in str(e): # Handle High Demand Spike
                    st.warning("Brain is busy. Retrying in 2 seconds...")
                    time.sleep(2)
                    st.rerun()
                st.error(f"Analysis Failed: {str(e)}")

# STEP 3: PRICE (MARGIN MASTER)
st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
if st.session_state.app_state['master_desc']: st.info(f"**ID:** {st.session_state.app_state['master_desc']}")

search_q = urllib.parse.quote(st.session_state.app_state['master_desc'] if st.session_state.app_state['master_desc'] else notes)
st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.ebay.com/sch/i.html?_nkw={search_q}&LH_Sold=1&LH_Complete=1" target="_blank" class="m-btn" id="ebay-blue">EBAY SOLD</a>
        <a href="https://www.google.com/search?q={search_q}+price" target="_blank" class="m-btn" id="google-red">GOOGLE</a>
        <a href="https://poshmark.com/search?query={search_q}" target="_blank" class="m-btn" id="posh-maroon">POSH</a>
    </div>
''', unsafe_allow_html=True)

# STEP 4: LIST (COMMITMENT GATE)
st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
style = st.radio("Style", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")
st.markdown(f'''
    <div class="flex-grid">
        <div class="m-btn" id="fb-blue" id="fb-trig">FB</div>
        <div class="m-btn" id="ebay-blue" id="ebay-trig">EBAY</div>
        <div class="m-btn" id="cl-purple" id="cl-trig">CL</div>
        <div class="m-btn" id="posh-maroon" id="posh-trig">POSH</div>
    </div>
''', unsafe_allow_html=True)
st.text_area("Output", value=st.session_state.app_state['listing_out'], height=150, label_visibility="collapsed")

# STEP 5: SUPPLIES (INTEL-AWARE)
st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
if st.session_state.app_state['supply_tips']: st.success(f"📦 BRAIN: {st.session_state.app_state['supply_tips']}")

# STEP 6: INVENTORY & VIRAL SHARE
st.markdown('<p class="step-label">STEP 6: <span class="neon-text">INVENTORY</span></p>', unsafe_allow_html=True)
if st.session_state.inventory:
    df = pd.DataFrame(st.session_state.inventory)
    st.table(df)
    # Viral Loop: Share My Haul
    st.markdown('<div class="m-btn" id="viral-neon">🚀 SHARE MY HAUL & SESSION STATS</div>', unsafe_allow_html=True)

# --- 5. SIDEBAR (ADS & GHOST ENGINE) ---
with st.sidebar:
    st.markdown("### 📢 AD SPACE")
    st.caption("Marketing Banners Here")
    
    def run_ghost(p):
        ctx = st.session_state.app_state['master_desc'] if st.session_state.app_state['master_desc'] else notes
        res = client.models.generate_content(model=LITE_MODEL, contents=[f"Write a {style} {p} listing: {ctx}"])
        st.session_state.app_state['listing_out'] = res.text
        # COMMITMENT GATE: Only log once an action is taken
        st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": ctx[:30], "Platform": p})

    if st.button("GHOST_FB"): run_ghost("Facebook")
    if st.button("GHOST_EBAY"): run_ghost("eBay")
    if st.button("GHOST_CL"): run_ghost("Craigslist")
    if st.button("GHOST_POSH"): run_ghost("Poshmark")
