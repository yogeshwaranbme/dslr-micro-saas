import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io

# --- ADSTERRA CONFIGURATION ---
# Replace these placeholder links with your actual codes from the Adsterra Publisher Dashboard
ADSTERRA_SMARTLINK = "https://www.profitableratecpmnetwork.com/ht2mnivmg?key=46a0e809bd9560cf22f3e6c3bc983134" 
ADSTERRA_BANNER_HTML = """
<div style="text-align:center;">
    <!-- Paste your 728x90 or 300x250 Adsterra Script/Iframe below -->
    <script async="async" data-cfasync="false" src="https://pl31341379.profitableratecpmnetwork.com/d5ab78a2c49c200d979abfd7d409f186/invoke.js"></script>
<div id="container-d5ab78a2c49c200d979abfd7d409f186"></div>
    <a href="https://example-adsterra-smartlink.com" target="_blank">
        <img src="https://placeholder.com" alt="Ad"/>
    </a>
</div>
"""

# --- PAGE CONFIG ---
st.set_page_config(page_title="DSLR Photo Enhancer AI", layout="centered", page_icon="📸")

# Custom CSS to integrate seamlessly
st.markdown("""
    <style>
    .main { background-color: #fafafa; }
    div.stButton > button:first-child {
        background-color: #FF4B4B; color: white; border-radius: 8px; width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📸 AI DSLR Quality Photo Enhancer")
st.write("Transform your standard smartphone photos into professional DSLR-looking shots instantly.")

# --- TOP AD BANNER ---
st.components.v1.html(ADSTERRA_BANNER_HTML, height=100)

# --- IMAGE PIPELINE FUNCTION ---
def convert_to_dslr(pil_image, sharp_val, color_val, blur_bkg):
    # 1. Convert to Open CV format for color space handling
    img_np = np.array(pil_image)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) for DSLR-like dynamic range
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    enhanced_bgr = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
    # Convert back to PIL
    enhanced_pil = Image.fromarray(cv2.cvtColor(enhanced_bgr, cv2.COLOR_BGR2RGB))
    
    # 2. Adjust Vibrance/Color
    color_enhancer = ImageEnhance.Color(enhanced_pil)
    enhanced_pil = color_enhancer.enhance(color_val) # Boost midtones
    
    # 3. Adjust Sharpness/Clarity
    sharp_enhancer = ImageEnhance.Sharpness(enhanced_pil)
    enhanced_pil = sharp_enhancer.enhance(sharp_val)
    
    # 4. Optional Bokeh/Depth of Field Simulation
    if blur_bkg:
        # Subtle unsharp mask to isolate details slightly
        enhanced_pil = enhanced_pil.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
        
    return enhanced_pil

# --- UI COMPONENT ---
uploaded_file = st.file_uploader("Upload a normal photo (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    original_image = Image.open(uploaded_file)
    
    # Multi-column UI for comparison
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original")
        st.image(original_image, use_container_width=True)
        
    # Sidebar control adjustments mimicking DSLR features
    st.sidebar.header("🔧 Pro DSLR Adjustments")
    sharpness = st.sidebar.slider("Clarity / Sharpness", 1.0, 3.0, 1.8, step=0.1)
    color_vibrance = st.sidebar.slider("Color Depth (Vibrance)", 1.0, 2.5, 1.3, step=0.1)
    simulate_bokeh = st.sidebar.checkbox("Simulate Lens Depth of Field", value=True)
    
    # Process image
    with st.spinner("Processing to DSLR standard..."):
        processed_image = convert_to_dslr(original_image, sharpness, color_vibrance, simulate_bokeh)
        
    with col2:
        st.subheader("DSLR Standard")
        st.image(processed_image, use_container_width=True)
        
    # --- MONETIZATION WALL ---
    st.write("---")
    st.subheader("📥 Export Final Creation")
    
    # Setup download button buffer
    buf = io.BytesIO()
    processed_image.save(buf, format="JPEG", quality=95)
    byte_im = buf.getvalue()
    
    # Monetization Strategy: Force an Adsterra SmartLink click or show ad alongside download
    st.warning("⚠️ High-resolution processing generates server loads. Please support us by looking at our sponsor link below!")
    
    col_dl, col_ad = st.columns([1, 1])
    with col_dl:
        st.download_button(
            label="💾 Download Ultra-HD Image",
            data=byte_im,
            file_name="dslr_enhanced.jpg",
            mime="image/jpeg"
        )
    with col_ad:
        # Button navigating directly to Adsterra SmartLink
        st.markdown(f'<a href="{ADSTERRA_SMARTLINK}" target="_blank"><button style="background-color:#4CAF50; color:white; border:none; padding:10px 24px; border-radius:8px; width:100%; cursor:pointer; font-weight:bold;">🚀 Unlock Maximum Download Speed</button></a>', unsafe_allow_html=True)

# --- BOTTOM AD BANNER ---
st.write("---")
st.components.v1.html(ADSTERRA_BANNER_HTML, height=250)

