import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
from google import genai
from google.genai import types

# --- 1. ENGINE ROOM ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'master_id': "", 'listing_out': "", 'active_model': None,
        'supply_tips': "", 'is_pro': False
    }

try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    if st.session_state.app_state['active_model'] is None:
        avail = [m.name for m in client.models.list() if "generateContent" in m.supported_actions]
        target = next((m for m in avail if "flash" in m), "gemini-1.5-flash")
        st.session_state.app_state['active_model'] = target.replace("models/", "")
    LITE_MODEL = st.session_state.app_state['active_model']
except Exception as e:
    st.error(f"ENGINE ROOM: Handshake Failed. {str(e)}")

# --- 2. THE WHITE MASTERPIECE UI (FORENSIC CSS) ---
st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }

    /* TEXT STYLING */
    [data-testid="stRadio"] label p, [data-testid="stWidgetLabel"] p {
        color: #0F172A !important; font-weight: 800 !important;
    }
    [data-testid="stTextArea"] textarea {
        background-color: #F8FAFC !important; color: #0F172A !important; font-weight: 600 !important; border: 2px solid #E2E8F0 !important;
    }

    /* BRANDING */
    .brand-word { color: #0F172A; font-size: 55px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .step-label { color: #0F172A !important; font-weight: 950; font-size: 26px; text-transform: uppercase; margin-top: 25px; border-bottom: 4px solid #0F172A; display: inline-block; }
    
    /* INSTRUCTIONS */
    .protocol-box { margin: 15px 0; padding: 15px; border-left: 4px solid #22d3ee; background-color: #F1F5F9; border-radius: 0 8px 8px 0; }
    .protocol-text { color: #475569; font-weight: 700; font-size: 13px; line-height: 1.5; }

    /* BUTTONS: THE COLOR INJECTION */
    div.stButton > button {
        height: 60px !important; border-radius: 12px !important; font-weight: 950 !important; 
        font-size: 14px !important; text-transform: uppercase !important; border: none !important;
        width: 100% !important;
    }

    /* TARGETED COLOR OVERRIDES (KILLING THE ORANGE) */
    /* Step 1 & 2: Cyan */
    div.stButton > button:has(div p:contains("ADD NEW ITEM")),
    div.stButton > button:has(div p:contains("AI IDENTIFY")) {
        background-color: #22d3ee !important; color: #0F172A !important;
    }

    /* Step 4: Company Colors */
    div.stButton > button:has(div p:contains("FACEBOOK")) {
        background-color: #1877F2 !important; color: #FFFFFF !important;
    }
    div.stButton > button:has(div p:contains("EBAY")) {
        background-color: #0F172A !important; color: #FFFFFF !important;
    }
    div.stButton > button:has(div p:contains("POSHMARK")) {
        background-color: #8C1B2F !important; color: #FFFFFF !important;
    }
    
    /* Pro Lock Styling */
    div.stButton > button:disabled {
        background-color: #E2E8F0 !important; color: #94A3B8 !important;
    }

    /* GRID LINKS (Steps 3 & 5) */
    .flex-grid { display: flex; flex-wrap: nowrap; gap: 8px; width: 100%; margin: 10px 0; }
    .m-btn {
        flex: 1; height: 60px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
        text-decoration: none; color: #FFFFFF !important; font-weight: 950; font-size: 11px; text-transform: uppercase;
    }
    #ebay-blue { background-color: #0F172A !important; }
    #google-red { background-color: #CC0000 !important; }
    #posh-maroon { background-color: #8C1B2F !important; }
    #amz-brown { background-color: #483332 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. THE 6-STEP FLOW ---
st.markdown('<div style="margin-top:20px;"><span class="brand-word">LAZY LISTER</span><br><span class="neon-text" style="font-size:16px;">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)

# STEP 1: SCAN
st.markdown('<p class="step-label">STEP 1: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)

st.markdown('''
<div class="protocol-box">
    <div class="protocol-text">
        1. <b>SNAP:</b> Capture a clear photo of the item using the scanner.<br>
        2. <b>NOTES:</b> Describe the brand, size, and condition in Step 2.<br>
        3. <b>IDENTIFY:</b> Run the AI to generate the master item details.<br>
        4. <b>LAUNCH:</b> Select a platform to generate your listing copy.
    </div>
</div>
''', unsafe_allow_html=True)

if 'hero_shot' not in st.session_state:
    img_file = st.camera_input("Scanner", label_visibility="collapsed")
    if img_file:
        st.session_state.hero_shot = img_file.getvalue()
        st.session_state.img_type = img_file.type
        st.rerun()
else:
    st.image(st.session_state.hero_shot, use_container_width=True)
    if st.button("ADD NEW ITEM", key="add_new_item"):
        del st.session_state.hero_shot
        st.session_state.app_state['master_id'] = ""
        st.session_state.app_state['listing_out'] = ""
        st.rerun()

# STEP 2: ANALYZE
st.markdown('<p class="step-label">STEP 2: <span class="neon-text">ANALYZE</span></p>', unsafe_allow_html=True)
notes = st.text_area("Notes", height=100, placeholder="Condition, brand, flaws...", label_visibility="collapsed")

if st.button("AI IDENTIFY", key="ai_identify"):
    if 'hero_shot' in st.session_state:
        with st.spinner("Decoding..."):
            part = types.Part.from_bytes(data=st.session_state.hero_shot, mime_type=st.session_state.img_type)
            res = client.models.generate_content(model=LITE_MODEL, contents=[f"Analyze: {notes}. 5-word title.", part])
            st.session_state.app_state['master_id'] = res.text
            sup_res = client.models.generate_content(model=LITE_MODEL, contents=[f"Packing tips for: {res.text}"])
            st.session_state.app_state['supply_tips'] = sup_res.text
            st.rerun()

# STEP 3: PRICE
st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
if st.session_state.app_state['master_id']: st.info(f"**AI ID:** {st.session_state.app_state['master_id']}")

sq = urllib.parse.quote(st.session_state.app_state['master_id'] if st.session_state.app_state['master_id'] else notes)
st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.ebay.com/sch/i.html?__nkw={sq}&LH_Sold=1&LH_Complete=1" target="_blank" class="m-btn" id="ebay-blue">EBAY SOLD</a>
        <a href="https://www.google.com/search?q={sq}+price&tbm=shop" target="_blank" class="m-btn" id="google-red">GOOGLE SHOP</a>
        <a href="https://poshmark.com/search?query={sq}" target="_blank" class="m-btn" id="posh-maroon">POSH</a>
    </div>
''', unsafe_allow_html=True)

# STEP 4: LIST
st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
style = st.radio("Style", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")

def generate_listing(platform):
    ctx = st.session_state.app_state['master_id'] if st.session_state.app_state['master_id'] else notes
    if ctx:
        with st.spinner(f"Writing {platform}..."):
            res = client.models.generate_content(model=LITE_MODEL, contents=[f"Write a {style} {platform} listing for: {ctx}"])
            st.session_state.app_state['listing_out'] = res.text
            st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": ctx[:30], "Platform": platform})
    else:
        st.error("Run STEP 2 first.")

if st.button("FACEBOOK", key="fb_btn"): generate_listing("Facebook")
if st.button("EBAY", key="ebay_btn"): generate_listing("eBay")
if st.button("POSHMARK", key="posh_btn"): generate_listing("Poshmark")

st.text_area("Output", value=st.session_state.app_state['listing_out'], height=150, label_visibility="collapsed")

# OMNI-SHARE (PRO ONLY)
if st.session_state.app_state['is_pro']:
    if st.button("OMNI-SHARE TO DEVICE", key="omni_btn"): pass
else:
    st.button("OMNI-SHARE (PRO ONLY LOCK)", disabled=True, key="omni_locked")

# STEP 5: SUPPLIES
st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
if st.session_state.app_state['supply_tips']: st.success(f"BRAIN: {st.session_state.app_state['supply_tips']}")

supply_q = urllib.parse.quote(f"shipping supplies for {st.session_state.app_state['master_id']}")
st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.amazon.com/s?k={supply_q}" target="_blank" class="m-btn" id="amz-brown">AMAZON PRO</a>
        <a href="https://www.google.com/search?q={supply_q}+shipping&tbm=shop" target="_blank" class="m-btn" id="google-red">GOOGLE SHOP</a>
    </div>
''', unsafe_allow_html=True)

# STEP 6: INVENTORY
st.markdown('<p class="step-label">STEP 6: <span class="neon-text">INVENTORY</span></p>', unsafe_allow_html=True)
if st.session_state.inventory:
    st.table(pd.DataFrame(st.session_state.inventory))

with st.sidebar:
    st.markdown("### COMMERCIAL SUITE")
    st.session_state.app_state['is_pro'] = st.toggle("Simulate Pro Subscription", value=st.session_state.app_state['is_pro'])
