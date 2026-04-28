import streamlit as st
import pandas as pd
from google import genai

# --- 1. THE CONNECTION ENGINE (GOOGLE BRAIN) ---
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("API Key not found in secrets.toml.")

# --- 2. THE ARCHITECTURAL ENGINE (ULTRA-CONTRAST CSS) ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

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
    
    [data-testid="stTextArea"] textarea::placeholder {
        color: #64748B !important;
    }

    /* ZONE 4: NOTIFICATION BOXES */
    .reminder-box { 
        background-color: #FFFBEB !important; 
        border-left: 6px solid #F59E0B !important; 
        padding: 15px; border-radius: 12px; margin: 10px 0; border: 1px solid #FEF3C7;
    }
    .suggestion-box { 
        background-color: #F0F9FF !important; 
        border-left: 6px solid #0EA5E9 !important; 
        padding: 15px; border-radius: 12px; margin: 10px 0; border: 1px solid #E0F2FE;
    }
    .tip-tag { font-weight: 900; font-size: 11px; text-transform: uppercase; display: block; margin-bottom: 2px; }
    .tip-text { color: #1E293B !important; font-size: 14px; font-weight: 600; line-height: 1.4; }

    /* ZONE 5: HEADER & NEON */
    .header-wrapper { margin-top: 30px; margin-bottom: 40px; }
    .title-container { display: flex; align-items: center; gap: 12px; }
    .brand-word { color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; margin: 0; letter-spacing: -1px; }
    .sloth-anchor { font-size: 55px; margin-top: -25px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .neon-sub { font-size: 18px; margin-top: 10px; display: block; }

    .step-label { color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; margin-top: 30px; border-bottom: 3px solid #0F172A; display: inline-block; }
    .step-instruction { color: #64748B; font-size: 14px; font-weight: 700; margin-top: 5px; margin-bottom: 10px; display: block; }

    /* ZONE 6: BUTTONS */
    .flex-grid { display: flex; flex-wrap: nowrap; gap: 8px; width: 100%; margin: 10px 0; }
    .m-btn {
        flex: 1 !important; height: 60px !important; border-radius: 12px !important;
        display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: center !important;
        text-decoration: none !important; color: white !important; font-weight: 950 !important; font-size: 12px !important;
        text-transform: uppercase !important; text-align: center !important; line-height: 60px !important;
    }
    #google-red { background-color: #CC0000 !important; }
    #amz-brown { background-color: #483332 !important; }
    #ebay-blue { background-color: #002F6C !important; }
    #fb-blue { background-color: #1877F2 !important; }
    #cl-purple { background-color: #502189 !important; }
    #posh-maroon { background-color: #8C1B2F !important; }
    #copy-teal { background-color: #0D9488 !important; }
    #dl-indigo { background-color: #4338CA !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. THE "BRAIN" LISTENER ---
if 'listing_cache' not in st.session_state:
    st.session_state.listing_cache = ""

query_params = st.query_params
if "p" in query_params:
    target_platform = query_params["p"]
    user_notes = st.session_state.get("notes_input", "")
    current_style = st.session_state.get("selected_style_val", "Simple")
    
    if user_notes:
        prompt = f"Write a professional {target_platform} listing. Style: {current_style}. Details: {user_notes}"
        try:
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            st.session_state.listing_cache = response.text
        except:
            st.session_state.listing_cache = "Error generating listing."
    else:
        st.session_state.listing_cache = "Please enter notes in Step 2 first!"

# --- 4. HEADER ---
st.markdown('''
    <div class="header-wrapper">
        <div class="title-container">
            <span class="brand-word">LAZY</span>
            <span class="sloth-anchor">🦥</span>
            <span class="brand-word">LISTER</span>
        </div>
        <span class="neon-text neon-sub">PREMIUM RESELLER ASSISTANT</span>
    </div>
''', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<p class="step-label">STEP 1: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)
    st.markdown('<span class="step-instruction">Switch to back camera for high-res detail.</span>', unsafe_allow_html=True)
    st.camera_input("Scanner", label_visibility="collapsed")
    
    st.markdown('<p class="step-label">STEP 2: <span class="neon-text">DESCRIBE</span></p>', unsafe_allow_html=True)
    st.markdown('<span class="step-instruction">No logo? Describe silhouette and texture for fallback logic.</span>', unsafe_allow_html=True)
    st.text_area("Notes", placeholder="Describe vibe, texture, fit. Use sensory words: 'buttery,' 'chunky,' 'structured.'", height=150, key="notes_input", label_visibility="collapsed")
    st.button("🗑️ CLEAR DESCRIPTION", use_container_width=True)

with col2:
    st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
    st.button("🚀 ANALYZE MARKET", type="primary", use_container_width=True)
    st.markdown('''
        <div class="flex-grid">
            <a href="https://www.ebay.com" target="_blank" class="m-btn" id="ebay-blue">EBAY</a>
            <a href="https://www.amazon.com" target="_blank" class="m-btn" id="amz-brown">AMAZON</a>
            <a href="https://www.google.com" target="_blank" class="m-btn" id="google-red">GOOGLE</a>
            <a href="https://poshmark.com" target="_blank" class="m-btn" id="posh-maroon">POSHMARK</a>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
    st.radio("STYLE:", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed", key="selected_style_val")
    
    style_reminders = {
        "Simple": "Quick-flip mode. Optimized for short attention spans.",
        "Expert": "SEO Heavy. Focuses on tech specs and condition keywords.",
        "Pro": "Boutique Storytelling. Highlights heritage and styling potential."
    }
    selected_rem = style_reminders.get(st.session_state.selected_style_val, "")
    st.markdown(f'''<div class="reminder-box"><span class="tip-tag" style="color: #F59E0B;">🔔 STYLE REMINDER</span><p class="tip-text">{selected_rem}</p></div>''', unsafe_allow_html=True)

    st.markdown('''
        <div class="flex-grid">
            <a href="/?p=Facebook" target="_self" class="m-btn" id="fb-blue">FACEBOOK</a>
            <a href="/?p=eBay" target="_self" class="m-btn" id="ebay-blue">EBAY</a>
            <a href="/?p=Craigslist" target="_self" class="m-btn" id="cl-purple">C-LIST</a>
            <a href="/?p=Poshmark" target="_self" class="m-btn" id="posh-maroon">POSHMARK</a>
        </div>
    ''', unsafe_allow_html=True)
    st.text_area("Output", value=st.session_state.listing_cache, placeholder="Select a platform above to craft your listing.", height=150, key="output_input", label_visibility="collapsed")
    st.button("📋 COPY LISTING", use_container_width=True)

    st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
    st.markdown('<span class="step-instruction">Order packaging materials below.</span>', unsafe_allow_html=True)
    st.markdown('''<div class="suggestion-box"><span class="tip-tag" style="color: #0EA5E9;">📦 PRO-TIP</span><p class="tip-text">Branded mailers increase repeat buyer rates by 15%.</p></div>''', unsafe_allow_html=True)
    st.markdown('''
        <div class="flex-grid">
            <a href="https://shopping.google.com" target="_blank" class="m-btn" id="google-red">GOOGLE SHOP</a>
            <a href="https://www.amazon.com" target="_blank" class="m-btn" id="amz-brown">AMAZON PRO</a>
        </div>
    ''', unsafe_allow_html=True)

# --- 5. INVENTORY LOG ---
st.divider()
st.markdown('<p class="step-label">INVENTORY LOG</p>', unsafe_allow_html=True)

if 'inventory' not in st.session_state or len(st.session_state.inventory) == 0:
    ghost_data = pd.DataFrame({
        "Item": ["Your scanned inventory will be logged here automatically..."],
        "Platform": ["Syncing"],
        "Price": ["--"]
    })
    st.table(ghost_data)
else:
    st.table(st.session_state.inventory)

st.markdown('''
    <div class="flex-grid">
        <a href="#" class="m-btn" id="copy-teal">📋 COPY DATA</a>
        <a href="#" class="m-btn" id="dl-indigo">📥 DOWNLOAD CSV</a>
    </div>
''', unsafe_allow_html=True)

st.markdown('''<div class="suggestion-box"><span class="tip-tag" style="color: #0EA5E9;">🧠 AI STRATEGY</span><p class="tip-text">Resellers who export their data weekly to CSV are 40% more likely to accurately forecast tax deductions and profit margins.</p></div>''', unsafe_allow_html=True)

if st.button("🗑️ RESET SESSION", use_container_width=True):
    st.session_state.clear(); st.rerun()
