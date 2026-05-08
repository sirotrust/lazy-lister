import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
from google import genai
from google.genai import types

# --- 1. ENGINE ROOM (STATE & RELAY) ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'master_id': "", 'listing_out': "", 'supply_tips': "", 'is_pro': False
    }

# Query Parameter Listener for Step 4 Execution (Reliability Anchor)
params = st.query_params
if "action" in params:
    action = params.get("action")
    ctx = st.session_state.app_state['master_id']
    if ctx:
        try:
            client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
            style_pref = st.session_state.get("style_radio", "Simple")
            res = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=[f"Write a {style_pref} {action} listing for: {ctx}"]
            )
            st.session_state.app_state['listing_out'] = res.text
            st.session_state.inventory.append({
                "Date": datetime.now().strftime("%m/%d"), 
                "Item": ctx[:30], 
                "Platform": action.upper()
            })
            st.query_params.clear()
        except Exception as e:
            st.error(f"ENGINE FAILURE: {str(e)}")
    else:
        st.query_params.clear()

# --- 2. THE WHITE MASTERPIECE UI (CSS) ---
st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }

    /* UI VISIBILITY LOCK */
    [data-testid="stRadio"] label, [data-testid="stRadio"] label p, [data-testid="stWidgetLabel"] p {
        color: #0F172A !important; font-weight: 800 !important; opacity: 1 !important;
    }
    [data-testid="stTextArea"] textarea {
        background-color: #F1F5F9 !important; color: #0F172A !important; font-weight: 600 !important; border: 2px solid #CBD5E1 !important;
    }

    /* BRANDING & HEADER */
    .brand-word { color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    
    /* HORIZONTAL SYMMETRICAL INSTRUCTIONS */
    .instruction-container { 
        display: flex; 
        justify-content: space-between; 
        margin: 20px 0 30px 40px; /* Left indentation */
        padding-right: 40px; 
        max-width: 100%;
        border-top: 1px solid #F1F5F9;
        border-bottom: 1px solid #F1F5F9;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .modern-instruction-item { 
        font-size: 10px; 
        font-weight: 800; 
        text-transform: uppercase; 
        letter-spacing: 0.5px; 
        background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        white-space: nowrap;
    }

    .step-label { color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; margin-top: 30px; border-bottom: 4px solid #0F172A; display: inline-block; }

    /* PRO-PALETTE BUTTONS (HTML ANCHORS) */
    .flex-grid { display: flex; flex-wrap: nowrap; gap: 8px; width: 100%; margin: 10px 0; }
    .m-btn {
        flex: 1; height: 60px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
        text-decoration: none; color: #FFFFFF !important; font-weight: 950; font-size: 12px; text-transform: uppercase; border: none;
    }
    
    #fb-cyan { background: linear-gradient(45deg, #22d3ee, #0ea5e9) !important; }
    #ebay-midnight { background: linear-gradient(45deg, #002F6C, #0F172A) !important; }
    #posh-velvet { background: linear-gradient(45deg, #8C1B2F, #4c0519) !important; }
    #google-red { background-color: #CC0000 !important; }
    #amz-brown { background-color: #483332 !important; }
    
    .stButton button {
        height: 60px !important; border-radius: 12px !important; font-weight: 950 !important;
        background: #0F172A !important; color: white !important; border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. THE HEADER & SYMMETRICAL INSTRUCTIONS ---
st.markdown('<div style="margin-top:30px;"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text" style="font-size:18px;">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)

st.markdown("""
<div class="instruction-container">
    <span class="modern-instruction-item">1 SCAN — IMAGE CAPTURE</span>
    <span class="modern-instruction-item">2 IDENTIFY — AI DATA</span>
    <span class="modern-instruction-item">3 PRICE — MARKET COMPS</span>
    <span class="modern-instruction-item">4 LIST — COPY GENERATION</span>
    <span class="modern-instruction-item">5 SUPPLY — PACKING TOOLS</span>
    <span class="modern-instruction-item">6 VAULT — ARCHIVE ENTRY</span>
</div>
""", unsafe_allow_html=True)

# --- 4. THE 6-STEP FLOW ---

# STEP 1: SCAN
st.markdown('<p class="step-label">STEP 1: SCAN</p>', unsafe_allow_html=True)
if 'hero_shot' not in st.session_state:
    img_file = st.camera_input("Scanner", label_visibility="collapsed")
    if img_file:
        st.session_state.hero_shot = img_file.getvalue()
        st.session_state.img_type = img_file.type
        st.rerun()
else:
    st.image(st.session_state.hero_shot, use_container_width=True)
    if st.button("ADD ITEM", use_container_width=True):
        del st.session_state.hero_shot
        st.session_state.app_state['master_id'] = ""
        st.session_state.app_state['listing_out'] = ""
        st.rerun()

# STEP 2: ANALYZE
st.markdown('<p class="step-label">STEP 2: ANALYZE</p>', unsafe_allow_html=True)
notes = st.text_area("Notes", height=100, placeholder="Brand, condition, flaws...", label_visibility="collapsed")

if st.button("AI IDENTIFY", use_container_width=True):
    if 'hero_shot' in st.session_state:
        with st.spinner("Identifying..."):
            client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
            part = types.Part.from_bytes(data=st.session_state.hero_shot, mime_type=st.session_state.img_type)
            res = client.models.generate_content(model="gemini-1.5-flash", contents=[f"Analyze image + notes: {notes}. Create 5-word title.", part])
            st.session_state.app_state['master_id'] = res.text
            # Load Step 5 advice
            sup_res = client.models.generate_content(model="gemini-1.5-flash", contents=[f"Suggest 2 packing items for: {res.text}"])
            st.session_state.app_state['supply_tips'] = sup_res.text
            st.rerun()

# STEP 3: PRICE (GOOGLE SHOPPING FIX)
st.markdown('<p class="step-label">STEP 3: PRICE</p>', unsafe_allow_html=True)
if st.session_state.app_state['master_id']: st.info(f"**AI ID:** {st.session_state.app_state['master_id']}")

sq = urllib.parse.quote(st.session_state.app_state['master_id'] if st.session_state.app_state['master_id'] else notes)
st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.ebay.com/sch/i.html?_nkw={sq}&LH_Sold=1&LH_Complete=1" target="_blank" class="m-btn" id="ebay-midnight">EBAY SOLD</a>
        <a href="https://www.google.com/search?q={sq}+price&tbm=shop" target="_blank" class="m-btn" id="google-red">GOOGLE SHOP</a>
        <a href="https://poshmark.com/search?query={sq}" target="_blank" class="m-btn" id="posh-velvet">POSH</a>
    </div>
''', unsafe_allow_html=True)

# STEP 4: LIST (QUERY PARAMETER ANCHOR)
st.markdown('<p class="step-label">STEP 4: LIST</p>', unsafe_allow_html=True)
st.radio("Style", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed", key="style_radio")

st.markdown(f'''
    <div class="flex-grid">
        <a href="/?action=facebook" target="_self" class="m-btn" id="fb-cyan">FACEBOOK</a>
        <a href="/?action=ebay" target="_self" class="m-btn" id="ebay-midnight">EBAY</a>
        <a href="/?action=poshmark" target="_self" class="m-btn" id="posh-velvet">POSHMARK</a>
    </div>
''', unsafe_allow_html=True)

st.text_area("Output", value=st.session_state.app_state['listing_out'], height=150, label_visibility="collapsed")

if st.session_state.app_state['is_pro']:
    if st.button("OMNI-SHARE TO DEVICE", use_container_width=True): pass
else:
    st.button("OMNI-SHARE (PRO ONLY 🔒)", disabled=True, use_container_width=True)

# STEP 5: SUPPLIES (GOOGLE SHOPPING FIX)
st.markdown('<p class="step-label">STEP 5: SUPPLIES</p>', unsafe_allow_html=True)
if st.session_state.app_state['supply_tips']: st.success(f"📦 BRAIN: {st.session_state.app_state['supply_tips']}")

supply_q = urllib.parse.quote(f"shipping supplies for {st.session_state.app_state['master_id']}")
st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.amazon.com/s?k={supply_q}" target="_blank" class="m-btn" id="amz-brown">AMAZON PRO</a>
        <a href="https://www.google.com/search?q={supply_q}+shipping&tbm=shop" target="_blank" class="m-btn" id="google-red">GOOGLE SHOP</a>
    </div>
''', unsafe_allow_html=True)

# STEP 6: INVENTORY
st.markdown('<p class="step-label">STEP 6: INVENTORY</p>', unsafe_allow_html=True)
if st.session_state.app_state['is_pro']:
    with st.expander("➕ MANUAL ENTRY (UNLOCKED)"):
        with st.form("manual"):
            m_item = st.text_input("Item Name")
            m_plat = st.selectbox("Platform", ["eBay", "Facebook", "Poshmark"])
            if st.form_submit_button("Log Item"):
                st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": m_item, "Platform": m_plat})
                st.rerun()
else:
    st.warning("🔒 Manual Entry & Batching are reserved for Pro Subscribers.")

if st.session_state.inventory:
    st.table(pd.DataFrame(st.session_state.inventory))

# SIDEBAR PAYWALL
with st.sidebar:
    st.markdown("### 💎 COMMERCIAL SUITE")
    st.session_state.app_state['is_pro'] = st.toggle("Simulate Pro Subscription", value=st.session_state.app_state['is_pro'])
