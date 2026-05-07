import streamlit as st
import pandas as pd
from google import genai
from google.genai import types
import random

# --- 1. THE CONNECTION ENGINE ---
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("API Connection Error.")

# --- 2. THE MASTER 50-TIP NEURAL LIBRARY (DESIGNATED LOCK) ---
TIP_POOL = {
    "s1": ["Pro Tip: Use the rear-facing lens for 40% higher resolution.", "Pro Tip: Lock focus (AE/AF) by holding the screen.", "Pro Tip: Natural light between 10am-2pm is best.", "Pro Tip: Turn on gridlines for perfect leveling.", "Pro Tip: Move closer; never use digital zoom.", "Pro Tip: Clean your lens before every session.", "Pro Tip: Use white backgrounds for AI edge detection.", "Pro Tip: Shoot the care tag for fabric verification.", "Pro Tip: Use white board to reflect light into shadows.", "Pro Tip: Shoot shoes at a 45-degree hero angle."],
    "s2": ["Pro Tip: Place Brand and Model in the first 3 words.", "Pro Tip: Use words like 'buttery' or 'structured'.", "Pro Tip: Mention 'Smoke-Free' to build buyer trust.", "Pro Tip: List Pit-to-pit, Length, and Sleeve measurements.", "Pro Tip: Use 'texture' keywords like 'slubby' or 'brushed'.", "Pro Tip: Define the Vibe: Is it Gorpcore or Minimalist?", "Pro Tip: Find the model code on the internal tag.", "Pro Tip: Disclose pilling early to reduce returns.", "Pro Tip: Use 'Azure' or 'Cobalt' instead of just 'Blue'.", "Pro Tip: Mention hardware quality for premium items."],
    "s3": ["Pro Tip: Check 'Sold' listings, not 'Active' ones.", "Pro Tip: Price 10% high to allow for negotiations.", "Pro Tip: $24.99 converts 15% better than $25.00.", "Pro Tip: Weigh items before pricing to calculate shipping.", "Pro Tip: Cross-reference eBay vs Poshmark for averages.", "Pro Tip: Free Shipping tags increase filter hits by 2x.", "Pro Tip: Price vintage on rarity, not just fashion.", "Pro Tip: Drop prices by 10% on Friday afternoons.", "Pro Tip: High-demand brands follow strict MSRP logic.", "Pro Tip: High-quality photos justify a 20% price hike."],
    "s4": ["Pro Tip: Max out the 80 characters in eBay titles.", "Pro Tip: Relist items every 30 days for 'New' status.", "Pro Tip: Share your Poshmark closet at 9PM EST.", "Pro Tip: Use seasonal keywords like 'Summer Essential'.", "Pro Tip: Never use stock photos alone; AI flags them.", "Pro Tip: Put top 5 SEO tags in the description footer.", "Pro Tip: Use 'Expert' style for tech listings.", "Pro Tip: Respond within 5 mins on FB Marketplace.", "Pro Tip: Send offers within 10 mins of a 'Like'.", "Pro Tip: Combine shipping to encourage multi-buys."],
    "s5": ["Helpful Suggestion: This Thermal Printer pays for itself. [View Setup]", "Efficiency Upgrade: Scales prevent shipping surcharges. [Secure Yours]", "Visual Advantage: Lighting kits kill yellow tints. [See My Set]", "Boutique Standard: Matte-black mailers win repeat fans. [Shop Bulk]", "Speed Strategy: Steamers remove wrinkles 3x faster. [Check Price]", "Reseller Essential: Forms sell 20% faster than flat-lays. [Check Price]", "Precision Tool: Retractable tape is mandatory for SEO. [See My Pick]", "Workflow Secret: Bulk 6-pack tape saves $12 monthly. [Stock Up]", "Organization Pro: Clear bins keep inventory searchable. [Explore Bins]", "Pro-Level Finish: 4x6 labels give a corporate look. [Shop Labels]"]
}

def get_random_tip(step_id):
    return random.choice(TIP_POOL.get(step_id, ["Synchronizing..."]))

# --- 3. BRAIN LOGIC ---
def analyze_market_logic(img_file, description):
    if not img_file and not description: return "Need data!"
    try:
        content_parts = []
        if img_file:
            content_parts.append(types.Part.from_bytes(data=img_file.getvalue(), mime_type=img_file.type))
        prompt = f"Expert Reseller Market Analysis. Notes: {description}. Value and Keywords."
        content_parts.append(types.Part.from_text(text=prompt))
        return client.models.generate_content(model="gemini-2.0-flash", contents=content_parts).text
    except Exception as e: return f"Brain Error: {str(e)}"

def generate_listing(platform, details, style):
    if not details: return "Enter details in Step 2!"
    try:
        prompt = f"Write a professional {platform} listing in {style} style: {details}"
        return client.models.generate_content(model="gemini-2.0-flash", contents=prompt).text
    except Exception as e: return f"Error: {str(e)}"

# --- 4. THE ARCHITECTURAL ENGINE (UNIFIED HTML/CSS DESIGN LOCK) ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }

    /* HEADER & TEXT */
    .brand-word { color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }
    .sloth-anchor { font-size: 55px; margin-top: -25px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .step-label { color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; margin-top: 30px; border-bottom: 3px solid #0F172A; display: inline-block; }

    /* BOXES */
    .reminder-box, .suggestion-box { padding: 15px; border-radius: 12px; margin: 10px 0; border: 1px solid; }
    .reminder-box { background-color: #FFFBEB !important; border-left: 6px solid #F59E0B !important; border-color: #FEF3C7; }
    .suggestion-box { background-color: #F0F9FF !important; border-left: 6px solid #0EA5E9 !important; border-color: #E0F2FE; }
    .tip-tag { font-weight: 950; font-size: 11px; text-transform: uppercase; display: block; }
    .tip-text { color: #1E293B !important; font-size: 14px; font-weight: 600; line-height: 1.4; }

    /* UNIFIED HTML BUTTON GRID */
    .flex-grid { display: flex; flex-wrap: nowrap; gap: 8px; width: 100%; margin: 10px 0; }
    .m-btn {
        flex: 1 !important; height: 60px !important; border-radius: 12px !important; display: flex !important; align-items: center !important; justify-content: center !important;
        text-decoration: none !important; color: white !important; font-weight: 950 !important; font-size: 12px !important; text-transform: uppercase !important; line-height: 60px !important; border: none !important; cursor: pointer !important;
    }

    /* MODERN ICON PALETTE */
    .fb-blue { background-color: #1877F2 !important; }
    .ebay-blue { background-color: #002F6C !important; }
    .cl-purple { background-color: #502189 !important; }
    .posh-maroon { background-color: #8C1B2F !important; }
    .google-red { background-color: #CC0000 !important; }
    .amz-brown { background-color: #483332 !important; }
    
    /* UTILITY COLORS */
    .utility-clear { background-color: #334155 !important; } /* Charcoal */
    .utility-copy { background-color: #059669 !important; } /* Emerald */
    .utility-reset { background-color: #94A3B8 !important; } /* Slate */

    /* HIDE NATIVE BUTTONS */
    .stButton > button { display: none !important; }

    /* TEXT AREA */
    [data-testid="stTextArea"] textarea { background-color: #F1F5F9 !important; color: #000000 !important; font-weight: 600 !important; border: 2px solid #CBD5E1 !important; border-radius: 12px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 5. UI LAYOUT ---
st.markdown('<div style="margin-top:30px;"><div style="display: flex; align-items: center; gap: 12px;"><span class="brand-word">LAZY</span><span class="sloth-anchor">🦥</span><span class="brand-word">LISTER</span></div><span class="neon-text" style="font-size:18px;">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<p class="step-label">STEP 1: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)
    st.markdown(f'<div class="suggestion-box"><span class="tip-tag" style="color:#0EA5E9;">📸 PRO TIP</span><p class="tip-text">{get_random_tip("s1")}</p></div>', unsafe_allow_html=True)
    img_file = st.camera_input("Scanner", label_visibility="collapsed")
    
    st.markdown('<p class="step-label">STEP 2: <span class="neon-text">DESCRIBE</span></p>', unsafe_allow_html=True)
    st.markdown(f'<div class="reminder-box"><span class="tip-tag" style="color:#F59E0B;">📝 PRO TIP</span><p class="tip-text">{get_random_tip("s2")}</p></div>', unsafe_allow_html=True)
    notes_input = st.text_area("Notes", placeholder="buttery, chunky, structured...", height=150, key="notes_input", label_visibility="collapsed")
    
    # HTML CLEAR BUTTON
    st.markdown(f'''<div class="flex-grid">
        <a href="/?action=clear" target="_self" class="m-btn utility-clear">🗑️ CLEAR DESCRIPTION</a>
    </div>''', unsafe_allow_html=True)

with col2:
    st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
    st.markdown(f'<div class="suggestion-box"><span class="tip-tag" style="color:#0EA5E9;">💰 PRO TIP</span><p class="tip-text">{get_random_tip("s3")}</p></div>', unsafe_allow_html=True)
    
    # HTML ANALYZE BUTTON
    st.markdown(f'''<div class="flex-grid">
        <a href="/?action=analyze" target="_self" class="m-btn google-red">🚀 ANALYZE MARKET</a>
    </div>''', unsafe_allow_html=True)
    if st.session_state.get("market_analysis"): st.info(st.session_state.market_analysis)

    st.markdown(f'''<div class="flex-grid">
        <a href="https://www.ebay.com/sch/i.html?_nkw={notes_input}" target="_blank" class="m-btn ebay-blue">EBAY</a>
        <a href="https://www.amazon.com/s?k={notes_input}" target="_blank" class="m-btn amz-brown">AMAZON</a>
        <a href="https://www.google.com/search?q={notes_input}" target="_blank" class="m-btn google-red">GOOGLE</a>
        <a href="https://poshmark.com/search?query={notes_input}" target="_blank" class="m-btn posh-maroon">POSHMARK</a>
    </div>''', unsafe_allow_html=True)

    st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
    st.markdown(f'<div class="reminder-box"><span class="tip-tag" style="color:#F59E0B;">🚀 PRO TIP</span><p class="tip-text">{get_random_tip("s4")}</p></div>', unsafe_allow_html=True)
    selected_style = st.radio("STYLE:", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")
    
    # HTML STEP 4 GRID
    st.markdown(f'''<div class="flex-grid">
        <a href="/?platform=Facebook" target="_self" class="m-btn fb-blue">📱 FB</a>
        <a href="/?platform=eBay" target="_self" class="m-btn ebay-blue">📦 EBAY</a>
        <a href="/?platform=Craigslist" target="_self" class="m-btn cl-purple">🏘️ CL</a>
        <a href="/?platform=Poshmark" target="_self" class="m-btn posh-maroon">👗 POSH</a>
    </div>''', unsafe_allow_html=True)

    st.text_area("Output", value=st.session_state.get('listing_out', ''), height=150, key="output_area", label_visibility="collapsed")
    
    # HTML COPY BUTTON
    st.markdown(f'''<div class="flex-grid">
        <a href="/?action=copy" target="_self" class="m-btn utility-copy">📋 COPY LISTING</a>
    </div>''', unsafe_allow_html=True)

    st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
    st.markdown(f'<div class="suggestion-box"><span class="tip-tag" style="color:#0EA5E9;">🤝 YOUR EXPERT PARTNER</span><p class="tip-text">{get_random_tip("s5")}</p></div>', unsafe_allow_html=True)
    st.markdown('''<div class="flex-grid">
        <a href="YOUR_LINK" target="_blank" class="m-btn google-red">🔍 GOOGLE SHOP</a>
        <a href="YOUR_LINK" target="_blank" class="m-btn amz-brown">🛡️ AMAZON PRO</a>
    </div>''', unsafe_allow_html=True)

# RESET SESSION
st.markdown(f'''<div class="flex-grid" style="margin-top:50px;">
    <a href="/?action=reset" target="_self" class="m-btn utility-reset">🔄 RESET SESSION</a>
</div>''', unsafe_allow_html=True)

# THE BRAIN BRIDGE: Catching HTML clicks via URL
params = st.query_params
if "action" in params:
    act = params["action"]
    if act == "clear": st.session_state.notes_input = ""; st.rerun()
    if act == "analyze": st.session_state.market_analysis = analyze_market_logic(img_file, notes_input)
    if act == "reset": st.session_state.clear(); st.rerun()
    st.query_params.clear()

if "platform" in params:
    st.session_state.listing_out = generate_listing(params["platform"], notes_input, selected_style)
    st.query_params.clear()
