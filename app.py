import streamlit as st
import pandas as pd
import urllib.parse
import random
from datetime import datetime
from google import genai
from google.genai import types

# --- 1. THE ENGINE ROOM (STATE & RELAY) ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'master_id': "", 'listing_out': "", 'active_model': None,
        'supply_intel': "", 'is_pro': False 
    }

# Dynamic Handshake (Zero 404s)
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    if st.session_state.app_state['active_model'] is None:
        avail = [m.name for m in client.models.list() if "generateContent" in m.supported_actions]
        target = next((m for m in avail if "flash" in m), "gemini-1.5-flash")
        st.session_state.app_state['active_model'] = target.replace("models/", "")
    LITE_MODEL = st.session_state.app_state['active_model']
except Exception as e:
    st.error(f"ENGINE ROOM ERROR: {str(e)}")

# --- 2. WHITE MASTERPIECE & KEY-ANCHORED CSS ---
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

    /* BRANDING & SEQUENTIAL FLOW */
    .brand-word {{ color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }}
    .neon-text {{ font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }}
    .step-label {{ color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; margin-top: 30px; border-bottom: 4px solid #0F172A; display: inline-block; }}
    .onboarding {{ color: #475569; font-weight: 600; font-size: 14px; margin: 15px 0; border-left: 4px solid #CBD5E1; padding-left: 10px; }}

    /* KEY-ANCHORED PRO PALETTE (Step 4 Fix) */
    div[data-testid="stElementContainer"]:has(button[key="fb_btn"]) button {{
        background: linear-gradient(45deg, #22d3ee, #0ea5e9) !important; color: white !important;
    }}
    div[data-testid="stElementContainer"]:has(button[key="ebay_btn"]) button {{
        background: linear-gradient(45deg, #002F6C, #0F172A) !important; color: white !important;
    }}
    div[data-testid="stElementContainer"]:has(button[key="posh_btn"]) button {{
        background: linear-gradient(45deg, #8C1B2F, #4c0519) !important; color: white !important;
    }}
    
    /* UNIVERSAL BUTTON STYLING */
    .stButton button {{
        height: 60px !important; border-radius: 12px !important; font-weight: 950 !important; 
        font-size: 12px !important; text-transform: uppercase !important; border: none !important;
    }}

    /* HTML LINKS (Steps 3 & 5) */
    .flex-grid {{ display: flex; flex-wrap: nowrap; gap: 8px; width: 100%; margin: 10px 0; }}
    .m-btn {{
        flex: 1; height: 60px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
        text-decoration: none; color: #FFFFFF !important; font-weight: 950; font-size: 11px; text-transform: uppercase; border: none;
    }}
    #ebay-blue {{ background-color: #002F6C !important; }}
    #amz-brown {{ background-color: #483332 !important; }}
    #google-red {{ background-color: #CC0000 !important; }}
    #posh-maroon {{ background-color: #8C1B2F !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 3. THE 6-STEP FLOW ---
st.markdown('<div style="margin-top:30px;"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text" style="font-size:18px;">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)

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
    if st.button("📸 NEW SCAN (PURGE SANDBOX)", key="purge_btn"):
        del st.session_state.hero_shot
        st.session_state.app_state['master_id'] = ""
        st.session_state.app_state['listing_out'] = ""
        st.session_state.app_state['supply_intel'] = ""
        st.rerun()

# STEP 2: ANALYZE (MASTER ANCHOR)
st.markdown('<p class="step-label">STEP 2: <span class="neon-text">ANALYZE</span></p>', unsafe_allow_html=True)
notes = st.text_area("Notes", height=100, placeholder="Condition, brand, flaws...", label_visibility="collapsed")

if st.button("🚀 RUN BRAIN ANALYSIS", type="primary", key="analyze_btn"):
    if 'hero_shot' in st.session_state:
        with st.spinner("AI Analysis..."):
            part = types.Part.from_bytes(data=st.session_state.hero_shot, mime_type=st.session_state.img_type)
            res = client.models.generate_content(model=LITE_MODEL, contents=[f"Analyze image + notes: {notes}. Create 5-word search title.", part])
            st.session_state.app_state['master_id'] = res.text
            # Pre-load specialized Step 5 advice
            sup_res = client.models.generate_content(model=LITE_MODEL, contents=[f"Suggest 2 specialized packing items for: {res.text}"])
            st.session_state.app_state['supply_intel'] = sup_res.text
            st.rerun()

# STEP 3: PRICE (GOOGLE SHOPPING FIX)
st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
if st.session_state.app_state['master_id']: st.info(f"**AI ID:** {st.session_state.app_state['master_id']}")

sq = urllib.parse.quote(st.session_state.app_state['master_id'] if st.session_state.app_state['master_id'] else notes)
st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.ebay.com/sch/i.html?_nkw={sq}&LH_Sold=1&LH_Complete=1" target="_blank" class="m-btn" id="ebay-blue">EBAY SOLD</a>
        <a href="https://www.google.com/search?q={sq}+price&tbm=shop" target="_blank" class="m-btn" id="google-red">GOOGLE SHOP</a>
        <a href="https://poshmark.com/search?query={sq}" target="_blank" class="m-btn" id="posh-maroon">POSH</a>
    </div>
''', unsafe_allow_html=True)

# STEP 4: LIST (NATIVE ANCHORS)
st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
style = st.radio("Style", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")

def generate_listing(platform_name):
    ctx = st.session_state.app_state['master_id'] if st.session_state.app_state['master_id'] else notes
    if ctx:
        with st.spinner(f"Writing {platform_name} Listing..."):
            res = client.models.generate_content(model=LITE_MODEL, contents=[f"Write a {style} {platform_name} listing for: {ctx}"])
            st.session_state.app_state['listing_out'] = res.text
            st.session_state.inventory.append({{"Date": datetime.now().strftime("%m/%d"), "Item": ctx[:30], "Platform": platform_name}})
    else:
        st.error("Please run STEP 2 ANALYSIS first.")

if st.button("FACEBOOK", key="fb_btn", use_container_width=True): generate_listing("Facebook Marketplace")
if st.button("EBAY", key="ebay_btn", use_container_width=True): generate_listing("eBay")
if st.button("POSHMARK", key="posh_btn", use_container_width=True): generate_listing("Poshmark")

st.text_area("Output", value=st.session_state.app_state['listing_out'], height=150, label_visibility="collapsed")

if not st.session_state.app_state['is_pro']:
    st.button("📲 OMNI-SHARE (PRO ONLY 🔒)", disabled=True, use_container_width=True)
else:
    if st.button("📲 OMNI-SHARE TO DEVICE", type="primary", use_container_width=True): pass

# STEP 5: SUPPLIES (RESTORED SHOPPING BUTTONS)
st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
if st.session_state.app_state['supply_intel']: st.success(f"📦 BRAIN ADVICE: {st.session_state.app_state['supply_intel']}")

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
    with st.expander("➕ MANUAL ENTRY (UNLOCKED)"):
        with st.form("manual"):
            m_item = st.text_input("Item Name")
            m_plat = st.selectbox("Platform", ["eBay", "Facebook", "Poshmark"])
            if st.form_submit_button("Add to Log"):
                st.session_state.inventory.append({{"Date": datetime.now().strftime("%m/%d"), "Item": m_item, "Platform": m_plat}})
                st.rerun()
else:
    st.warning("🔒 Manual Entry & Batching are reserved for Pro Subscribers.")

if st.session_state.inventory:
    st.table(pd.DataFrame(st.session_state.inventory))

# SIDEBAR PAYWALL
with st.sidebar:
    st.markdown("### 💎 COMMERCIAL SUITE")
    st.session_state.app_state['is_pro'] = st.toggle("Simulate Pro Subscription", value=st.session_state.app_state['is_pro'])
