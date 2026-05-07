import streamlit as st
import pandas as pd
from google import genai
from google.genai import types
import random
import time

# --- 1. THE CONNECTION ENGINE ---
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("API Key not found. Check secrets.toml.")

# --- 2. THE MASTER 50-TIP PRO LIBRARY (DATA-DRIVEN) ---
TIP_POOL = {
    "s1": [
        "Pro Tip: Clean your lens with a microfiber cloth before every shoot.",
        "Pro Tip: Shoot at a 45-degree 'hero' angle to show depth and scale.",
        "Pro Tip: Use the 'Portrait Mode' on modern phones to blur busy backgrounds.",
        "Pro Tip: Always photograph the care tag; buyers search for fabric content.",
        "Pro Tip: Use a white foam board as a reflector to bounce light into shadows.",
        "Pro Tip: Capture 'Scale' by placing a coin or ruler next to small items.",
        "Pro Tip: Shoot 'Flat Lays' from directly above to avoid perspective distortion.",
        "Pro Tip: Use a lint roller on every fabric item before the first shutter click.",
        "Pro Tip: Turn off overhead yellow lights; stick to pure natural window light.",
        "Pro Tip: Highlight 'Imperfections' with a pointer to build immediate trust."
    ],
    "s2": [
        "Pro Tip: Front-load your title with Brand + Model + Size for SEO.",
        "Pro Tip: Use 'NWT' (New With Tags) or 'EUC' (Excellent Used Condition) in titles.",
        "Pro Tip: List three specific measurements: Pit-to-pit, length, and sleeve.",
        "Pro Tip: Use 'texture' keywords like 'slubby,' 'pebbled,' or 'brushed'.",
        "Pro Tip: Mention if an item comes from a 'Smoke-Free' or 'Pet-Free' home.",
        "Pro Tip: Add a 'Style Note' on how to wear the item to inspire the buyer.",
        "Pro Tip: Define the 'Vibe': Is it Gorpcore, Dark Academia, or Streetwear?.",
        "Pro Tip: Use the 'Model Code' from the tag to find professional stock info.",
        "Pro Tip: Be specific about color; use 'Cobalt' instead of just 'Blue'.",
        "Pro Tip: Mention 'Stitch Detail' or 'Quality Hardware' for luxury items."
    ],
    "s3": [
        "Pro Tip: Check 'Sold' listings, then price 10% higher for negotiation room.",
        "Pro Tip: Items listed at $24.99 sell 15% faster than those at $25.00.",
        "Pro Tip: Use 'Promoted Listings' at 2% to jump to the top of eBay search.",
        "Pro Tip: Calculate shipping *before* you price; heavy coats eat margins.",
        "Pro Tip: Cross-reference 'Poshmark' vs 'eBay' prices for a true market average.",
        "Pro Tip: Items with 'Free Shipping' tags get 2x more visibility in filters.",
        "Pro Tip: Price vintage items based on decade and rarity, not just condition.",
        "Pro Tip: Drop prices by 10% on Fridays when buyers receive their paychecks.",
        "Pro Tip: High-demand brands (Nike, Lululemon) follow strict MSRP-logic.",
        "Pro Tip: Don't chase the bottom; if your photos are better, price higher."
    ],
    "s4": [
        "Pro Tip: Relist items every 30 days to keep 'New Listing' algorithm status.",
        "Pro Tip: Use all 80 characters in eBay; the algorithm hates empty space.",
        "Pro Tip: Share your Poshmark closet at 9PM EST for peak buyer activity.",
        "Pro Tip: Include 'Gifts for Him/Her' during holiday seasons for SEO.",
        "Pro Tip: Never use stock photos alone; platforms de-prioritize them.",
        "Pro Tip: Copy-paste your top tags into the bottom of the description.",
        "Pro Tip: Offer 'Combined Shipping' to encourage multi-item purchases.",
        "Pro Tip: Use 'Expert' style for high-end tech to show technical knowledge.",
        "Pro Tip: On Facebook, respond within 5 mins to keep your 'Responsive' badge.",
        "Pro Tip: Use 'Simple' style for fast-moving trendy items like mall brands."
    ],
    "s5": [
        "Affiliate Suggestion: Stop overpaying for ink. This Thermal Printer pays for itself in 3 months. [View Deal].",
        "Affiliate Suggestion: Precision scales prevent $5 USPS 'Underweight' surcharges. [Get My Scale].",
        "Affiliate Suggestion: Professional Softboxes kill 'Yellow Tint' in photos instantly. [See My Set].",
        "Affiliate Suggestion: These Matte-Black Polymailers win repeat boutique buyers. [Shop Bulk].",
        "Affiliate Suggestion: Items on a Mannequin sell 20% faster than flat-lays. [Check Current Price].",
        "Affiliate Suggestion: Retractable Fabric Measures are mandatory for SEO listing. [Get One Here].",
        "Affiliate Suggestion: Bulk 6-pack Shipping Tape saves $12 over single rolls. [Stock Up Now].",
        "Affiliate Suggestion: Clear Bin Storage keeps inventory dust-free and searchable. [Shop Bins].",
        "Affiliate Suggestion: Use a Dymo for high-volume 4x6 label professional looks. [See Deals].",
        "Affiliate Suggestion: Ring Lights provide consistent 'Eyes' reflection for jewelry. [Shop Top Picks]."
    ]
}

def get_random_tip(step_id):
    """Pulls zero-quota advice from the local pool."""
    return random.choice(TIP_POOL.get(step_id, ["Analyzing market trends..."]))

def analyze_market_logic(img_file, description):
    """Comparative Engine: Photo first, Text fallback."""
    if not img_file and not description:
        return "Need a photo or description!"
    try:
        content_parts = []
        if img_file:
            content_parts.append(types.Part.from_bytes(data=img_file.getvalue(), mime_type=img_file.type))
        prompt = f"Expert Reseller. Analyze photo or notes: '{description}'. Provide: Value, Demand, and Top 3 Comparative Keywords."
        content_parts.append(types.Part.from_text(text=prompt))
        response = client.models.generate_content(model="gemini-2.0-flash", contents=content_parts)
        return response.text
    except Exception as e:
        return f"Brain Error: {str(e)}"

def generate_listing(platform, details, style):
    if not details: return "Please enter details in Step 2 first!"
    try:
        prompt = f"Write a professional {platform} listing. Style: {style}. Details: {details}."
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def clear_text_callback():
    st.session_state["notes_input"] = ""
    st.session_state["listing_out"] = ""
    if "market_analysis" in st.session_state:
        st.session_state["market_analysis"] = ""

# --- 3. ARCHITECTURAL ENGINE (CSS LOCK) ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")
st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }
    [data-testid="stRadio"] label, [data-testid="stRadio"] label p, [data-testid="stWidgetLabel"] p {
        color: #0F172A !important; font-weight: 800 !important;
    }
    [data-testid="stTextArea"] textarea {
        background-color: #F1F5F9 !important; color: #000000 !important; font-weight: 600 !important; border: 2px solid #CBD5E1 !important; border-radius: 12px !important;
    }
    .reminder-box, .suggestion-box { padding: 15px; border-radius: 12px; margin: 10px 0; border: 1px solid; }
    .reminder-box { background-color: #FFFBEB !important; border-left: 6px solid #F59E0B !important; border-color: #FEF3C7; }
    .suggestion-box { background-color: #F0F9FF !important; border-left: 6px solid #0EA5E9 !important; border-color: #E0F2FE; }
    .tip-tag { font-weight: 950; font-size: 11px; text-transform: uppercase; display: block; margin-bottom: 2px; }
    .tip-text { color: #1E293B !important; font-size: 14px; font-weight: 600; line-height: 1.4; }
    .header-wrapper { margin-top: 30px; margin-bottom: 40px; }
    .brand-word { color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .step-label { color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; margin-top: 30px; border-bottom: 3px solid #0F172A; display: inline-block; }
    
    .stButton > button { border-radius: 12px !important; height: 60px !important; font-weight: 950 !important; text-transform: uppercase !important; border: none !important; color: white !important; width: 100% !important; }
    div[data-testid="column"]:nth-of-type(1) div[data-testid="stButton"] button { background-color: #1877F2 !important; }
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"] button { background-color: #002F6C !important; }
    div[data-testid="column"]:nth-of-type(3) div[data-testid="stButton"] button { background-color: #502189 !important; }
    div[data-testid="column"]:nth-of-type(4) div[data-testid="stButton"] button { background-color: #8C1B2F !important; }
    
    .m-btn {
        flex: 1 !important; height: 60px !important; border-radius: 12px !important; display: flex !important; align-items: center !important; justify-content: center !important;
        text-decoration: none !important; color: white !important; font-weight: 950 !important; font-size: 12px !important; text-transform: uppercase !important; text-align: center !important; line-height: 60px !important;
    }
    #google-red { background-color: #CC0000 !important; }
    #amz-brown { background-color: #483332 !important; }
    #ebay-blue { background-color: #002F6C !important; }
    #posh-maroon { background-color: #8C1B2F !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. UI LAYOUT ---
st.markdown(f'''<div class="header-wrapper"><div class="title-container"><span class="brand-word">LAZY</span><span class="sloth-anchor">🦥</span><span class="brand-word">LISTER</span></div><span class="neon-text" style="font-size:18px;">PREMIUM RESELLER ASSISTANT</span></div>''', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<p class="step-label">STEP 1: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)
    st.markdown(f'''<div class="suggestion-box"><span class="tip-tag" style="color:#0EA5E9;">📸 PRO TIP</span><p class="tip-text">{get_random_tip("s1")}</p></div>''', unsafe_allow_html=True)
    img_file = st.camera_input("Scanner", label_visibility="collapsed")
    
    st.markdown('<p class="step-label">STEP 2: <span class="neon-text">DESCRIBE</span></p>', unsafe_allow_html=True)
    st.markdown(f'''<div class="reminder-box"><span class="tip-tag" style="color:#F59E0B;">📝 PRO TIP</span><p class="tip-text">{get_random_tip("s2")}</p></div>''', unsafe_allow_html=True)
    notes_input = st.text_area("Notes", placeholder="buttery, chunky, structured...", height=150, key="notes_input", label_visibility="collapsed")
    st.button("🗑️ CLEAR DESCRIPTION", use_container_width=True, on_click=clear_text_callback)

with col2:
    st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
    st.markdown(f'''<div class="suggestion-box"><span class="tip-tag" style="color:#0EA5E9;">💰 PRO TIP</span><p class="tip-text">{get_random_tip("s3")}</p></div>''', unsafe_allow_html=True)
    if st.button("🚀 ANALYZE MARKET", type="primary", use_container_width=True):
        st.session_state.market_analysis = analyze_market_logic(img_file, notes_input)
    if st.session_state.get("market_analysis"):
        st.info(st.session_state.market_analysis)

    st.markdown(f'''<div style="display:flex; gap:8px; margin:8px 0;">
        <a href="https://www.ebay.com/sch/i.html?_nkw={st.session_state.get('notes_input', '')}" target="_blank" class="m-btn" id="ebay-blue">EBAY</a>
        <a href="https://www.amazon.com/s?k={st.session_state.get('notes_input', '')}" target="_blank" class="m-btn" id="amz-brown">AMAZON</a>
        <a href="https://www.google.com/search?q={st.session_state.get('notes_input', '')}" target="_blank" class="m-btn" id="google-red">GOOGLE</a>
        <a href="https://poshmark.com/search?query={st.session_state.get('notes_input', '')}" target="_blank" class="m-btn" id="posh-maroon">POSHMARK</a>
    </div>''', unsafe_allow_html=True)

    st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
    st.markdown(f'''<div class="reminder-box"><span class="tip-tag" style="color:#F59E0B;">🚀 PRO TIP</span><p class="tip-text">{get_random_tip("s4")}</p></div>''', unsafe_allow_html=True)
    selected_style = st.radio("STYLE:", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")
    p1, p2, p3, p4 = st.columns(4)
    if p1.button("FB"): st.session_state.listing_out = generate_listing("Facebook", notes_input, selected_style)
    if p2.button("EBAY"): st.session_state.listing_out = generate_listing("eBay", notes_input, selected_style)
    if p3.button("CL"): st.session_state.listing_out = generate_listing("Craigslist", notes_input, selected_style)
    if p4.button("POSH"): st.session_state.listing_out = generate_listing("Poshmark", notes_input, selected_style)
    st.text_area("Output", value=st.session_state.get('listing_out', ''), height=150, key="output_area", label_visibility="collapsed")
    st.button("📋 COPY LISTING", use_container_width=True)

    st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
    st.markdown(f'''<div class="suggestion-box"><span class="tip-tag" style="color:#0EA5E9;">📦 AFFILIATE DEALS</span><p class="tip-text">{get_random_tip("s5")}</p></div>''', unsafe_allow_html=True)
    st.markdown(f'''<div style="display:flex; gap:8px; margin:8px 0;">
        <a href="YOUR_GOOGLE_AFFILIATE_LINK" target="_blank" class="m-btn" id="google-red">SHOP</a>
        <a href="YOUR_AMAZON_AFFILIATE_LINK" target="_blank" class="m-btn" id="amz-brown">PRO</a>
    </div>''', unsafe_allow_html=True)

if st.button("🗑️ RESET SESSION", use_container_width=True):
    st.session_state.clear(); st.rerun()
