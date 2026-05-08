import streamlit as st
import pandas as pd
import urllib.parse
import random
from datetime import datetime
from google import genai
from google.genai import types

# --- 1. THE ENGINE ROOM (SELF-HEALING & STATE) ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

# Static Tip Library (Zero-Token Efficiency)
TIP_LIBRARY = [
    "PRO TIP: Bright, natural light increases sales velocity by 30%.",
    "PRO TIP: Mention flaws early to build buyer trust and reduce returns.",
    "PRO TIP: Check 'Sold' listings on eBay for true market value.",
    "PRO TIP: SEO is king; use the 'Pro' style for high-search rankings.",
    "PRO TIP: Right-sizing your package saves an average of $2.40 per ship.",
    "PRO TIP: Consistent daily listings signal algorithms to boost your store.",
    "PRO TIP: Neutral backgrounds keep the buyer's focus on the item."
]

if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'master_desc': "", 
        'listing_out': "", 
        'active_model': None,
        'margin_est': "",
        'supply_intel': "",
        'tip': random.choice(TIP_LIBRARY)
    }

# API Handshake with Discovery Audit
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    if st.session_state.app_state['active_model'] is None:
        available_models = [m.name for m in client.models.list() if "generateContent" in m.supported_actions]
        target = next((m for m in available_models if "1.5-flash" in m), None)
        if not target: target = next((m for m in available_models if "flash" in m), "gemini-1.5-flash")
        st.session_state.app_state['active_model'] = target.replace("models/", "")
    LITE_MODEL = st.session_state.app_state['active_model']
except Exception as e:
    st.error(f"Engine Connection Failed: {str(e)}")

# --- 2. THE WHITE MASTERPIECE CSS (UI LOCK) ---
st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }

    /* STEP LABELS & INSTRUCTIONS */
    .brand-word { color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .step-label { color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; margin-top: 30px; border-bottom: 4px solid #0F172A; display: inline-block; }
    .onboarding { color: #475569; font-weight: 600; font-size: 14px; margin: 15px 0; border-left: 4px solid #CBD5E1; padding-left: 10px; }
    .pro-tip { color: #64748B; font-size: 13px; font-weight: 700; margin-bottom: 10px; font-style: italic; }

    /* WIDGET VISIBILITY FIXES */
    [data-testid="stRadio"] label, [data-testid="stRadio"] label p {
        color: #0F172A !important; font-weight: 800 !important; opacity: 1 !important;
    }
    [data-testid="stTextArea"] textarea {
        background-color: #F1F5F9 !important; color: #0F172A !important; font-weight: 600 !important; border: 2px solid #CBD5E1 !important; border-radius: 12px !important;
    }

    /* BUTTONS & BRAND COLORS */
    .flex-grid { display: flex; flex-wrap: nowrap; gap: 8px; width: 100%; margin: 10px 0; }
    .m-btn {
        flex: 1; height: 60px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
        text-decoration: none; color: #FFFFFF !important; font-weight: 950; font-size: 11px; text-transform: uppercase; border: none;
        cursor: pointer;
    }
    #ebay-blue { background-color: #002F6C !important; }
    #amz-brown { background-color: #483332 !important; }
    #google-red { background-color: #CC0000 !important; }
    #posh-maroon { background-color: #8C1B2F !important; }
    #fb-blue { background-color: #1877F2 !important; }
    #cl-purple { background-color: #502189 !important; }
    #viral-neon { background: linear-gradient(45deg, #22d3ee, #002F6C); font-size: 14px; }

    /* SIDEBAR AD SPACE & GHOST HIDER */
    [data-testid="stSidebar"] { border-left: 1px solid #E2E8F0; background-color: #F8FAFC !important; }
    div.stButton > button[kind="secondary"] { position: fixed; top: -500px; opacity: 0; pointer-events: none; }
    </style>
""", unsafe_allow_html=True)

# --- 3. THE OMNI-SHARE BRIDGE (JS) ---
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

# --- 4. 6-STEP SEQUENTIAL UI ---
st.markdown('<div style="margin-top:30px;"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text" style="font-size:18px;">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)
st.markdown('<div class="onboarding">Scan ➜ Analyze ➜ Price (Margin Master) ➜ List & Omni-Share ➜ Supplies ➜ Inventory Log</div>', unsafe_allow_html=True)

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
        st.session_state.app_state['master_desc'] = ""
        st.rerun()

# STEP 2: DESCRIBE & ANALYZE
st.markdown('<p class="step-label">STEP 2: <span class="neon-text">DESCRIBE</span></p>', unsafe_allow_html=True)
notes = st.text_area("Notes", height=80, placeholder="Brand, Size, Condition, or Rare Flaws...", label_visibility="collapsed")

if st.button("🚀 ANALYZE", type="primary", use_container_width=True):
    if 'hero_shot' in st.session_state:
        with st.spinner("Brain Analyzing..."):
            # Master Description Generation
            part = types.Part.from_bytes(data=st.session_state.hero_shot, mime_type=st.session_state.img_type)
            res = client.models.generate_content(model=LITE_MODEL, contents=[f"Analyze image + notes: {notes}. Create a specific 5-word search title.", part])
            st.session_state.app_state['master_desc'] = res.text
            
            # Step 5 Intelligence: Specific Supply Advice
            sup_res = client.models.generate_content(model=LITE_MODEL, contents=[f"Suggest 2 essential packing materials for: {res.text}"])
            st.session_state.app_state['supply_intel'] = sup_res.text
            
            # Refresh Tip
            st.session_state.app_state['tip'] = random.choice(TIP_LIBRARY)
            st.rerun()

# STEP 3: PRICE (MARGIN MASTER)
st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
if st.session_state.app_state['master_desc']:
    st.info(f"**IDENTIFIED:** {st.session_state.app_state['master_desc']}")
    st.caption("💡 MARGIN MASTER: Search results below represent GROSS value. Subtract ~15% for platform fees.")

search_q = urllib.parse.quote(st.session_state.app_state['master_desc'] if st.session_state.app_state['master_desc'] else notes)
st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.ebay.com/sch/i.html?_nkw={search_q}&LH_Sold=1&LH_Complete=1" target="_blank" class="m-btn" id="ebay-blue">EBAY SOLD</a>
        <a href="https://www.google.com/search?q={search_q}+price" target="_blank" class="m-btn" id="google-red">GOOGLE</a>
        <a href="https://poshmark.com/search?query={search_q}" target="_blank" class="m-btn" id="posh-maroon">POSH</a>
    </div>
''', unsafe_allow_html=True)

# STEP 4: LIST (OMNI-SHARE)
st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
style_choice = st.radio("Style", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")

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
if st.session_state.app_state['supply_intel']:
    st.success(f"📦 BRAIN ADVICE: {st.session_state.app_state['supply_intel']}")

supply_q = urllib.parse.quote(f"shipping supplies for {st.session_state.app_state['master_desc']}")
st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.amazon.com/s?k={supply_q}" target="_blank" class="m-btn" id="amz-brown">AMAZON PRO</a>
        <a href="https://www.google.com/search?q={supply_q}+shop" target="_blank" class="m-btn" id="google-red">GOOGLE SHOP</a>
    </div>
''', unsafe_allow_html=True)

# STEP 6: INVENTORY & VIRAL SHARE
st.markdown('<p class="step-label">STEP 6: <span class="neon-text">INVENTORY</span></p>', unsafe_allow_html=True)

with st.expander("➕ MANUAL ENTRY"):
    with st.form("manual"):
        m_item = st.text_input("Item Name")
        m_plat = st.selectbox("Platform", ["eBay", "Facebook", "Poshmark", "Other"])
        if st.form_submit_button("Add to Log"):
            st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": m_item, "Platform": m_plat})
            st.rerun()

if st.session_state.inventory:
    df = pd.DataFrame(st.session_state.inventory)
    st.table(df)
    
    # Viral Share & Management
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="m-btn" id="viral-neon">🚀 SHARE MY HAUL</div>', unsafe_allow_html=True)
    with col2:
        to_del = st.multiselect("Remove Item", range(len(st.session_state.inventory)), format_func=lambda x: st.session_state.inventory[x]['Item'], label_visibility="collapsed")
        if st.button("🗑️ DELETE"):
            st.session_state.inventory = [i for j, i in enumerate(st.session_state.inventory) if j not in to_del]
            st.rerun()

# --- 5. THE SIDEBAR (ADS & PRO DISPATCHER) ---
with st.sidebar:
    st.markdown("### 📢 AD SPACE")
    st.caption("Affiliate Banners & Marketing")
    
    st.divider()
    st.markdown("### 💎 PRO BATCH MODE")
    st.info("Batch Scan & Smart Dispatch is locked. Subscribe to unlock mass-listing.")
    if st.button("BATCH_SCAN_PRO", disabled=True):
        pass

    # Headless Ghost Triggers
    def run_ghost(p):
        with st.spinner(f"Writing {p}..."):
            ctx = st.session_state.app_state['master_desc'] if st.session_state.app_state['master_desc'] else notes
            res = client.models.generate_content(model=LITE_MODEL, contents=[f"Write a {style_choice} {p} listing: {ctx}"])
            st.session_state.app_state['listing_out'] = res.text
            st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": ctx[:30], "Platform": p})

    if st.button("GHOST_FB"): run_ghost("Facebook Marketplace")
    if st.button("GHOST_EBAY"): run_ghost("eBay")
    if st.button("GHOST_CL"): run_ghost("Craigslist")
    if st.button("GHOST_POSH"): run_ghost("Poshmark")
