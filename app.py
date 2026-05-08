import streamlit as st
import pandas as pd
import urllib.parse
import random
from datetime import datetime
from google import genai
from google.genai import types

# --- 1. THE ENGINE ROOM (STABILITY & STATE) ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'master_id': "", 'listing_out': "", 'active_model': None,
        'supply_intel': "", 'is_pro': False 
    }

# Dynamic Handshake (Resolving 404 connection errors)
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    if st.session_state.app_state['active_model'] is None:
        avail = [m.name for m in client.models.list() if "generateContent" in m.supported_actions]
        target = next((m for m in avail if "flash" in m), "gemini-1.5-flash")
        st.session_state.app_state['active_model'] = target.replace("models/", "")
    LITE_MODEL = st.session_state.app_state['active_model']
except Exception as e:
    st.error(f"ENGINE ROOM: Connection Failure. {str(e)}")

# --- 2. WHITE MASTERPIECE UI (CSS LOCK) ---
st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }

    /* LABEL VISIBILITY LOCK */
    [data-testid="stRadio"] label, [data-testid="stRadio"] label p, [data-testid="stWidgetLabel"] p {
        color: #0F172A !important; font-weight: 800 !important; opacity: 1 !important;
    }
    [data-testid="stTextArea"] textarea {
        background-color: #F1F5F9 !important; color: #0F172A !important; font-weight: 600 !important; border: 2px solid #CBD5E1 !important;
    }

    /* BRANDING & SEQUENTIAL FLOW */
    .brand-word { color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .step-label { color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; margin-top: 30px; border-bottom: 4px solid #0F172A; display: inline-block; }
    .onboarding { color: #475569; font-weight: 600; font-size: 14px; margin: 15px 0; border-left: 4px solid #CBD5E1; padding-left: 10px; }

    /* BUTTON GRID & COLORS */
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
    #viral-neon { background: linear-gradient(45deg, #22d3ee, #002F6C); font-size: 14px; font-weight: 950; color: #FFFFFF !important; }

    /* HIDDEN GHOST CONTROLS */
    div.stButton > button[kind="secondary"] { position: fixed; top: -500px; opacity: 0; pointer-events: none; }
    [data-testid="stSidebar"] { border-left: 1px solid #E2E8F0; background-color: #F8FAFC !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. THE JS LIVE-WIRE BRIDGE ---
st.components.v1.html("""
<script>
const doc = window.parent.document;
const trigger = (platform) => {
    const btns = Array.from(doc.querySelectorAll('button'));
    const target = btns.find(el => el.innerText.includes('GHOST_' + platform));
    if (target) target.click();
};
doc.addEventListener('click', (e) => {
    const txt = e.target.innerText || "";
    if (txt === "FB") trigger("FB");
    if (txt === "EBAY") trigger("EBAY");
    if (txt === "POSH") trigger("POSH");
});
</script>
""", height=0)

# --- 4. THE 6-STEP FLOW ---
st.markdown('<div style="margin-top:30px;"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text" style="font-size:18px;">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)
st.markdown('<div class="onboarding">Scan ➜ Analyze ➜ Price ➜ List ➜ Supplies ➜ Log</div>', unsafe_allow_html=True)

# STEP 1: SCAN (AUTO-PURGE)
st.markdown('<p class="step-label">STEP 1: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)
if 'hero_shot' not in st.session_state:
    img_file = st.camera_input("Scanner", label_visibility="collapsed")
    if img_file:
        st.session_state.hero_shot = img_file.getvalue()
        st.session_state.img_type = img_file.type
        st.rerun()
else:
    st.image(st.session_state.hero_shot, use_container_width=True)
    if st.button("📸 NEW SCAN (AUTO-PURGE SANDBOX)", use_container_width=True):
        del st.session_state.hero_shot
        st.session_state.app_state['master_id'] = ""
        st.session_state.app_state['listing_out'] = ""
        st.session_state.app_state['supply_intel'] = ""
        st.rerun()

# STEP 2: ANALYZE (MASTER RELAY ANCHOR)
st.markdown('<p class="step-label">STEP 2: <span class="neon-text">ANALYZE</span></p>', unsafe_allow_html=True)
notes = st.text_area("Notes", height=100, placeholder="Condition, flaws, brand...", label_visibility="collapsed")

if st.button("🚀 RUN BRAIN ANALYSIS", type="primary", use_container_width=True):
    if 'hero_shot' in st.session_state:
        with st.spinner("Brain Mapping..."):
            part = types.Part.from_bytes(data=st.session_state.hero_shot, mime_type=st.session_state.img_type)
            res = client.models.generate_content(model=LITE_MODEL, contents=[f"Analyze: {notes}. Create 5-word title.", part])
            st.session_state.app_state['master_id'] = res.text
            # Pre-load Step 5 Intelligence
            sup_res = client.models.generate_content(model=LITE_MODEL, contents=[f"Suggest 2 packing items for: {res.text}"])
            st.session_state.app_state['supply_intel'] = sup_res.text
            st.rerun()

# STEP 3: PRICE (GOOGLE SHOPPING FIX)
st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
if st.session_state.app_state['master_id']: st.info(f"**AI ID:** {st.session_state.app_state['master_id']}")

search_q = urllib.parse.quote(st.session_state.app_state['master_id'] if st.session_state.app_state['master_id'] else notes)
st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.ebay.com/sch/i.html?_nkw={search_q}&LH_Sold=1&LH_Complete=1" target="_blank" class="m-btn" id="ebay-blue">EBAY SOLD</a>
        <a href="https://www.google.com/search?q={search_q}+price&tbm=shop" target="_blank" class="m-btn" id="google-red">GOOGLE SHOP</a>
        <a href="https://poshmark.com/search?query={search_q}" target="_blank" class="m-btn" id="posh-maroon">POSH</a>
    </div>
''', unsafe_allow_html=True)

# STEP 4: LIST (LIVE-WIRE CONNECTIVITY)
st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
style = st.radio("Style", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")
st.markdown(f'''
    <div class="flex-grid">
        <div class="m-btn" id="fb-blue">FB</div>
        <div class="m-btn" id="ebay-blue">EBAY</div>
        <div class="m-btn" id="posh-maroon">POSH</div>
    </div>
''', unsafe_allow_html=True)
st.text_area("Output", value=st.session_state.app_state['listing_out'], height=150, label_visibility="collapsed")

# Omni-Share Paywall
if st.session_state.app_state['is_pro']:
    if st.button("📲 OMNI-SHARE TO MOBILE SHEET", use_container_width=True): pass
else:
    st.button("📲 OMNI-SHARE (PRO ONLY 🔒)", disabled=True, use_container_width=True)

# STEP 5: SUPPLIES (NIKKI'S PIVOT)
st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
if st.session_state.app_state['supply_intel']: st.success(f"📦 BRAIN: {st.session_state.app_state['supply_intel']}")

supply_q = urllib.parse.quote(f"shipping supplies for {st.session_state.app_state['master_id']}")
st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.amazon.com/s?k={supply_q}" target="_blank" class="m-btn" id="amz-brown">AMAZON PRO</a>
        <a href="https://www.google.com/search?q={supply_q}+shipping&tbm=shop" target="_blank" class="m-btn" id="google-red">GOOGLE SHOP</a>
    </div>
''', unsafe_allow_html=True)

# STEP 6: INVENTORY (PRO PAYWALL)
st.markdown('<p class="step-label">STEP 6: <span class="neon-text">INVENTORY</span></p>', unsafe_allow_html=True)
if st.session_state.app_state['is_pro']:
    with st.expander("➕ MANUAL ENTRY"):
        with st.form("manual"):
            m_item = st.text_input("Item Name")
            m_plat = st.selectbox("Platform", ["eBay", "FB", "Posh"])
            if st.form_submit_button("Log Item"):
                st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": m_item, "Platform": m_plat})
                st.rerun()
else:
    st.warning("🔒 Manual Entry & Batching are locked for Pro Subscribers.")

if st.session_state.inventory:
    st.table(pd.DataFrame(st.session_state.inventory))

# --- 5. SIDEBAR ENGINE & PAYWALL ---
with st.sidebar:
    st.markdown("### 💎 COMMERCIAL SUITE")
    st.session_state.app_state['is_pro'] = st.toggle("Simulate Pro Subscription", value=st.session_state.app_state['is_pro'])
    
    st.divider()
    st.caption("ENGINE CONTROLS")
    
    def run_ghost(p):
        ctx = st.session_state.app_state['master_id'] if st.session_state.app_state['master_id'] else notes
        if ctx:
            with st.spinner(f"AI Writing {p}..."):
                res = client.models.generate_content(model=LITE_MODEL, contents=[f"Write a {style} {p} listing for: {ctx}"])
                st.session_state.app_state['listing_out'] = res.text
                st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": ctx[:30], "Platform": p})
        else:
            st.error("Run STEP 2 ANALYSIS first.")

    if st.button("GHOST_FB"): run_ghost("Facebook Marketplace")
    if st.button("GHOST_EBAY"): run_ghost("eBay")
    if st.button("GHOST_POSH"): run_ghost("Poshmark")
