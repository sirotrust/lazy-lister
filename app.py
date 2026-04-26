import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image

# --- 1. THE BRAIN (GOOGLE API PIVOT) ---
# This looks for your key in .streamlit/secrets.toml
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Missing Google API Key! Please add it to your secrets.toml file.")

def process_scan(image_data, notes, style):
    """The engine that replaces OpenRouter"""
    if image_data is None:
        return "Please take a photo first!"
    
    prompt = f"""
    You are a professional reseller expert. Analyze this image.
    User Notes: {notes}
    Listing Style: {style}
    
    Provide:
    1. A catchy SEO-optimized Title.
    2. A detailed description focusing on condition and brand.
    3. Suggested Market Price based on the item's appearance.
    """
    
    img = Image.open(image_data)
    response = model.generate_content([prompt, img])
    return response.text

# --- 2. THE ARCHITECTURAL ENGINE (CSS LOCK) ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }
    
    /* YOUR COLORS & CONTRAST LOCK */
    [data-testid="stRadio"] label, [data-testid="stRadio"] label p, [data-testid="stWidgetLabel"] p {
        color: #0F172A !important; font-weight: 800 !important;
    }
    [data-testid="stTable"] td, [data-testid="stTable"] th {
        color: #0F172A !important; background-color: #F8FAFC !important; font-weight: 600 !important;
    }
    [data-testid="stTextArea"] textarea {
        background-color: #F1F5F9 !important; color: #0F172A !important; font-weight: 600 !important;
        border: 2px solid #CBD5E1 !important; border-radius: 12px !important;
    }

    /* BOXES */
    .reminder-box { background-color: #FFFBEB !important; border-left: 6px solid #F59E0B !important; padding: 15px; border-radius: 12px; margin: 10px 0; }
    .suggestion-box { background-color: #F0F9FF !important; border-left: 6px solid #0EA5E9 !important; padding: 15px; border-radius: 12px; margin: 10px 0; }
    .tip-tag { font-weight: 900; font-size: 11px; text-transform: uppercase; display: block; }
    .tip-text { color: #1E293B !important; font-size: 14px; font-weight: 600; }

    /* BRANDING */
    .brand-word { color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; letter-spacing: -1px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    
    .step-label { color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; border-bottom: 3px solid #0F172A; display: inline-block; }
    .step-instruction { color: #64748B; font-size: 14px; font-weight: 700; display: block; margin-bottom: 10px; }

    /* BUTTONS */
    .flex-grid { display: flex; flex-wrap: nowrap; gap: 8px; width: 100%; margin: 10px 0; }
    .m-btn {
        flex: 1 !important; height: 60px !important; border-radius: 12px !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        text-decoration: none !important; color: white !important; font-weight: 950 !important; font-size: 12px !important; text-transform: uppercase !important;
    }
    #google-red { background-color: #CC0000 !important; }
    #amz-brown { background-color: #483332 !important; }
    #ebay-blue { background-color: #002F6C !important; }
    #fb-blue { background-color: #1877F2 !important; }
    #posh-maroon { background-color: #8C1B2F !important; }
    #copy-teal { background-color: #0D9488 !important; }
    #dl-indigo { background-color: #4338CA !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
st.markdown('''
    <div style="margin-top: 30px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <span class="brand-word">LAZY</span>
            <span style="font-size: 55px; margin-top: -25px;">🦥</span>
            <span class="brand-word">LISTER</span>
        </div>
        <span class="neon-text" style="font-size: 18px;">PREMIUM RESELLER ASSISTANT</span>
    </div>
''', unsafe_allow_html=True)

# --- 4. THE TABS ---
tab_studio, tab_inventory = st.tabs(["🚀 LISTING STUDIO", "📊 INVENTORY LOG"])

with tab_studio:
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<p class="step-label">STEP 1: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)
        img_file = st.camera_input("Scanner", label_visibility="collapsed")
        
        st.markdown('<p class="step-label">STEP 2: <span class="neon-text">DESCRIBE</span></p>', unsafe_allow_html=True)
        st.markdown('<span class="step-instruction">Describe silhouette and texture.</span>', unsafe_allow_html=True)
        notes = st.text_area("Notes", placeholder="Describe vibe, texture, fit.", height=150, key="notes_in", label_visibility="collapsed")

    with col2:
        st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
        
        # FUNCTIONAL ANALYZE BUTTON
        if st.button("🚀 ANALYZE MARKET", type="primary", use_container_width=True):
            if img_file:
                with st.spinner("AI analyzing item..."):
                    result = process_scan(img_file, notes, "Pro")
                    st.session_state["output_text"] = result
            else:
                st.warning("Take a photo first!")

        st.markdown('<div class="flex-grid"><a href="#" class="m-btn" id="ebay-blue">EBAY</a><a href="#" class="m-btn" id="amz-brown">AMAZON</a><a href="#" class="m-btn" id="google-red">GOOGLE</a><a href="#" class="m-btn" id="posh-maroon">POSHMARK</a></div>', unsafe_allow_html=True)

        st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
        selected_style = st.radio("STYLE:", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")
        
        # Display the AI output
        st.text_area("Output", value=st.session_state.get("output_text", ""), height=250, key="out_in", label_visibility="collapsed")
        st.button("📋 COPY LISTING", use_container_width=True)

with tab_inventory:
    st.markdown('<p class="step-label">YOUR INVENTORY</p>', unsafe_allow_html=True)
    
    if 'inventory' not in st.session_state or len(st.session_state.inventory) == 0:
        st.markdown('''<div class="reminder-box"><span class="tip-tag" style="color: #F59E0B;">🦥 STILL EMPTY</span><p class="tip-text">Start scanning in the "Listing Studio" to build your inventory.</p></div>''', unsafe_allow_html=True)
    
    if st.button("🗑️ RESET SESSION", use_container_width=True):
        st.session_state.clear(); st.rerun()