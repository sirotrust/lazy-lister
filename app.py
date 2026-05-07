import streamlit as st
import pandas as pd
from google import genai
from google.genai import types
import random
import time

# --- 1. THE CONNECTION ENGINE (THE BRAIN) ---
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("API Key not found. Check secrets.toml.")

# --- 2. THE MASTER 50-TIP NEURAL LIBRARY ---
TIP_POOL = {
    "s1": [
        "Rear-Lens Superiority: Use the back camera for higher resolution.",
        "Exposure Locking: Hold the screen to lock focus and lighting.",
        "The Grid Rule: Use camera gridlines to center products perfectly.",
        "Natural Window Light: Shoot between 10 AM and 2 PM for true colors.",
        "No Digital Zoom: Physically move closer to maintain pixel detail.",
        "Rule of Thirds: Place logos at grid intersections for pro looks.",
        "White Balance: Use a plain white background for better AI detection.",
        "Shadow Control: Use white board to reflect light into dark spots.",
        "Macro Detail: Get within 4 inches for jewelry or weave shots.",
        "Consistent Angle: Shoot shoes at 45-degrees for a shoppable look."
    ],
    "s2": [
        "Brand Front-Loading: Place the brand name in the first 3 words.",
        "Sensory Keywords: Use 'buttery' or 'chunky' to sell the feel.",
        "Condition Transparency: Mention fading early to reduce returns.",
        "Material Logic: '100% Wool' is a top-tier SEO search trigger.",
        "Aesthetic Appeal: Use 'boho' or 'minimalist' for better reach.",
        "Measurement Inclusion: List pit-to-pit to answer buyers fast.",
        "Flaw Disclosure: Photos of stains build massive buyer trust.",
        "Style Codes: Find the model number on the small internal tag.",
        "Seasonality: Label as 'Spring-Ready' to match current trends.",
        "Fabric Care: Mention if it is 'Machine Washable' or 'Dry Clean'."
    ],
    "s3": [
        "The ROI Goal: Target 100%+ ROI after fees and shipping.",
        "Sold-Listing Logic: Base prices on Solds, not active asks.",
        "Off-Season Arbitrage: Buy winter gear in summer for high margins.",
        "USA Premium: 'Made in USA' vintage commands 50% higher prices.",
        "90-Day Velocity: If unsold in 90 days, drop price by 15%.",
        "Bundle Discounts: Offer 15% off for 2+ items to clear stock.",
        "Psychological Pricing: $29.99 often beats flat numbers.",
        "Shipping Buffer: Bake costs into price for 'Free Shipping'.",
        "Authentication: Use 3rd-party apps to justify luxury hikes.",
        "Rarity Factor: Use 'Rare' only if solds are actually scarce."
    ],
    "s4": [
        "eBay Specs: Fill every 'Item Specific' to boost search rank.",
        "Poshmark Sharing: Share your closet 3x daily to stay on top.",
        "Character Maxing: Use all 80 characters for maximum SEO reach.",
        "Keyword Synonyms: Use 'sneakers' and 'kicks' to catch searches.",
        "Freshness Ranking: Relist old items as 'New' for an algo boost.",
        "Mercari Promotions: Use 'Promote' for a 5% discount to likers.",
        "Cross-Listing: List on 3+ platforms to increase sell-through.",
        "Offer to Likers: Sending offers within 10 mins doubles sales.",
        "Drafting Strategy: Create drafts at night; launch during peaks.",
        "Avoid Brand-Spamming: Unrelated tags can get you flagged."
    ],
    "s5": [
        "Professional Packaging: Branded mailers win repeat buyers.",
        "Weight Precision: Scales save $2 per package. [Get my scale].",
        "Eco-Friendly Edge: Compostable mailers are a top filter.",
        "Thermal Speed: No ink; thermal printers pay for themselves.",
        "Bulk Tape Logic: Buy 6-packs to avoid running out. [Grab tape].",
        "Lighting Kits: Softboxes kill yellow tints. [My light set].",
        "Measurement Tools: Fabric tape measures are essential. [Get one].",
        "4x6 Labels: Give a corporate delivery look. [Shop labels].",
        "Mannequin Magic: Forms sell 20% faster than flat lays. [Shop].",
        "Clear Bins: Find inventory fast with clear bin storage."
    ]
}

def get_random_tip(step_id):
    return random.choice(TIP_POOL.get(step_id, ["Analyzing market trends..."]))

# --- 3. NEURAL LOGIC FUNCTIONS ---
def analyze_market_logic(img_file, description):
    if not img_file and not description:
        return "Need a photo or description to analyze the market!"
    try:
        content_parts = []
        if img_file:
            content_parts.append(types.Part.from_bytes(data=img_file.getvalue(), mime_type=img_file.type))
        
        prompt = f"ACT AS PRO RESELLER. Use photo if clear, else fallback to notes: '{description}'. Provide: Value, Demand, and Top 3 Comparative Keywords for eBay/Poshmark."
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

# --- 4. ARCHITECTURAL ENGINE (CSS LOCK) ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }

    /* ZONE 1: RADIO & LABEL VISIBILITY */
    [data-testid="stRadio"] label, [data-testid="stRadio"] label p, [data-testid="stWidgetLabel"] p {
        color: #0F172A !important; font-weight: 800 !important; opacity: 1 !important;
    }

    /* ZONE 2: TABLE CONTRAST */
    [data-testid="stTable"] td, [data-testid="stTable"] th {
        color: #0F172A !important; background-color: #F8FAFC !important; font-weight: 600 !important; border: 1px solid #E2E8F0 !important;
    }

    /* ZONE 3: TEXT INPUTS */
    [data-testid="stTextArea"] textarea {
        background-color: #F1F5F9 !important; color: #000000 !important; font-weight: 600 !important; border: 2px solid #CBD5E1 !important; border-radius: 12px !important;
    }
    [data-testid="stTextArea"] textarea::placeholder { color: #64748B !important; }

    /* ZONE 4: NOTIFICATION BOXES */
    .reminder-box { background-color: #FFFBEB !important; border-left: 6px solid #F59E0B !important; padding: 15px; border-radius: 12px; margin: 10px 0; border: 1px solid #FEF3C7; }
    .suggestion-box { background-color: #F0F9FF !important; border-left: 6px solid #0EA5E9 !important; padding: 15px; border-radius: 12px; margin: 10px 0; border: 1px solid #E0F2FE; }
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

    /* ZONE 6: BUTTONS & COLORS */
    .stButton > button {
        border-radius: 12px !important; height: 60px !important; font-weight: 950 !important;
        text-transform: uppercase !important; border: none !important; color: white !important; width: 100% !important;
    }
    div[data-testid="column"]:nth-of-type(1) div[data-testid="stButton"] button { background-color: #1877F2 !important; }
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"] button { background-color: #002F6C !important; }
    div[data-testid="column"]:nth-of-type(3) div[data-testid="stButton"] button { background-color: #502189 !important; }
    div[data-testid="column"]:nth-of-type(4) div[data-testid="stButton"] button { background-color: #8C1B2F !important; }

    .m-btn {
        flex: 1 !important; height: 60px !important; border-radius: 12px !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        text-decoration: none !important; color: white !important; font-weight: 950 !important; font-size: 12px !important;
        text-transform: uppercase !important; text-align: center !important; line-height: 60px !important;
    }
    #google-red { background-color: #CC0000 !important; }
    #amz-brown { background-color: #483332 !important; }
    #ebay-blue { background-color: #002F6C !important; }
    #posh-maroon { background-color: #8C1B2F !important; }
    </style>
""", unsafe_allow_html=True)

# --- 5. UI LAYOUT ---
st.markdown(f'''<div class="header-wrapper"><div class="title-container"><span class="brand-word">LAZY</span><span class="sloth-anchor">🦥</span><span class="brand-word">LISTER</span></div><span class="neon-text neon-sub">PREMIUM RESELLER ASSISTANT</span></div>''', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<p class="step-label">STEP 1: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)
    st.markdown(f'''<div class="suggestion-box"><span class="tip-tag" style="color:#0EA5E9;">🧠 AI STRATEGY</span><p class="tip-text">{get_random_tip("s1")}</p></div>''', unsafe_allow_html=True)
    img_file = st.camera_input("Scanner", label_visibility="collapsed")
    
    st.markdown('<p class="step-label">STEP 2: <span class="neon-text">DESCRIBE</span></p>', unsafe_allow_html=True)
    st.markdown(f'''<div class="reminder-box"><span class="tip-tag" style="color:#F59E0B;">🧠 AI STRATEGY</span><p class="tip-text">{get_random_tip("s2")}</p></div>''', unsafe_allow_html=True)
    notes_input = st.text_area("Notes", placeholder="buttery, chunky, structured...", height=150, key="notes_input", label_visibility="collapsed")
    st.button("🗑️ CLEAR DESCRIPTION", use_container_width=True, on_click=clear_text_callback)

with col2:
    st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
    st.markdown(f'''<div class="suggestion-box"><span class="tip-tag" style="color:#0EA5E9;">🧠 AI STRATEGY</span><p class="tip-text">{get_random_tip("s3")}</p></div>''', unsafe_allow_html=True)
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
    st.markdown(f'''<div class="reminder-box"><span class="tip-tag" style="color:#F59E0B;">🧠 AI STRATEGY</span><p class="tip-text">{get_random_tip("s4")}</p></div>''', unsafe_allow_html=True)
    selected_style = st.radio("STYLE:", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")
    
    p1, p2, p3, p4 = st.columns(4)
    if p1.button("FB"): st.session_state.listing_out = generate_listing("Facebook", notes_input, selected_style)
    if p2.button("EBAY"): st.session_state.listing_out = generate_listing("eBay", notes_input, selected_style)
    if p3.button("CL"): st.session_state.listing_out = generate_listing("Craigslist", notes_input, selected_style)
    if p4.button("POSH"): st.session_state.listing_out = generate_listing("Poshmark", notes_input, selected_style)

    st.text_area("Output", value=st.session_state.get('listing_out', ''), height=150, key="output_area", label_visibility="collapsed")
    st.button("📋 COPY LISTING", use_container_width=True)

    st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
    st.markdown(f'''<div class="suggestion-box"><span class="tip-tag" style="color:#0EA5E9;">🧠 AI STRATEGY</span><p class="tip-text">{get_random_tip("s5")}</p></div>''', unsafe_allow_html=True)
    st.markdown(f'''<div style="display:flex; gap:8px; margin:8px 0;">
        <a href="https://shopping.google.com" target="_blank" class="m-btn" id="google-red">SHOP</a>
        <a href="https://www.amazon.com" target="_blank" class="m-btn" id="amz-brown">PRO</a>
    </div>''', unsafe_allow_html=True)

st.divider()
st.markdown('<p class="step-label">INVENTORY LOG</p>', unsafe_allow_html=True)
st.table(pd.DataFrame({"Item": ["Scanning..."], "Platform": ["Syncing"], "Price": ["--"]}))

if st.button("🗑️ RESET SESSION", use_container_width=True):
    st.session_state.clear(); st.rerun()
