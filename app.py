import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
from google import genai
from google.genai import types

# --- 1. THE PRO TIP LIBRARY (60 ENTRIES) ---
TIP_LIBRARY = {
    "1": ["Wipe your camera lens before every scan to remove pocket lint and blur.", "Natural daylight is the best free studio lighting; avoid direct sun glare.", "Use a plain white or light gray backdrop to help AI isolate the item.", "Capture the 'Money Shot' first—the angle that best shows the item's value.", "For clothing, use a 'Ghost Mannequin' effect by filling it with padding.", "Take close-ups of brand tags and serial numbers for authenticity.", "Photograph every flaw; transparency builds buyer trust and prevents returns.", "Ensure the item fills 80% of the frame to maximize thumbnail visibility.", "Use a micro-fiber cloth to buff out smudges on electronics before scanning.", "For shoes, include a shot of the tread to show exact wear patterns."],
    "2": ["Mention 'Smoke-Free' or 'Pet-Free' homes; these are top buyer searches.", "If a logo is faded, describe the texture or material (e.g., 'Pebbled Leather').", "Include the 'MSRP' in your notes if the item is a known luxury piece.", "Note the 'Fit'—is it true to size, oversized, or runs small?", "Identify the 'Seasonality'—is this a 'Summer Essential' or 'Winter Ready'?", "List specific technology names (e.g., 'Gore-Tex' or 'Dri-FIT') for SEO.", "Describe flaws as 'Character' or 'Patina' for vintage items to stay positive.", "Mention if batteries or accessories are included to justify higher prices.", "Use the word 'Authentic' only if you have verified the serial number.", "If the brand is unknown, focus on the style trend (e.g., 'Boho' or 'Y2K')."],
    "3": ["Sort eBay by 'Sold Items' only; 'Listed Price' is often wishful thinking.", "Check Google Shopping to see what major retailers are charging for 'New'.", "On Poshmark, look at recently sold 'Comps' to gauge current platform heat.", "Price 10% higher than your goal to leave room for 'Best Offer' negotiations.", "End your price in '.99' or '.95' for psychological 'Value' perception.", "If supply is low but demand is high, don't be afraid to set a 'Premium' price.", "Monitor 'Watchers'—if you have many but no sales, drop price by 5%.", "Consider 'Free Shipping' but bake the shipping cost into the item price.", "Analyze the 'Age' of comps; sales from 6 months ago may be outdated.", "During holidays, prices can sustain a 15-20% markup on giftable items."],
    "4": ["The first 80 characters of your title are the most important for SEO.", "Use 'Expert' style for high-ticket items to sound like a boutique.", "Include 'NWT' (New With Tags) at the start of titles if applicable.", "Add emojis to Facebook Marketplace titles to catch the scroller's eye.", "Mention 'Fast Shipping' in the description to encourage immediate buys.", "Use bullet points for features; buyers scan descriptions rather than reading.", "Cross-post to at least 3 platforms to triple your chances of a 24hr sale.", "List items on Sunday evenings; this is peak traffic time for most apps.", "Keep descriptions concise but thorough to reduce 'Is this available' DMs.", "Refresh your listings every 30 days to stay at the top of search results."],
    "5": ["Reuse clean Amazon boxes to save on supply costs and reduce waste.", "Invest in a thermal label printer to save hundreds on ink annually.", "Double-wrap fragile items in bubble wrap AND brown packing paper.", "Use 'Poly Mailers' for clothing to reduce weight and shipping costs.", "Always weigh your item WITH the box to avoid 'Postage Due' errors.", "Keep a 'Thank You' note template to encourage 5-star buyer reviews.", "Use 'Fragile' tape on the outside of boxes to alert postal handlers.", "For high-value items, use 'Signature Confirmation' for legal protection.", "Store poly mailers in sizes Small, Medium, and Large for quick packing.", "Use recycled paper shredding as a sustainable alternative to packing peanuts."],
    "6": ["Assign each item a 'Bin Number' to find sold items in under 60 seconds.", "Track your 'Cost of Goods Sold' (COGS) to see your actual net profit.", "Log the 'Date Listed' to identify 'Stale' inventory that needs a price cut.", "Quarterly inventory audits prevent 'Lost Item' cancellations.", "Keep photos on a cloud drive even after listing for backup.", "Group similar items in bins to make batch shipping faster.", "Use a simple 'SKU' system (e.g., SH-001 for Shirt #1) for tracking.", "Note the original platform listed on to avoid 'Double Selling'.", "Calculate your 'Sell-Through Rate' to see which brands flip the fastest.", "Keep your inventory off the floor to prevent moisture or dust damage."]
}

# --- 2. ENGINE ROOM (HARD-LOCK) ---
LITE_MODEL = "gemini-2.5-flash-lite" 
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'master_id': "", 'listing_out': "", 'supply_tips': "", 'is_pro': False, 
        'scan_count': 0, 'tip_idx': 0
    }

def get_pro_tip(step_num):
    idx = st.session_state.app_state['tip_idx'] % 10
    return TIP_LIBRARY[str(step_num)][idx]

# --- 3. UI ARCHITECTURE (CSS) ---
st.markdown(f"""
    <style>
    header, footer, [data-testid="stHeader"] {{visibility: hidden; display: none;}}
    .stApp {{ background-color: #FFFFFF !important; }}

    /* BRANDING (60px) */
    .brand-word {{ color: #0F172A; font-size: 60px; font-weight: 950; text-transform: uppercase; line-height: 0.8; letter-spacing: -1.5px; }}
    .neon-text {{ font-weight: 900; background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; font-size: 16px !important; }}
    
    /* RADIO BUTTON FIX */
    [data-testid="stRadio"] label, [data-testid="stRadio"] label p {{
        color: #0F172A !important; font-weight: 800 !important; opacity: 1 !important;
    }}

    /* TOP NAV MANUAL */
    .instruction-container {{ margin: 15px 0 30px 0; max-width: 950px; }}
    .instruction-row {{ display: flex; align-items: center; margin-bottom: 3px; gap: 6px; }}
    .instruction-text {{ 
        font-size: 12px; font-weight: 950; text-transform: uppercase; letter-spacing: 0.5px; 
        background: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        white-space: nowrap; 
    }}

    /* STEP LABELS (28px) */
    .step-label {{ 
        font-weight: 950; font-size: 28px !important; text-transform: uppercase; margin-top: 30px; 
        display: block; width: 100%;
        background-image: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        line-height: 1.0; letter-spacing: -0.5px;
    }}
    
    .step-sub-label {{
        font-weight: 800; font-size: 14px; text-transform: uppercase; margin-bottom: 10px;
        background-image: linear-gradient(to right, #22d3ee, #002F6C, #8C1B2F);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        white-space: nowrap; display: block; border-bottom: 2px solid #F1F5F9; padding-bottom: 5px;
    }}

    /* PRO TIP BOX */
    .pro-tip-box {{
        background: #F8FAFC; border-left: 4px solid #002F6C; padding: 12px; margin: 10px 0; border-radius: 0 8px 8px 0;
    }}
    .pro-tip-header {{ font-weight: 950; font-size: 10px; text-transform: uppercase; color: #002F6C; margin-bottom: 3px; letter-spacing: 1px; }}
    .pro-tip-content {{ font-weight: 600; font-size: 13px; color: #0F172A; font-style: italic; }}

    /* BUTTONS */
    .flex-grid {{ display: flex; flex-wrap: nowrap; gap: 8px; width: 100%; margin: 15px 0; }}
    .m-btn {{
        flex: 1; height: 60px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
        text-decoration: none !important; color: #FFFFFF !important; font-weight: 950; font-size: 12px; text-transform: uppercase; border: none;
    }}
    
    #fb-cyan {{ background: linear-gradient(45deg, #22d3ee, #0ea5e9) !important; }}
    #ebay-midnight {{ background: linear-gradient(45deg, #002F6C, #0F172A) !important; }}
    #posh-velvet {{ background: linear-gradient(45deg, #8C1B2F, #4c0519) !important; }}
    #google-red {{ background-color: #CC0000 !important; }}
    #amz-brown {{ background-color: #483332 !important; }}
    
    .stButton button {{
        height: 65px !important; border-radius: 14px !important; font-weight: 950 !important;
        font-size: 22px !important; background: #0F172A !important; 
        color: white !important; border: none !important;
        text-transform: uppercase !important; letter-spacing: 1px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. APP LAYOUT ---
st.markdown('<div style="margin-top:5px;"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="instruction-container">
    <div class="instruction-row"><div class="instruction-text">1. Scan — Take a photo</div></div>
    <div class="instruction-row"><div class="instruction-text">2. Analyze — Search online with Ai</div></div>
    <div class="instruction-row"><div class="instruction-text">3. Price — Compare market value</div></div>
    <div class="instruction-row"><div class="instruction-text">4. List — Generate listing with Ai</div></div>
    <div class="instruction-row"><div class="instruction-text">5. Supplies — Purchase shipping supplies</div></div>
    <div class="instruction-row"><div class="instruction-text">6. Inventory — Create and share your items</div></div>
</div>
""", unsafe_allow_html=True)

# STEP 1: SCAN
st.markdown('<div class="step-label">STEP 1: SCAN</div>', unsafe_allow_html=True)
st.markdown('<div class="step-sub-label">Take a photo of your item</div>', unsafe_allow_html=True)
if 'hero_shot' not in st.session_state:
    img_file = st.camera_input("Scanner", label_visibility="collapsed")
    if img_file:
        st.session_state.hero_shot = img_file.getvalue()
        st.session_state.img_type = img_file.type
        st.rerun()
else:
    st.image(st.session_state.hero_shot, use_container_width=True)
    st.markdown(f"""<div class="pro-tip-box"><div class="pro-tip-header">💡 PRO TIP: VISIBILITY</div><div class="pro-tip-content">"{get_pro_tip(1)}"</div></div>""", unsafe_allow_html=True)
    if st.button("ADD ITEM", use_container_width=True):
        st.session_state.app_state['tip_idx'] += 1
        for key in ['hero_shot', 'img_type']:
            if key in st.session_state: del st.session_state[key]
        st.session_state.app_state['master_id'] = ""
        st.session_state.app_state['listing_out'] = ""
        st.session_state.app_state['scan_count'] += 1 
        st.rerun()

# STEP 2: ANALYZE
st.markdown('<div class="step-label">STEP 2: ANALYZE</div>', unsafe_allow_html=True)
st.markdown('<div class="step-sub-label">Search online with Ai</div>', unsafe_allow_html=True)
notes = st.text_area("Notes", height=100, placeholder="Describe your item if details are not visible...", label_visibility="collapsed", key=f"notes_{st.session_state.app_state['scan_count']}")

st.markdown(f"""<div class="pro-tip-box"><div class="pro-tip-header">💡 PRO TIP: ACCURACY</div><div class="pro-tip-content">"{get_pro_tip(2)}"</div></div>""", unsafe_allow_html=True)
if st.button("ANALYZE", use_container_width=True):
    st.session_state.app_state['tip_idx'] += 1
    if 'hero_shot' in st.session_state:
        with st.spinner("Surgical Brand Scan..."):
            client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
            part = types.Part.from_bytes(data=st.session_state.hero_shot, mime_type=st.session_state.img_type)
            surgical_prompt = (
                f"Professional identifier scan. Discard background/surfaces. Identify exact BRAND and MODEL. "
                f"Notes: {notes}. 5-word title."
            )
            res = client.models.generate_content(model=LITE_MODEL, contents=[surgical_prompt, part])
            st.session_state.app_state['master_id'] = res.text
            sup_res = client.models.generate_content(model=LITE_MODEL, contents=[f"2 packing items for: {res.text}"])
            st.session_state.app_state['supply_tips'] = sup_res.text
            st.rerun()

# STEP 3: PRICE
st.markdown('<div class="step-label">STEP 3: PRICE</div>', unsafe_allow_html=True)
st.markdown('<div class="step-sub-label">Compare market value</div>', unsafe_allow_html=True)
if st.session_state.app_state['master_id']: st.info(f"**AI ID:** {st.session_state.app_state['master_id']}")

sq = urllib.parse.quote(st.session_state.app_state['master_id'] if st.session_state.app_state['master_id'] else notes)
st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.ebay.com/sch/i.html?_nkw={sq}&LH_Sold=1&LH_Complete=1" target="_blank" class="m-btn" id="ebay-midnight">EBAY</a>
        <a href="https://www.google.com/search?q={sq}+price&tbm=shop" target="_blank" class="m-btn" id="google-red">GOOGLE</a>
        <a href="https://poshmark.com/search?query={sq}" target="_blank" class="m-btn" id="posh-velvet">POSH</a>
    </div>
''', unsafe_allow_html=True)
st.markdown(f"""<div class="pro-tip-box"><div class="pro-tip-header">💡 PRO TIP: PROFIT</div><div class="pro-tip-content">"{get_pro_tip(3)}"</div></div>""", unsafe_allow_html=True)

# STEP 4: LIST
st.markdown('<div class="step-label">STEP 4: LIST</div>', unsafe_allow_html=True)
st.markdown('<div class="step-sub-label">Generate a listing with Ai</div>', unsafe_allow_html=True)
st.radio("Style", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed", key="style_radio")

# Pro Tip positioned under radio buttons but above platform buttons
st.markdown(f"""<div class="pro-tip-box"><div class="pro-tip-header">💡 PRO TIP: VELOCITY</div><div class="pro-tip-content">"{get_pro_tip(4)}"</div></div>""", unsafe_allow_html=True)

st.markdown(f'''
    <div class="flex-grid">
        <a href="/?action=facebook" target="_self" class="m-btn" id="fb-cyan">FACEBOOK</a>
        <a href="/?action=ebay" target="_self" class="m-btn" id="ebay-midnight">EBAY</a>
        <a href="/?action=poshmark" target="_self" class="m-btn" id="posh-velvet">POSHMARK</a>
    </div>
''', unsafe_allow_html=True)

st.text_area("Output", value=st.session_state.app_state['listing_out'], height=150, label_visibility="collapsed")

# STEP 5: SUPPLIES
st.markdown('<div class="step-label">STEP 5: SUPPLIES</div>', unsafe_allow_html=True)
st.markdown('<div class="step-sub-label">Purchase shipping supplies</div>', unsafe_allow_html=True)

# Tip positioned above buttons
st.markdown(f"""<div class="pro-tip-box"><div class="pro-tip-header">💡 PRO TIP: OVERHEAD</div><div class="pro-tip-content">"{get_pro_tip(5)}"</div></div>""", unsafe_allow_html=True)

supply_q = urllib.parse.quote(f"shipping supplies for {st.session_state.app_state['master_id']}")
st.markdown(f'''
    <div class="flex-grid">
        <a href="https://www.amazon.com/s?k={supply_q}" target="_blank" class="m-btn" id="amz-brown">AMAZON</a>
        <a href="https://www.google.com/search?q={supply_q}+shipping&tbm=shop" target="_blank" class="m-btn" id="google-red">GOOGLE</a>
    </div>
''', unsafe_allow_html=True)

# Ai tips positioned below buttons
if st.session_state.app_state['supply_tips']: 
    st.success(f"📦 Ai tips: {st.session_state.app_state['supply_tips']}")

# STEP 6: INVENTORY
st.markdown('<div class="step-label">STEP 6: INVENTORY</div>', unsafe_allow_html=True)
st.markdown('<div class="step-sub-label">Create and share your items</div>', unsafe_allow_html=True)

if st.session_state.app_state['is_pro']:
    with st.expander("➕ MANUAL ENTRY (UNLOCKED)"):
        with st.form("manual"):
            m_item = st.text_input("Item Name")
            m_plat = st.selectbox("Platform", ["eBay", "Facebook", "Poshmark"])
            if st.form_submit_button("Log Item"):
                st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": m_item, "Platform": m_plat})
                st.rerun()
else:
    st.warning("🔒 Manual Entry & Batching are reserved for Pro Subscribers.")

if st.session_state.inventory:
    st.table(pd.DataFrame(st.session_state.inventory))

st.markdown(f"""<div class="pro-tip-box"><div class="pro-tip-header">💡 PRO TIP: SCALE</div><div class="pro-tip-content">"{get_pro_tip(6)}"</div></div>""", unsafe_allow_html=True)

# SIDEBAR PAYWALL
with st.sidebar:
    st.markdown("### 💎 COMMERCIAL SUITE")
    st.session_state.app_state['is_pro'] = st.toggle("Simulate Pro Subscription", value=st.session_state.app_state['is_pro'])

# Trigger Listener
params = st.query_params
if "action" in params:
    action = params.get("action")
    ctx = st.session_state.app_state['master_id']
    if ctx:
        try:
            st.session_state.app_state['tip_idx'] += 1 
            client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
            style = st.session_state.get("style_radio", "Simple")
            res = client.models.generate_content(model=LITE_MODEL, contents=[f"Write a {style} {action} listing for: {ctx}"])
            st.session_state.app_state['listing_out'] = res.text
            st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": ctx[:30], "Platform": action.upper()})
            st.query_params.clear()
            st.rerun()
        except: st.query_params.clear()
