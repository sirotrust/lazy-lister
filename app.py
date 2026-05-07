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

# --- 2. THE MASTER 50-TIP NEURAL LIBRARY ---
TIP_POOL = {
    "s1": [
        "Pro Tip: Use the rear-facing lens; it has 40% higher resolution than the selfie camera.",
        "Pro Tip: Lock your focus (AE/AF Lock) by holding the screen to prevent 'breathing' shots.",
        "Pro Tip: Natural window light between 10am-2pm yields the most color-accurate photos.",
        "Pro Tip: Turn on camera gridlines to ensure your horizons and products are perfectly level.",
        "Pro Tip: Physically move closer to the item; never use digital zoom as it destroys detail.",
        "Pro Tip: Clean your lens with a microfiber cloth before every session to remove finger oils.",
        "Pro Tip: Use a plain white background to help the AI detect item edges instantly.",
        "Pro Tip: Capture a dedicated shot of the 'Care Tag' for fabric content verification.",
        "Pro Tip: Use a white poster board as a reflector to bounce light into dark shadows.",
        "Pro Tip: Shoot shoes at a 45-degree 'hero' angle for the most shoppable presentation."
    ],
    "s2": [
        "Pro Tip: Always place the Brand Name and Model in the first 3 words of your description.",
        "Pro Tip: Use sensory words like 'buttery,' 'chunky,' or 'structured' to sell the feel.",
        "Pro Tip: Mention 'Smoke-Free' or 'Pet-Free' status to build immediate buyer confidence.",
        "Pro Tip: List three mandatory measurements: Pit-to-pit, Total Length, and Sleeve Length.",
        "Pro Tip: Use 'texture' keywords like 'slubby' or 'brushed' to improve search hits.",
        "Pro Tip: Describe the 'Vibe'—is it Gorpcore, Dark Academia, or Minimalist?",
        "Pro Tip: Find the small model code on the internal tag for professional stock data.",
        "Pro Tip: Disclose pilling or fading early; it reduces return rates by nearly 30%.",
        "Pro Tip: Be specific with colors; 'Cobalt' or 'Azure' ranks better than just 'Blue'.",
        "Pro Tip: Mention 'Stitch Detail' or 'Quality Hardware' to justify premium pricing."
    ],
    "s3": [
        "Pro Tip: Check 'Sold' listings only; active prices are what people want, not what they get.",
        "Pro Tip: Price 10-15% higher than the average to allow room for 'Best Offer' negotiations.",
        "Pro Tip: Items at $24.99 sell significantly faster than items listed at a flat $25.00.",
        "Pro Tip: Calculate shipping costs before pricing; heavy items can kill your profit margins.",
        "Pro Tip: Cross-reference eBay vs. Poshmark for a true, multi-platform market average.",
        "Pro Tip: Free Shipping tags increase listing visibility in buyer filters by over 2x.",
        "Pro Tip: Price vintage based on decade and rarity, not just current fashion trends.",
        "Pro Tip: Drop prices by 10% on Friday afternoons when buyers receive their paychecks.",
        "Pro Tip: High-demand brands (Nike, Lululemon) follow very strict MSRP-based resale logic.",
        "Pro Tip: High-quality photos allow you to price 20% higher than competitors with dark shots."
    ],
    "s4": [
        "Pro Tip: Use all 80 characters in eBay titles; the algorithm penalizes empty space.",
        "Pro Tip: Relist items every 30 days to keep your 'New Listing' status in the algorithm.",
        "Pro Tip: Share your Poshmark closet at 9PM EST during peak mobile shopping hours.",
        "Pro Tip: Include seasonal keywords like 'Gifts for Him' or 'Summer Essential' for SEO.",
        "Pro Tip: Never use stock photos alone; platforms de-prioritize listings without real photos.",
        "Pro Tip: Copy-paste your top 5 SEO tags into the very bottom of your description field.",
        "Pro Tip: Offer 'Combined Shipping' to encourage buyers to purchase multiple items at once.",
        "Pro Tip: Use 'Expert' style for electronics to show buyers you know the technical specs.",
        "Pro Tip: On Facebook Marketplace, respond within 5 mins to keep your 'Responsive' badge.",
        "Pro Tip: Send 'Offers to Likers' within 10 minutes of a 'Like' to double your conversion rate."
    ],
    "s5": [
        "Helpful Suggestion: Stop overpaying for ink. This Thermal Printer pays for itself in 3 months. [View Setup]",
        "Efficiency Upgrade: Eliminate 'Underweight' surcharges with a high-precision digital scale. [Secure Yours]",
        "Visual Advantage: Kill the 'Yellow Tint' in your photos instantly with a curated lighting kit. [See My Set]",
        "Boutique Standard: Buyers notice quality mailers. These matte-black mailers earn repeat customers. [Get Bulk Deal]",
        "Speed Strategy: Handheld fabric steamers remove wrinkles 3x faster than traditional irons. [Check Current Price]",
        "Reseller Essential: Items on a mannequin sell 20% faster than 'flat-lays.' [View Top-Rated Form]",
        "Precision Tool: Accurate measurements are mandatory for SEO. Grab the retractable tape I use. [See My Pick]",
        "Workflow Secret: Bulk 6-pack shipping tape saves $12 monthly over single-roll pricing. [Stock Up Now]",
        "Organization Pro: Clear bin storage keeps inventory dust-free and instantly searchable. [Explore Bins]",
        "Pro-Level Finish: Thermal 4x6 labels give every package a 'corporate' professional look. [Shop Label Deals]"
    ]
}

def get_random_tip(step_id):
    return random.choice(TIP_POOL.get(step_id, ["Synchronizing market intelligence..."]))

# --- 3. BRAIN LOGIC ---
def analyze_market_logic(img_file, description):
    if not img_file and not description: return "Need data!"
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

# --- 4. ARCHITECTURAL ENGINE (UNIFIED DESIGN LOCK) ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }

    /* STEP LABELS */
    .step-label { color: #0F172A !important; font-weight: 950; font-size: 28px; text-transform: uppercase; margin-top: 30px; border-bottom: 3px solid #0F172A; display: inline-block; }
    .brand-word { color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1px; }
    .sloth-anchor { font-size: 55px; margin-top: -25px; }
    .neon-text { font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }

    /* BOXES */
    .reminder-box, .suggestion-box { padding: 15px; border-radius: 12px; margin: 10px 0; border: 1px solid; }
    .reminder-box { background-color: #FFFBEB !important; border-left: 6px solid #F59E0B !important; border-color: #FEF3C7; }
    .suggestion-box { background-color: #F0F9FF !important; border-left: 6px solid #0EA5E9 !important; border-color: #E0F2FE; }
    .tip-tag { font-weight: 950; font-size: 11px; text-transform: uppercase; display: block; }
    .tip-text { color: #1E293B !important; font-size: 14px; font-weight: 600; }

    /* TEXT AREA */
    [data-testid="stTextArea"] textarea { background-color: #F1F5F9 !important; color: #000000 !important; font-weight: 600 !important; border: 2px solid #CBD5E1 !important; border-radius: 12px !important; }

    /* FLEX GRID FOR HTML BUTTONS (STEP 3 & 5) */
    .flex-grid { display: flex; flex-wrap: nowrap; gap: 8px; width: 100%; margin: 10px 0; }
    .m-btn {
        flex: 1 !important; height: 60px !important; border-radius: 12px !important; display: flex !important; align-items: center !important; justify-content: center !important;
        text-decoration: none !important; color: white !important; font-weight: 950 !important; font-size: 12px !important; text-transform: uppercase !important; text-align: center !important; line-height: 60px !important;
    }
    
    /* BRAND COLORS */
    .ebay-blue { background-color: #002F6C !important; }
    .amz-brown { background-color: #483332 !important; }
    .google-red { background-color: #CC0000 !important; }
    .posh-maroon { background-color: #8C1B2F !important; }

    /* NATIVE BUTTON OVERRIDES (STEP 4) */
    .stButton > button { border-radius: 12px !important; height: 60px !important; font-weight: 950 !important; text-transform: uppercase !important; color: white !important; width: 100% !important; }
    div[data-testid="column"]:nth-of-type(1) button { background-color: #1877F2 !important; }
    div[data-testid="column"]:nth-of-type(2) button { background-color: #002F6C !important; }
    div[data-testid="column"]:nth-of-type(3) button { background-color: #502189 !important; }
    div[data-testid="column"]:nth-of-type(4) button { background-color: #8C1B2F !important; }
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
    if st.button("🗑️ CLEAR DESCRIPTION", use_container_width=True):
        st.session_state.notes_input = ""; st.rerun()

with col2:
    st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
    st.markdown(f'<div class="suggestion-box"><span class="tip-tag" style="color:#0EA5E9;">💰 PRO TIP</span><p class="tip-text">{get_random_tip("s3")}</p></div>', unsafe_allow_html=True)
    if st.button("🚀 ANALYZE MARKET", type="primary", use_container_width=True):
        st.session_state.market_analysis = analyze_market_logic(img_file, notes_input)
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
    
    p1, p2, p3, p4 = st.columns(4)
    with p1: 
        if st.button("FB", use_container_width=True): 
            st.session_state.listing_out = generate_listing("Facebook", notes_input, selected_style)
    with p2:
        if st.button("EBAY", use_container_width=True):
            st.session_state.listing_out = generate_listing("eBay", notes_input, selected_style)
    with p3:
        if st.button("CL", use_container_width=True):
            st.session_state.listing_out = generate_listing("Craigslist", notes_input, selected_style)
    with p4:
        if st.button("POSH", use_container_width=True):
            st.session_state.listing_out = generate_listing("Poshmark", notes_input, selected_style)

    st.text_area("Output", value=st.session_state.get('listing_out', ''), height=150, key="output_area", label_visibility="collapsed")
    st.button("📋 COPY LISTING", use_container_width=True)

    st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
    st.markdown(f'<div class="suggestion-box"><span class="tip-tag" style="color:#0EA5E9;">🤝 YOUR EXPERT PARTNER</span><p class="tip-text">{get_random_tip("s5")}</p></div>', unsafe_allow_html=True)
    st.markdown('''<div class="flex-grid">
        <a href="YOUR_GOOGLE_LINK" target="_blank" class="m-btn google-red">GOOGLE SHOP</a>
        <a href="YOUR_AMAZON_LINK" target="_blank" class="m-btn amz-brown">AMAZON PRO</a>
    </div>''', unsafe_allow_html=True)

if st.button("🗑️ RESET SESSION", use_container_width=True):
    st.session_state.clear(); st.rerun()
