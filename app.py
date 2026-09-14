import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# --- ADSTERRA CONFIGURATION ---
ADSTERRA_SMARTLINK = "https://example-adsterra-smartlink.com" 
ADSTERRA_BANNER_HTML = """
<div style="text-align:center;">
    <a href="https://example-adsterra-smartlink.com" target="_blank">
        <img src="https://placeholder.com" alt="Ad"/>
    </a>
</div>
"""

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cinematic Colour Grading AI", layout="centered", page_icon="🎨")

st.markdown("""
    <style>
    .main { background-color: #fafafa; }
    div.stButton > button:first-child {
        background-color: #FF4B4B; color: white; border-radius: 8px; width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎨 Pro Colour Grader & DSLR Optimizer")
st.write("Apply high-end cinematic color grading profiles instantly without changing your faces or backgrounds.")

# --- TOP AD BANNER ---
st.components.v1.html(ADSTERRA_BANNER_HTML, height=100)

# --- ADVANCED COLOUR GRADING ENGINE ---
def apply_colour_grade(pil_image, profile, intensity):
    img_np = np.array(pil_image)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    graded = img_bgr.copy()
    
    if profile == "Cinematic Teal & Orange":
        ycrcb = cv2.cvtColor(graded, cv2.COLOR_BGR2YCrCb)
        y, cr, cb = cv2.split(ycrcb)
        
        # Shift chrominance safely using numpy to avoid clipping issues
        cr = cv2.add(cr, 10)
        cb = cv2.subtract(cb, 10)
        
        graded = cv2.merge((y, cr, cb))
        graded = cv2.cvtColor(graded, cv2.COLOR_YCrCb2BGR)

    elif profile == "Moody Vintage / Film":
        # FIXED LINE 53: Convert image to float32 before applying matrix, then clip back to uint8
        matrix = np.array([[0.131, 0.534, 0.272],
                           [0.168, 0.686, 0.349],
                           [0.189, 0.769, 0.393]])
        graded = cv2.transform(graded.astype(np.float32), matrix)
        graded = np.clip(graded, 0, 255).astype(np.uint8)
        
    elif profile == "Cyberpunk / Neon":
        lab = cv2.cvtColor(graded, cv2.COLOR_BGR2Lab)
        l, a, b = cv2.split(lab)
        a = cv2.equalizeHist(a)
        b = cv2.equalizeHist(b)
        graded = cv2.merge((l, a, b))
        graded = cv2.cvtColor(graded, cv2.COLOR_Lab2BGR)

    # Blend original and graded image together using intensity factor
    blended_bgr = cv2.addWeighted(graded, intensity, img_bgr, 1.0 - intensity, 0)
    final_pil = Image.fromarray(cv2.cvtColor(blended_bgr, cv2.COLOR_BGR2RGB))
    
    return final_pil

# --- UI COMPONENT ---
uploaded_file = st.file_uploader("Upload your image (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    original_image = Image.open(uploaded_file)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original")
        st.image(original_image, use_container_width=True)
        
    st.sidebar.header("🎨 Color Grading Panel")
    selected_profile = st.sidebar.selectbox(
        "Select Color Profile",
        ["Cinematic Teal & Orange", "Moody Vintage / Film", "Cyberpunk / Neon"]
    )
    
    grade_intensity = st.sidebar.slider("Grading Filter Intensity", 0.1, 1.0, 0.7, step=0.05)
    
    with st.spinner("Applying premium color grading look..."):
        processed_image = apply_colour_grade(original_image, selected_profile, grade_intensity)
        
    with col2:
        st.subheader("Color Graded")
        st.image(processed_image, use_container_width=True)
        
    st.write("---")
    st.subheader("📥 Export Final Creation")
    
    buf = io.BytesIO()
    processed_image.save(buf, format="JPEG", quality=95)
    byte_im = buf.getvalue()
    
    st.warning("⚠️ High-resolution processing generates server loads. Please support us by looking at our sponsor link below!")
    
    # FIXED LINE 103: Added explicit count '2' into st.columns parameter
    col_dl, col_ad = st.columns(2)
    with col_dl:
        st.download_button(
            label="💾 Download Color Graded Image",
            data=byte_im,
            file_name="color_graded.jpg",
            mime="image/jpeg"
        )
    with col_ad:
        st.markdown(f'<a href="{ADSTERRA_SMARTLINK}" target="_blank"><button style="background-color:#4CAF50; color:white; border:none; padding:10px 24px; border-radius:8px; width:100%; cursor:pointer; font-weight:bold;">🚀 Unlock Maximum Download Speed</button></a>', unsafe_allow_html=True)

# --- BOTTOM AD BANNER ---
st.write("---")
st.components.v1.html(ADSTERRA_BANNER_HTML, height=250)

