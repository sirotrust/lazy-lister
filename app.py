import streamlit as st
import pandas as pd
import random
from datetime import datetime
from google import genai

# --- 1. THE ARCHITECTURAL ENGINE (ULTRA-CONTRAST CSS) ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

if 'inventory' not in st.session_state:
    st.session_state.inventory = []

# Google Client Handshake
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("LEAD DEV: API Handshake Failed. Check secrets.toml.")

st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }

    /* ZONE 1: RADIO & LABEL VISIBILITY */
    [data-testid="stRadio"] label, 
    [data-testid="stRadio"] label p,
    [data-testid="stWidgetLabel"] p {
        color: #0F172A !important;
        font-weight: 800 !important;
        opacity: 1 !important;
    }

    /* ZONE 2: TABLE CONTRAST */
    [data-testid="stTable"] td, 
    [data-testid="stTable"] th {
        color: #0F172A !important;
        background-color: #F8FAFC !important;
        font-weight: 600 !important;
        border: 1px solid #E2E8F0 !important;
    }

    /* ZONE 3: TEXT INPUTS */
    [data-testid="stTextArea"] textarea {
        background-color: #F1F5F9 !important;
        color: #0F172A !important; 
        -webkit-text-fill-color: #0F172A !important;
        font-weight: 600 !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 12px !important;
    }

    /* ZONE 4: BRANDING */
    .brand-word { color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .step-label { color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; margin-top: 30px; border-bottom: 4px solid #0F172A; display: inline-block; }

    /* ZONE 5: BUTTON GRID LOCK */
    .flex-grid { display: flex; flex-wrap: nowrap; gap: 8px; width: 100%; margin: 10px 0; }
    .m-btn {
        flex: 1;
        height: 60px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        color: #FFFFFF !important;
        font-weight: 950;
        font-size: 11px;
        text-transform: uppercase;
        border: none;
    }

    /* ZONE 6: COLORS */
    #ebay-blue { background-color: #002F6C !important; }
    #amz-brown { background-color: #483332 !important; }
    #google-red { background-color: #CC0000 !important; }
    #posh-maroon { background-color: #8C1B2F !important; }
    #fb-blue { background-color: #1877F2 !important; }
    #cl-purple { background-color: #502189 !important; }
    #copy-teal { background-color: #0D9488 !important; }
    #dl-indigo { background-color: #4F46E5 !important; }

    /* ZONE 7: BOXES */
    .suggestion-box { background-color: #F0F9FF !important; border-left: 6px solid #0EA5E9 !important; padding: 15px; border-radius: 12px; margin: 10px 0; border: 1px solid #E0F2FE; }
    .reminder-box { background-color: #FFFBEB !important; border-left: 6px solid #F59E0B !important; padding: 15px; border-radius: 12px; margin: 10px 0; border: 1px solid #FEF3C7; }
    .tip-tag { font-weight: 950; font-size: 11px; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

# --- 2. UI EXECUTION ---
st.markdown('<div style="margin-top:30px;"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text" style="font-size:18px;">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)

# STEP 1
st.markdown('<p class="step-label">STEP 1: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)
img_file = st.camera_input("Scanner", label_visibility="collapsed")

# STEP 2
st.markdown('<p class="step-label">STEP 2: <span class="neon-text">DESCRIBE</span></p>', unsafe_allow_html=True)
notes = st.text_area("Notes", height=100, placeholder="Brand, Size, Condition...", label_visibility="collapsed")

# STEP 3
st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)

if st.button("🚀 ANALYZE MARKET", type="primary", use_container_width=True):
    if img_file:
        with st.spinner("AI Brain Thinking..."):
            response = client.models.generate_content(
                model="gemini-2.0-flash-lite-preview-02-05",
                contents=[notes, img_file]
            )
            st.info(response.text)

st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.ebay.com/sch/i.html?_nkw={notes}" target="_blank" class="m-btn" id="ebay-blue">EBAY</a>
        <a href="https://www.amazon.com/s?k={notes}" target="_blank" class="m-btn" id="amz-brown">AMAZON</a>
        <a href="https://www.google.com/search?q={notes}" target="_blank" class="m-btn" id="google-red">GOOGLE</a>
        <a href="https://poshmark.com/search?query={notes}" target="_blank" class="m-btn" id="posh-maroon">POSH</a>
    </div>
''', unsafe_allow_html=True)

# STEP 4
st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)

style = st.radio("Style", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("FB", use_container_width=True):
        res = client.models.generate_content(model="gemini-2.0-flash-lite-preview-02-05", contents=[f"Write a {style} Facebook listing: {notes}"])
        st.session_state.listing = res.text
        st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": notes[:30], "Platform": "Facebook"})
with col2:
    if st.button("EBAY", use_container_width=True):
        res = client.models.generate_content(model="gemini-2.0-flash-lite-preview-02-05", contents=[f"Write a {style} eBay listing: {notes}"])
        st.session_state.listing = res.text
        st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": notes[:30], "Platform": "eBay"})
with col3:
    if st.button("CL", use_container_width=True):
        res = client.models.generate_content(model="gemini-2.0-flash-lite-preview-02-05", contents=[f"Write a {style} Craigslist listing: {notes}"])
        st.session_state.listing = res.text
        st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": notes[:30], "Platform": "Craigslist"})
with col4:
    if st.button("POSH", use_container_width=True):
        res = client.models.generate_content(model="gemini-2.0-flash-lite-preview-02-05", contents=[f"Write a {style} Poshmark listing: {notes}"])
        st.session_state.listing = res.text
        st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": notes[:30], "Platform": "Poshmark"})

st.text_area("Output", value=st.session_state.get('listing', ''), height=150, label_visibility="collapsed")

# STEP 5
st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
st.markdown('''
    <div class="flex-grid">
        <a href="https://google.com" target="_blank" class="m-btn" id="google-red">GOOGLE SHOP</a>
        <a href="https://amazon.com" target="_blank" class="m-btn" id="amz-brown">AMAZON PRO</a>
    </div>
''', unsafe_allow_html=True)

# INVENTORY LOG
st.divider()
st.markdown('<p class="step-label">INVENTORY LOG</p>', unsafe_allow_html=True)

if not st.session_state.inventory:
    ghost_data = pd.DataFrame({"Item": ["Scanning Log..."], "Platform": ["--"], "Date": ["--"]})
    st.table(ghost_data)
else:
    df = pd.DataFrame(st.session_state.inventory)
    st.table(df)

st.markdown('''
    <div class="flex-grid">
        <a href="#" class="m-btn" id="copy-teal">📋 COPY DATA</a>
        <a href="#" class="m-btn" id="dl-indigo">📥 DOWNLOAD CSV</a>
    </div>
''', unsafe_allow_html=True)
