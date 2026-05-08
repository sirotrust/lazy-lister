import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
from google import genai
from google.genai import types

# --- 1. ENGINE ROOM (HARD-LOCK) ---
# Hard-coded to Gemini 2.5 Flash-Lite for 1500+ RPD and $0.10/MTok pricing.
LITE_MODEL = "gemini-2.5-flash-lite" 

st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'master_id': "", 'listing_out': "", 'supply_tips': "", 'is_pro': False, 'scan_count': 0
    }
if 'notes_input' not in st.session_state:
    st.session_state.notes_input = ""

# --- 2. BACKEND TRIGGER (QUERY PARAMETER ANCHOR) ---
params = st.query_params
if "action" in params:
    action = params.get("action")
    ctx = st.session_state.app_state['master_id']
    if ctx:
        try:
            client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
            style_pref = st.session_state.get("style_radio", "Simple")
            res = client.models.generate_content(
                model=LITE_MODEL, 
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

# --- 3. THE WHITE MASTERPIECE UI (CSS) ---
st.markdown(f"""
    <style>
    header, footer, [data-testid="stHeader"] {{visibility: hidden; display: none;}}
    .stApp {{ background-color: #FFFFFF !important; }}

    /* UI VISIBILITY LOCK */
    [data-testid="stRadio"] label, [data-testid="stRadio"] label p, [data-testid="stWidgetLabel"] p {{
        color: #0F172A !important; font-weight: 800 !important; opacity: 1 !important;
    }}
    [data-testid="stTextArea"] textarea {{
        background-color: #F1F5F9 !important; color: #0F172A !important; font-weight: 600 !important; border: 2px solid #CBD5E1 !important;
    }}

    /* BRANDING (70px) */
    .brand-word {{ color: #0F172A; font-size: 70px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1.5px; }}
    .neon-text {{ font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; font-size: 18px !important; }}
    
    /* MICRO-INSTRUCTIONS (12px - ONE LINE) */
    .instruction-container {{ margin: 20px 0 30px 0; max-width: 950px; }}
    .instruction-row {{ 
        display: flex; 
        align-items: center; 
        margin-bottom: 3px;
        gap: 6px;
    }}
    .instruction-num {{
        font-size: 12px; font-weight: 950; min-width: 14px; flex-shrink: 0;
        background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .instruction-text {{ 
        font-size: 12px; font-weight: 950; text-transform: uppercase; letter-spacing: 0.5px; 
        background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        white-space: nowrap; 
    }}

    /* STEP LABELS (36px - UNIFORM GRADIENT) */
    .step-label {{ 
        font-weight: 950; font-size: 36px !important; text-transform: uppercase; margin-top: 35px; 
        display: block; width: 100%;
        background-image: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        line-height: 1.0; letter-spacing: -1px; border-bottom: 4px solid #F8FAFC;
    }}

    /* PLATFORM BUTTONS (STEP 3, 4, 5) */
    .flex-grid {{ display: flex; flex-wrap: nowrap; gap: 8px; width: 100%; margin: 15px 0; }}
    .m-btn {{
        flex: 1; height: 65px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
        text-decoration: none; color: #FFFFFF !important; font-weight: 950; font-size: 14px; text-transform: uppercase; border: none;
    }}
    
    #fb-cyan {{ background: linear-gradient(45deg, #22d3ee, #0ea5e9) !important; }}
    #ebay-midnight {{ background: linear-gradient(45deg, #002F6C, #0F172A) !important; }}
    #posh-velvet {{ background: linear-gradient(45deg, #8C1B2F, #4c0519) !important; }}
    #google-red {{ background-color: #CC0000 !important; }}
    #amz-brown {{ background-color: #483332 !important; }}
    
    /* ENHANCED NATIVE BUTTONS (ADD ITEM / ANALYZE) */
    .stButton button {{
        height: 70px !important; 
        border-radius: 14px !important; 
        font-weight: 950 !important;
        font-size: 22px !important; 
        background: #0F172A !important; 
        color: white !important; 
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. APP LAYOUT ---
st.markdown('<div style="margin-top:30px;"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)

st.markdown("""
<div class="instruction-container">
    <div class="instruction-row"><div class="instruction-num">1</div><div class="instruction-text">SCAN — Capture image</div></div>
    <div class="instruction-row"><div class="instruction-num">2</div><div class="instruction-text">ANALYZE — Extract data</div></div>
    <div class="instruction-row"><div class="instruction-num">3</div><div class="instruction-text">PRICE — Market comps</div></div>
    <div class="instruction-row"><div class="instruction-num">4</div><div class="instruction-text">LIST — Generate copy</div></div>
    <div class="instruction-row"><div class="instruction-num">5</div><div class="instruction-text">SUPPLY — Packing tools</div></div>
    <div class="instruction-row"><div class="instruction-num">6</div><div class="instruction-text">VAULT — Archive entry</div></div>
</div>
""", unsafe_allow_html=True)

# STEP 1: SCAN
st.markdown('<div class="step-label">STEP 1: SCAN</div>', unsafe_allow_html=True)
if 'hero_shot' not in st.session_state:
    img_file = st.camera_input("Scanner", label_visibility="collapsed")
    if img_file:
        st.session_state.hero_shot = img_file.getvalue()
        st.session_state.img_type = img_file.type
        st.rerun()
else:
    st.image(st.session_state.hero_shot, use_container_width=True)
    if st.button("ADD ITEM", use_container_width=True):
        for key in ['hero_shot', 'img_type']:
            if key in st.session_state: del st.session_state[key]
        st.session_state.app_state['master_id'] = ""
        st.session_state.app_state['listing_out'] = ""
        st.session_state.app_state['scan_count'] += 1 
        st.rerun()

# STEP 2: ANALYZE
st.markdown('<div class="step-label">STEP 2: ANALYZE</div>', unsafe_allow_html=True)
notes = st.text_area("Notes", height=100, placeholder="Brand, condition, flaws...", label_visibility="collapsed", key=f"notes_{st.session_state.app_state['scan_count']}")

if st.button("ANALYZE", use_container_width=True):
    if 'hero_shot' in st.session_state:
        with st.spinner("Analyzing..."):
            client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
            part = types.Part.from_bytes(data=st.session_state.hero_shot, mime_type=st.session_state.img_type)
            res = client.models.generate_content(model=LITE_MODEL, contents=[f"Analyze image + notes: {notes}. Create 5-word title.", part])
            st.session_state.app_state['master_id'] = res.text
            sup_res = client.models.generate_content(model=LITE_MODEL, contents=[f"Suggest 2 packing items for: {res.text}"])
            st.session_state.app_state['supply_tips'] = sup_res.text
            st.rerun()

# STEP 3: PRICE
st.markdown('<div class="step-label">STEP 3: PRICE</div>', unsafe_allow_html=True)
if st.session_state.app_state['master_id']: st.info(f"**AI ID:** {st.session_state.app_state['master_id']}")

sq = urllib.parse.quote(st.session_state.app_state['master_id'] if st.session_state.app_state['master_id'] else notes)
st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.ebay.com/sch/i.html?_nkw={sq}&LH_Sold=1&LH_Complete=1" target="_blank" class="m-btn" id="ebay-midnight">EBAY</a>
        <a href="https://www.google.com/search?q={sq}+price&tbm=shop" target="_blank" class="m-btn" id="google-red">GOOGLE</a>
        <a href="https://poshmark.com/search?query={sq}" target="_blank" class="m-btn" id="posh-velvet">POSH</a>
    </div>
''', unsafe_allow_html=True)

# STEP 4: LIST
st.markdown('<div class="step-label">STEP 4: LIST</div>', unsafe_allow_html=True)
st.radio("Style", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed", key="style_radio")

st.markdown(f'''
    <div class="flex-grid">
        <a href="/?action=facebook" target="_self" class="m-btn" id="fb-cyan">FACEBOOK</a>
        <a href="/?action=ebay" target="_self" class="m-btn" id="ebay-midnight">EBAY</a>
        <a href="/?action=poshmark" target="_self" class="m-btn" id="posh-velvet">POSHMARK</a>
    </div>
''', unsafe_allow_html=True)

st.text_area("Output", value=st.session_state.app_state['listing_out'], height=150, label_visibility="collapsed")

# STEP 5: SUPPLIES
st.markdown('<div class="step-label">STEP 5: SUPPLIES</div>', unsafe_allow_html=True)
if st.session_state.app_state['supply_tips']: st.success(f"📦 BRAIN: {st.session_state.app_state['supply_tips']}")

supply_q = urllib.parse.quote(f"shipping supplies for {st.session_state.app_state['master_id']}")
st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.amazon.com/s?k={supply_q}" target="_blank" class="m-btn" id="amz-brown">AMAZON PRO</a>
        <a href="https://www.google.com/search?q={supply_q}+shipping&tbm=shop" target="_blank" class="m-btn" id="google-red">GOOGLE</a>
    </div>
''', unsafe_allow_html=True)

# STEP 6: INVENTORY
st.markdown('<div class="step-label">STEP 6: INVENTORY</div>', unsafe_allow_html=True)
if st.session_state.inventory:
    st.table(pd.DataFrame(st.session_state.inventory))

# SIDEBAR PAYWALL
with st.sidebar:
    st.markdown("### 💎 COMMERCIAL SUITE")
    st.session_state.app_state['is_pro'] = st.toggle("Simulate Pro Subscription", value=st.session_state.app_state['is_pro'])
