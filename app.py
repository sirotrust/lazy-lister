import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
from google import genai
from google.genai import types

# --- 1. THE BRAIN & SELF-HEALING DISCOVERY ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'analysis': "", 
        'master_desc': "", 
        'listing_out': "", 
        'active_model': None
    }

# Dynamic Handshake Logic
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    if st.session_state.app_state['active_model'] is None:
        # Self-Healing Audit: Auto-detect available flash models
        models = [m.name for m in client.models.list()]
        target = next((m for m in models if "flash" in m), "gemini-1.5-flash")
        st.session_state.app_state['active_model'] = target.replace("models/", "")
    
    LITE_MODEL = st.session_state.app_state['active_model']
except Exception as e:
    st.error(f"ENGINE ROOM ERROR: Handshake Failed. {str(e)}")

# --- 2. THE MASTERPIECE CSS (6-ZONE PROTECTION) ---
st.markdown(f"""
    <style>
    header, footer, [data-testid="stHeader"] {{visibility: hidden; display: none;}}
    .stApp {{ background-color: #FFFFFF !important; }}

    /* ZONE 1-6 LABELS */
    [data-testid="stRadio"] label, [data-testid="stWidgetLabel"] p {{
        color: #0F172A !important; font-weight: 800 !important;
    }}
    [data-testid="stTextArea"] textarea {{
        background-color: #F1F5F9 !important; color: #0F172A !important; 
        font-weight: 600 !important; border: 2px solid #CBD5E1 !important; border-radius: 12px !important;
    }}

    /* BRANDING & SEQUENTIAL STEPS */
    .brand-word {{ color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }}
    .neon-text {{ font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }}
    .step-label {{ color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; margin-top: 30px; border-bottom: 4px solid #0F172A; display: inline-block; }}
    
    /* BUTTON GRID LOCK */
    .flex-grid {{ display: flex; flex-wrap: nowrap; gap: 8px; width: 100%; margin: 10px 0; }}
    .m-btn {{
        flex: 1; height: 60px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
        text-decoration: none; color: #FFFFFF !important; font-weight: 950; font-size: 11px; text-transform: uppercase; border: none;
    }}
    #ebay-blue {{ background-color: #002F6C !important; }}
    #amz-brown {{ background-color: #483332 !important; }}
    #google-red {{ background-color: #CC0000 !important; }}
    #posh-maroon {{ background-color: #8C1B2F !important; }}
    #fb-blue {{ background-color: #1877F2 !important; }}
    #cl-purple {{ background-color: #502189 !important; }}

    /* INVISIBLE GHOST LAYER (FOR AD-READY SIDEBAR) */
    [data-testid="stSidebar"] {{ background-color: #F8FAFC !important; border-left: 1px solid #E2E8F0; }}
    div.stButton > button[kind="secondary"] {{
        position: fixed; top: -100px; opacity: 0; pointer-events: none;
    }}
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
    if (e.target.id === 'fb-blue-trig') trigger('GHOST_FB');
    if (e.target.id === 'ebay-blue-trig') trigger('GHOST_EBAY');
    if (e.target.id === 'cl-purple-trig') trigger('GHOST_CL');
    if (e.target.id === 'posh-maroon-trig') trigger('GHOST_POSH');
});
</script>
""", height=0)

# --- 4. 6-STEP SEQUENTIAL UI ---
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
notes = st.text_area("Notes", height=100, placeholder="Condition, flaws, etc.", label_visibility="collapsed")

# STEP 3: PRICE (MASTER RELAY)
st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
if st.button("🚀 ANALYZE MARKET", type="primary", use_container_width=True):
    if 'hero_shot' in st.session_state:
        with st.spinner("AI Generating Master Description..."):
            part = types.Part.from_bytes(data=st.session_state.hero_shot, mime_type=st.session_state.img_type)
            # Prompting for a structured search-ready master description
            res = client.models.generate_content(model=LITE_MODEL, contents=[f"Analyze this image. Create a 5-word specific search title for this item based on these notes: {notes}", part])
            st.session_state.app_state['master_desc'] = res.text
            st.session_state.app_state['analysis'] = f"Master ID: {res.text}"

if st.session_state.app_state['analysis']:
    st.info(st.session_state.app_state['analysis'])

search_query = urllib.parse.quote(st.session_state.app_state['master_desc'] if st.session_state.app_state['master_desc'] else notes)
st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.ebay.com/sch/i.html?_nkw={search_query}&LH_Sold=1&LH_Complete=1" target="_blank" class="m-btn" id="ebay-blue">EBAY SOLD</a>
        <a href="https://www.google.com/search?q={search_query}+price" target="_blank" class="m-btn" id="google-red">GOOGLE</a>
        <a href="https://poshmark.com/search?query={search_query}" target="_blank" class="m-btn" id="posh-maroon">POSH</a>
    </div>
''', unsafe_allow_html=True)

# STEP 4: LIST (ON-DEMAND)
st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
style_mode = st.radio("Style", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")

st.markdown(f'''
    <div class="flex-grid">
        <a href="#" class="m-btn" id="fb-blue-trig">FB</a>
        <a href="#" class="m-btn" id="ebay-blue-trig">EBAY</a>
        <a href="#" class="m-btn" id="cl-purple-trig">CL</a>
        <a href="#" class="m-btn" id="posh-maroon-trig">POSH</a>
    </div>
''', unsafe_allow_html=True)
st.text_area("Output", value=st.session_state.app_state['listing_out'], height=150, label_visibility="collapsed")

# STEP 5: SUPPLIES (INTELLIGENT SUGGESTIONS)
st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
supply_query = urllib.parse.quote(f"shipping supplies for {st.session_state.app_state['master_desc']}")
st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.amazon.com/s?k={supply_query}" target="_blank" class="m-btn" id="amz-brown">AMAZON PRO</a>
        <a href="https://www.google.com/search?q={supply_query}+shop" target="_blank" class="m-btn" id="google-red">GOOGLE SHOP</a>
    </div>
''', unsafe_allow_html=True)

# STEP 6: INVENTORY (MANAGEMENT PORTAL)
st.markdown('<p class="step-label">STEP 6: <span class="neon-text">INVENTORY</span></p>', unsafe_allow_html=True)

# 6.1 Manual Entry Form
with st.expander("➕ ADD MANUAL ENTRY"):
    with st.form("manual_add"):
        m_item = st.text_input("Item Name")
        m_plat = st.selectbox("Platform", ["eBay", "Facebook", "Poshmark", "Craigslist", "Other"])
        if st.form_submit_button("Add to Log"):
            st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": m_item, "Platform": m_plat})
            st.rerun()

# 6.2 The Log Table
if st.session_state.inventory:
    df = pd.DataFrame(st.session_state.inventory)
    st.table(df)
    
    # 6.3 Surgical Delete
    to_delete = st.multiselect("Select Items to Remove", range(len(st.session_state.inventory)), format_func=lambda x: st.session_state.inventory[x]['Item'])
    if st.button("🗑️ REMOVE SELECTED"):
        st.session_state.inventory = [i for j, i in enumerate(st.session_state.inventory) if j not in to_delete]
        st.rerun()
else:
    st.info("Log is currently empty.")

# --- 5. THE SIDEBAR (ENGINE ROOM & ADS) ---
with st.sidebar:
    st.markdown("### 📢 AD SPACE")
    st.write("Affiliate Banners Here")
    
    def run_ghost(p):
        with st.spinner(f"Writing {p}..."):
            ctx = st.session_state.app_state['master_desc'] if st.session_state.app_state['master_desc'] else notes
            prompt = f"Write a {style_mode} {p} listing for: {ctx}"
            res = client.models.generate_content(model=LITE_MODEL, contents=[prompt])
            st.session_state.app_state['listing_out'] = res.text
            st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": ctx[:30], "Platform": p})

    # Headless Triggers
    if st.button("GHOST_FB", type="secondary"): run_ghost("Facebook")
    if st.button("GHOST_EBAY", type="secondary"): run_ghost("eBay")
    if st.button("GHOST_CL", type="secondary"): run_ghost("Craigslist")
    if st.button("GHOST_POSH", type="secondary"): run_ghost("Poshmark")
