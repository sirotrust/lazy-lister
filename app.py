import streamlit as st
import pandas as pd
from google import genai
from google.genai import types
import random
from datetime import datetime

# --- 1. THE BRAIN & ARCHITECTURAL ENGINE ---
st.set_page_config(page_title="Lazy Lister Pro", layout="wide")

if 'inventory' not in st.session_state:
    st.session_state.inventory = []

if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'analysis': "",
        'listing_out': "",
        'style': "Pro"
    }

try:
    google_client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("LEAD DEV: API Handshake Failed. Check secrets.toml.")

# --- 2. THE MASTER 50-TIP NEURAL LIBRARY (PROTECTED) ---
TIP_POOL = {
    "s1": ["Pro Tip: Use the rear-facing lens; it has 40% higher resolution.", "Pro Tip: Lock AE/AF Lock by holding the screen.", "Pro Tip: Natural window light between 10am-2pm is best.", "Pro Tip: Turn on gridlines for perfect leveling.", "Pro Tip: Move closer; never use digital zoom.", "Pro Tip: Clean your lens before every session.", "Pro Tip: Use white backgrounds for AI edge detection.", "Pro Tip: Shoot the care tag for fabric verification.", "Pro Tip: Use white board to reflect light into shadows.", "Pro Tip: Shoot shoes at a 45-degree hero angle."],
    "s2": ["Pro Tip: Place the Brand and Model in the first 3 words.", "Pro Tip: Use words like 'buttery' or 'structured' to sell the feel.", "Pro Tip: Mention 'Smoke-Free' to build buyer trust.", "Pro Tip: List Pit-to-pit, Length, and Sleeve measurements.", "Pro Tip: Use 'texture' keywords like 'slubby'.", "Pro Tip: Define the Vibe: Is it Gorpcore or Minimalist?", "Pro Tip: Find the model code on the internal tag.", "Pro Tip: Disclose pilling early to reduce returns.", "Pro Tip: Use 'Azure' or 'Cobalt' instead of just 'Blue'.", "Pro Tip: Mention hardware quality for premium items."],
    "s3": ["Pro Tip: Check 'Sold' listings, not 'Active' ones.", "Pro Tip: Price 10% high to allow for negotiations.", "Pro Tip: $24.99 converts 15% better than $25.00.", "Pro Tip: Weigh items before pricing for shipping.", "Pro Tip: Cross-reference eBay vs Poshmark for averages.", "Pro Tip: Free Shipping tags increase filter hits by 2x.", "Pro Tip: Price vintage on rarity, not just fashion.", "Pro Tip: Drop prices by 10% on Fridays for paydays.", "Pro Tip: High-demand brands follow strict MSRP logic.", "Pro Tip: High-quality photos justify a 20% price hike."],
    "s4": ["Pro Tip: Max out 80 characters in eBay titles.", "Pro Tip: Relist items every 30 days for 'New' status.", "Pro Tip: Share closet at 9PM EST for peak activity.", "Pro Tip: Use seasonal keywords like 'Summer Essential'.", "Pro Tip: Never use stock photos alone; AI flags them.", "Pro Tip: Put top 5 SEO tags in description footer.", "Pro Tip: Use 'Expert' style for tech listings.", "Pro Tip: Respond within 5 mins on FB Marketplace.", "Pro Tip: Send offers within 10 mins of a 'Like'.", "Pro Tip: Combine shipping to encourage multi-buys."],
    "s5": ["Expert Partner: This Thermal Printer pays for itself. [View Setup]", "Sourcing Secret: Scales prevent shipping surcharges. [Secure Yours]", "Visual Power: Kill 'Yellow Tint' with a curated lighting kit. [See My Set]", "Boutique Standard: Matte-black mailers win fans. [Shop Bulk]", "Speed Logic: Steamers remove wrinkles 3x faster than irons. [View Price]", "Professional Edge: Items on a mannequin sell 20% faster. [Check Forms]", "Mandatory Tool: Accurate measurements are mandatory for SEO. [See Pick]", "Volume Strategy: Bulk 6-pack shipping tape saves $12 monthly. [Stock Up]", "Efficiency Pro: Clear bin storage keeps inventory searchable. [Explore Bins]", "The Pro Finish: Thermal 4x6 labels give every package a corporate look."]
}

# --- 3. THE TOTAL CSS OVERRIDE (RESTORED MASTERPIECE) ---
st.markdown("""
    <style>
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .stApp { background-color: #FFFFFF !important; }

    /* ZONE 1: RADIO & LABEL VISIBILITY */
    [data-testid="stRadio"] label, [data-testid="stRadio"] label p, [data-testid="stWidgetLabel"] p {
        color: #0F172A !important;
        font-weight: 800 !important;
        opacity: 1 !important;
    }

    /* ZONE 2: TABLE CONTRAST */
    [data-testid="stTable"] td, [data-testid="stTable"] th {
        color: #0F172A !important;
        background-color: #F8FAFC !important;
        font-weight: 600 !important;
        border: 1px solid #E2E8F0 !important;
    }

    /* ZONE 3: TEXT INPUTS */
    [data-testid="stTextArea"] textarea {
        background-color: #F1F5F9 !important;
        color: #0F172A !important; 
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
        flex: 1; height: 60px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
        text-decoration: none; color: #FFFFFF !important; font-weight: 950; font-size: 11px; text-transform: uppercase; border: none; cursor: pointer;
    }

    /* ZONE 6: COLORS */
    .c-ebay { background-color: #002F6C !important; }
    .c-amazon { background-color: #483332 !important; }
    .c-google { background-color: #CC0000 !important; }
    .c-posh { background-color: #8C1B2F !important; }
    .c-fb { background-color: #1877F2 !important; }
    .c-cl { background-color: #502189 !important; }
    
    /* ZONE 7: BOXES */
    .suggestion-box, .reminder-box { padding: 15px; border-radius: 12px; margin: 10px 0; border: 1px solid; }
    .suggestion-box { background-color: #F0F9FF !important; border-left: 6px solid #0EA5E9 !important; border-color: #E0F2FE; }
    .reminder-box { background-color: #FFFBEB !important; border-left: 6px solid #F59E0B !important; border-color: #FEF3C7; }
    .tip-tag { font-weight: 950; font-size: 11px; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

# --- 4. THE BRIDGE ---
st.markdown("""
    <script>
    const doc = window.parent.document;
    window.addEventListener('message', function(event) {
        if (event.data.type === 'trigger') {
            const btns = Array.from(doc.querySelectorAll('button'));
            const target = btns.find(el => el.innerText.includes(event.data.key));
            if (target) target.click();
        }
    });
    </script>
""", unsafe_allow_html=True)

# --- 5. UI EXECUTION ---
st.markdown('<div style="margin-top:30px;"><span class="brand-word">LAZY 🦥 LISTER</span><br><span class="neon-text" style="font-size:18px;">PREMIUM RESELLER ASSISTANT</span></div>', unsafe_allow_html=True)

# STEP 1 & 2
st.markdown('<p class="step-label">STEP 1 & 2: <span class="neon-text">SCAN</span></p>', unsafe_allow_html=True)
st.markdown(f'<div class="suggestion-box"><span class="tip-tag" style="color: #0EA5E9;">📸 PRO TIP</span><p style="margin:0; font-weight:600;">{random.choice(TIP_POOL["s1"])}</p></div>', unsafe_allow_html=True)
img_file = st.camera_input("Scanner", label_visibility="collapsed")

st.markdown('<p class="step-label">DESCRIBE</p>', unsafe_allow_html=True)
st.markdown(f'<div class="reminder-box"><span class="tip-tag" style="color: #F59E0B;">📝 PRO TIP</span><p style="margin:0; font-weight:600;">{random.choice(TIP_POOL["s2"])}</p></div>', unsafe_allow_html=True)
notes = st.text_area("Notes", key="notes_input", height=100, placeholder="Brand, Condition...", label_visibility="collapsed")

# STEP 3
st.markdown('<p class="step-label">STEP 3: <span class="neon-text">PRICE</span></p>', unsafe_allow_html=True)
st.markdown(f'<div class="suggestion-box"><span class="tip-tag" style="color: #0EA5E9;">💰 PRO TIP</span><p style="margin:0; font-weight:600;">{random.choice(TIP_POOL["s3"])}</p></div>', unsafe_allow_html=True)

analyze_html = """<button onclick="parent.postMessage({type: 'trigger', key: 'RUN_ANALYSIS'}, '*')" style="width:100%; height:70px; background-color:#CC0000; color:white; border:none; border-radius:15px; font-weight:950; font-size:20px; text-transform:uppercase; cursor:pointer;">🚀 ANALYZE MARKET</button>"""
st.components.v1.html(analyze_html, height=85)

market_links_html = f"""
<div class="flex-grid">
    <a href="https://www.ebay.com/sch/i.html?_nkw={notes}" target="_blank" class="m-btn c-ebay">EBAY</a>
    <a href="https://www.amazon.com/s?k={notes}" target="_blank" class="m-btn c-amazon">AMAZON</a>
    <a href="https://www.google.com/search?q={notes}" target="_blank" class="m-btn c-google">GOOGLE</a>
    <a href="https://poshmark.com/search?query={notes}" target="_blank" class="m-btn c-posh">POSH</a>
</div>"""
st.components.v1.html(market_links_html, height=75)

if st.button("RUN_ANALYSIS", type="secondary"):
    if img_file:
        parts = [types.Part.from_text(text=f"Analyze: {notes}"), types.Part.from_bytes(data=img_file.getvalue(), mime_type=img_file.type)]
        st.session_state.app_state['analysis'] = google_client.models.generate_content(model="gemini-2.0-flash-lite-preview-02-05", contents=parts).text

if st.session_state.app_state['analysis']: st.info(st.session_state.app_state['analysis'])

# STEP 4
st.markdown('<p class="step-label">STEP 4: <span class="neon-text">LIST</span></p>', unsafe_allow_html=True)
st.markdown(f'<div class="reminder-box"><span class="tip-tag" style="color: #F59E0B;">🚀 PRO TIP</span><p style="margin:0; font-weight:600;">{random.choice(TIP_POOL["s4"])}</p></div>', unsafe_allow_html=True)
st.session_state.app_state['style'] = st.radio("STYLE", ["Simple", "Expert", "Pro"], horizontal=True, label_visibility="collapsed")

platform_grid_html = """
<div class="flex-grid">
    <button onclick="parent.postMessage({type: 'trigger', key: 'GO_FB'}, '*')" class="m-btn c-fb">FB</button>
    <button onclick="parent.postMessage({type: 'trigger', key: 'GO_EBAY'}, '*')" class="m-btn c-ebay">EBAY</button>
    <button onclick="parent.postMessage({type: 'trigger', key: 'GO_CL'}, '*')" class="m-btn c-cl">CL</button>
    <button onclick="parent.postMessage({type: 'trigger', key: 'GO_POSH'}, '*')" class="m-btn c-posh">POSH</button>
</div>"""
st.components.v1.html(platform_grid_html, height=75)

def trigger_list(p):
    p_prompt = f"Write a {st.session_state.app_state['style']} listing for {p}. Notes: {notes}"
    res = google_client.models.generate_content(model="gemini-2.0-flash-lite-preview-02-05", contents=[p_prompt])
    st.session_state.app_state['listing_out'] = res.text
    st.session_state.inventory.append({"Date": datetime.now().strftime("%m/%d"), "Item": notes[:30], "Platform": p})

if st.button("GO_FB"): trigger_list("Facebook")
if st.button("GO_EBAY"): trigger_list("eBay")
if st.button("GO_CL"): trigger_list("Craigslist")
if st.button("GO_POSH"): trigger_list("Poshmark")

st.text_area("Output", value=st.session_state.app_state['listing_out'], height=200, label_visibility="collapsed")

# INVENTORY LOG
st.markdown('<p class="step-label">INVENTORY LOG</p>', unsafe_allow_html=True)
if not st.session_state.inventory:
    ghost_data = pd.DataFrame({"Item": ["Scanning Log..."], "Platform": ["--"], "Date": ["--"]})
    st.table(ghost_data)
else:
    df = pd.DataFrame(st.session_state.inventory)
    st.table(df)
    st.download_button("📥 DOWNLOAD CSV", data=df.to_csv(index=False), file_name="log.csv", mime="text/csv", use_container_width=True)

# STEP 5
st.markdown('<p class="step-label">STEP 5: <span class="neon-text">SUPPLIES</span></p>', unsafe_allow_html=True)
st.markdown(f'<div class="suggestion-box"><span class="tip-tag" style="color: #0EA5E9;">🤝 PARTNER</span><p style="margin:0; font-weight:600;">{random.choice(TIP_POOL["s5"])}</p></div>', unsafe_allow_html=True)

supply_html = """
<div class="flex-grid">
    <a href="https://google.com" target="_blank" class="m-btn c-google">GOOGLE SHOP</a>
    <a href="https://amazon.com" target="_blank" class="m-btn c-amazon">AMAZON PRO</a>
</div>"""
st.components.v1.html(supply_html, height=85)

if st.button("🔄 RESET MASTER SESSION", use_container_width=True):
    st.session_state.inventory = []
    st.session_state.app_state = {'analysis': "", 'listing_out': "", 'style': "Pro"}
    st.session_state.update({"notes_input": ""})
    st.rerun()
