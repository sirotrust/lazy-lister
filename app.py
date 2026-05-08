import streamlit as st
import pandas as pd
import random
from datetime import datetime
from google import genai

# --- 1. THE ARCHITECTURAL ENGINE (ULTRA-CONTRAST CSS RESTORED) ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

if 'inventory' not in st.session_state:
    st.session_state.inventory = []

if 'listing_out' not in st.session_state:
    st.session_state.listing_out = ""

# Google Client Handshake (Flash-Lite Engine)
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    LITE_MODEL = "gemini-2.0-flash-lite-preview-02-05"
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

    /* ZONE 5: BUTTON GRID LOCK & IDs */
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
    #copy-teal { background-color: #0D9488 !important; }
    #dl-indigo { background-color: #4F46E5 !important; }

    /* ZONE 6: BOXES */
    .suggestion-box { background-color: #F0F9FF !important; border-left: 6px solid #0EA5E9 !important; padding: 15px; border-radius: 12px; margin: 10px 0; border: 1px solid #E0F2FE; }
    .reminder-box { background-color: #FFFBEB !important; border-left: 6px solid #F59E0B !important; padding: 15px; border-radius: 12px; margin: 10px 0; border: 1px solid #FEF3C7; }
    .tip-tag { font-weight: 950; font-size: 11px; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE MASTER 50-TIP NEURAL LIBRARY ---
TIP_POOL = {
    "s1": ["Pro Tip: Use the rear-facing lens; it has 40% higher resolution.", "Pro Tip: Lock AE/AF Lock by holding the screen.", "Pro Tip: Natural window light between 10am-2pm is best.", "Pro Tip: Turn on gridlines for perfect leveling.", "Pro Tip: Move closer; never use digital zoom.", "Pro Tip: Clean your lens before every session.", "Pro Tip: Use white backgrounds for AI edge detection.", "Pro Tip: Shoot the care tag for fabric verification.", "Pro Tip: Use white board to reflect light into shadows.", "Pro Tip: Shoot shoes at a 45-degree hero angle."],
    "s2": ["Pro Tip: Place the Brand and Model in the first 3 words.", "Pro Tip: Use words like 'buttery' or 'structured' to sell the feel.", "Pro Tip: Mention 'Smoke-Free' to build buyer trust.", "Pro Tip: List Pit-to-pit, Length, and Sleeve measurements.", "Pro Tip: Use 'texture' keywords like 'slubby'.", "Pro Tip: Define the Vibe: Is it Gorpcore or Minimalist?", "Pro Tip: Find the model code on the internal tag.", "Pro Tip: Disclose pilling early to reduce returns.", "Pro Tip: Use 'Azure' or 'Cobalt' instead of just 'Blue'.", "Pro Tip: Mention hardware quality for premium items."],
    "s3": ["Pro Tip: Check 'Sold' listings, not 'Active' ones.", "Pro Tip: Price 10% high to allow for negotiations.", "Pro Tip: $24.99 converts 15% better than $25.00.", "Pro Tip: Weigh items before pricing for shipping.", "Pro Tip: Cross-reference eBay vs Poshmark for averages.", "Pro Tip: Free Shipping tags increase filter hits by 2x.", "Pro Tip: Price vintage on rarity, not just fashion.", "Pro Tip: Drop prices by 10% on Fridays for paydays.", "Pro Tip: High-demand brands follow strict MSRP logic.", "Pro Tip: High-quality photos justify a 20% price hike."],
    "s4": ["Pro Tip: Max out 80 characters in eBay titles.", "Pro Tip: Relist items every 30 days for 'New' status.", "Pro Tip: Share closet at 9PM EST for peak activity.", "Pro Tip: Use seasonal keywords like 'Summer Essential'.", "Pro Tip: Never use stock photos alone; AI flags them.", "Pro Tip: Put top 5 SEO tags in description footer.", "Pro Tip: Use 'Expert' style for tech listings.", "Pro Tip: Respond within 5 mins on FB Marketplace.", "Pro Tip: Send offers within 10 mins of a 'Like'.", "Pro Tip: Combine shipping to encourage multi-buys."],
    "s5": ["Expert Partner: This Thermal Printer pays for itself.", "Sourcing Secret: Scales prevent shipping surcharges.", "Visual Power: Kill 'Yellow Tint' with lighting kits.", "Boutique Standard: Matte-black mailers win fans.", "Speed Logic: Steamers remove wrinkles 3x faster.", "Professional Edge: Items on mannequins sell 20% faster.", "Mandatory Tool: Accurate measurements for SEO.", "Volume Strategy: Bulk 6-pack tape saves $12.", "Efficiency Pro: Clear bin storage keeps inventory searchable.", "The Pro Finish: Thermal 4x labels look corporate."]
}

# --- 3. UI EXECUTION ---
st.markdown('<div style="margin-top:30px;"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text" style="font-size:18px;">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)

# STEP 1
st.markdown('<p class="step-label">STEP 1: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)
st.markdown(f'''<div class="suggestion-box"><span class="tip-tag" style="color: #0EA5E9;">📸 PRO TIP</span><p style="margin:0; font-weight:600;">{random.choice(TIP_POOL['s1'])}</p></div>''', unsafe_allow_html=True)
img_file = st.camera_input("Scanner", label_visibility="collapsed")

# STEP 2
st.markdown('<p class="step-label">STEP 2: <span class="neon-text">DESCRIBE</span></p>', unsafe_allow_html=True)
st.markdown(f'''<div class="reminder-box"><span class="tip-tag" style="color: #F59E0B;">📝 PRO TIP</span><p style="margin:0; font-weight:600;">{random.choice(TIP_POOL['s2'])}</p></div>''', unsafe_allow_html=True)
notes = st.text_area("Notes", key="notes_input", height=100, placeholder="Brand, Size, Condition...", label_visibility="collapsed")

# STEP 3
st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
st.markdown(f'''<div class="suggestion-box"><span class="tip-tag" style="color: #0EA5E9;">💰 PRO TIP</span><p style="margin:0; font-weight:600;">{random.choice(TIP_POOL['s3'])}</p></div>''', unsafe_allow_html=True)

if st.button("🚀 ANALYZE MARKET", type="primary", use_container_width=True):
    if img_file:
        with st.spinner("Brain Processing..."):
            # FIXED LINE 112: Converting image for google-genai compatibility
            image_data = {"mime_type": img_file.type, "data": img_file.getvalue()}
            response = client.models.generate_content(model=LITE_MODEL, contents=[notes, image_data])
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
st.markdown(f'''<div class="reminder-box"><span class="tip-tag" style="color: #F59E0B;">🚀 PRO TIP</span><p style="margin:0; font-weight:600;">{random.choice(TIP_POOL['s4'])}</p></div>''', unsafe_allow_html=True)

style = st.radio("Style", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")

# COLOR-LOCKED HTML GRID FOR STEP 4
st.markdown(f'''
    <div class="flex-grid">
        <a href="?platform=Facebook" class="m-btn" id="fb-blue">FB</a>
        <a href="?platform=eBay" class="m-btn" id="ebay-blue">EBAY</a>
        <a href="?platform=Craigslist" class="m-btn" id="cl-purple">CL</a>
        <a href="?platform=Poshmark" class="m-btn" id="posh-maroon">POSH</a>
    </div>
''', unsafe_allow_html=True)

# Query Parameter Listener
params = st.query_params
if "platform" in params:
    plat = params["platform"]
    with st.spinner(f"Writing {plat} Listing..."):
        res = client.models.generate_content(model=LITE_MODEL, contents=[f"Write a {style} {plat} listing: {notes}"])
        st.session_state.listing_out = res.text
        st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": notes[:30], "Platform": plat})
        st.query_params.clear()

st.text_area("Output", value=st.session_state.listing_out, height=150, label_visibility="collapsed")

# STEP 5
st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
st.markdown(f'''<div class="suggestion-box"><span class="tip-tag" style="color: #0EA5E9;">📦 PARTNER</span><p style="margin:0; font-weight:600;">{random.choice(TIP_POOL['s5'])}</p></div>''', unsafe_allow_html=True)
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
