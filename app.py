import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. PAGE CONFIG (NO ICONS)
st.set_page_config(page_title="Lazy Lister", layout="centered")

# 2. THE SIRO TRUST "COLOR-LOCK" CSS
st.markdown("""
<style>
    /* Global Background */
    .stApp { background-color: #0F172A; color: white; }
    
    /* Step 4: Amazon Brown Button */
    div.stButton > button:first-child {
        background-color: #372810 !important;
        color: white !important;
        border: 2px solid #FF9900 !important;
        width: 100%;
        font-weight: bold;
    }

    /* Step 5: Google Red Link Buttons */
    .st-key-amz_restock a, .st-key-goog_deals a {
        background-color: #DB4437 !important;
        color: white !important;
        border-radius: 5px;
        padding: 12px;
        text-decoration: none;
        display: block;
        text-align: center;
        font-weight: bold;
        margin-bottom: 10px;
    }

    /* Checklist Styling */
    .inventory-box { background-color: white; padding: 15px; border-radius: 10px; color: black; }
    .stCheckbox label { color: black !important; font-weight: bold !important; }
</style>
""", unsafe_content_allowed=True)

# 3. API INITIALIZATION
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Check your secrets.toml for GOOGLE_API_KEY")

# 4. CORE PROCESSING
def process_listing(img_file, notes):
    img = Image.open(img_file)
    prompt = f"Analyze this reseller item. Notes: {notes}. Provide ITEM_NAME, PRICE, DESCRIPTION, and 3 TIPS."
    response = model.generate_content([prompt, img])
    return response.text

# 5. THE UI WORKFLOW (FOLLOWING YOUR EXACT DIRECTIONS)
st.title("Lazy Lister")
st.subheader("Premium Reseller Assistant")

# STEP 1: SCAN
img_file = st.file_uploader("Step 1: Scan Item", type=['jpg', 'png', 'jpeg'])

# STEP 2: NOTES
notes = st.text_input("Step 2: Voice/Text Notes")

# STEP 3 & 4: ANALYSIS
if st.button("Step 3 & 4: Analyze and Generate"):
    if img_file:
        with st.spinner("Analyzing..."):
            try:
                result = process_listing(img_file, notes)
                st.session_state['listing_data'] = result
                st.markdown("### Results")
                st.write(result)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please upload an image.")

# STEP 5: SYNC & SHARE
if 'listing_data' in st.session_state:
    st.divider()
    st.subheader("Step 5: Market Sync & Share")
    
    # Extract name for search
    lines = st.session_state['listing_data'].split('\n')
    search_query = "Item"
    for line in lines:
        if "ITEM_NAME" in line:
            search_query = line.split(":")[-1].strip()

    col1, col2 = st.columns(2)
    with col1:
        st.link_button("Amazon Restock Price", f"https://www.amazon.com/s?k={search_query}", key="amz_restock")
    with col2:
        st.link_button("Google Deals", f"https://www.google.com/search?q={search_query}", key="goog_deals")

    if st.button("Share Listing"):
        st.info("Listing copied to clipboard logic ready.")

# INVENTORY LOG
st.divider()
if 'inventory' not in st.session_state:
    st.session_state['inventory'] = []

if 'listing_data' in st.session_state and st.button("Add to Inventory Log"):
    if search_query not in st.session_state['inventory']:
        st.session_state['inventory'].append(search_query)

if st.session_state['inventory']:
    st.markdown('<div class="inventory-box">', unsafe_content_allowed=True)
    for item in st.session_state['inventory']:
        st.checkbox(f"Ready: {item}", key=item)
    st.markdown('</div>', unsafe_content_allowed=True)