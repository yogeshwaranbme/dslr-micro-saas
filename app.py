import streamlit as st
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

# Configure Streamlit page layout
st.set_page_config(
    page_title="85mm f/2.8 DSLR Emulator",
    page_icon="📸",
    layout="wide"
)

# Render main UI headers
st.title("📸 High-End Full-Frame DSLR Emulator (85mm f/2.8 Focus)")
st.markdown("Recreate authentic studio photography with shallow depth of field, preserved skin pores, and professional color grading.")

# Setup sidebar for precise control over the camera calibration
st.sidebar.header("📷 Camera & Lens Calibration")

# f/2.8 provides a more moderate, realistic background falloff than f/1.4
aperture_blur = st.sidebar.slider(
    "Lens Perimeter Blur (Simulated f/2.8 Falloff)", 
    min_value=0, 
    max_value=10, 
    value=4, 
    step=1
)

lighting_contrast = st.sidebar.slider(
    "Studio Key Light Contrast", 
    min_value=1.0, 
    max_value=1.4, 
    value=1.12, 
    step=0.02
)

color_grade = st.sidebar.selectbox(
    "Cinematic Film Stock Profile",
    ["Kodak Portra 400 (Warm & Natural)", "Fujifilm Pro 400H (Cool & Clean)", "Neutral Studio True-Color"]
)

# Application core layout split into two viewports
col1, col2 = st.columns(2)

with col1:
    st.subheader("Reference Image Input")
    uploaded_file = st.file_uploader("Upload reference photo (Identity and features will be preserved)", type=["jpg", "jpeg", "png"])

with col2:
    st.subheader("Authentic DSLR Rendered Output")
    if uploaded_file is not None:
        # Load the source image safely as RGB
        src_image = Image.open(uploaded_file).convert("RGB")
        col1.image(src_image, use_container_width=True)
        
        # --- 1. Compute f/2.8 Depth of Field Falloff ---
        # Generate a geometric matrix to keep the center identity area 100% sharp 
        # while gently bleeding blur into the background.
        width, height = src_image.size
        x = np.linspace(-1.2, 1.2, width)
        y = np.linspace(-1.2, 1.2, height)
        X, Y = np.meshgrid(x, y)
        
        # Create a smooth focal mask (1.0 = center/sharp, drops off towards edges)
        mask_matrix = np.clip(1.0 - (X**2 + Y**2), 0, 1)
        # Smooth out the transition boundaries
        mask_image = Image.fromarray((mask_matrix * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=30))
        
        # Apply the background perimeter blur layer
        blurred_layer = src_image.filter(ImageFilter.GaussianBlur(radius=aperture_blur))
        processed_image = Image.composite(src_image, blurred_layer, mask_image)
        
        # --- 2. Professional Studio Lighting Adjustment ---
        # Subtle enhancement avoiding over-sharpening or plastic AI flattening
        contrast_adjuster = ImageEnhance.Contrast(processed_image)
        processed_image = contrast_adjuster.enhance(lighting_contrast)
        
        # --- 3. Cinematic Color Grading Remapping ---
        r, g, b = processed_image.split()
        if color_grade == "Kodak Portra 400 (Warm & Natural)":
            r = r.point(lambda i: min(255, int(i * 1.04)))
            g = g.point(lambda i: min(255, int(i * 1.01)))
            b = b.point(lambda i: int(i * 0.96))
        elif color_grade == "Fujifilm Pro 400H (Cool & Clean)":
            r = r.point(lambda i: int(i * 0.97))
            g = g.point(lambda i: min(255, int(i * 1.03)))
            b = b.point(lambda i: min(255, int(i * 1.05)))
            
        processed_image = Image.merge("RGB", (r, g, b))
        
        # Output the finished photograph
        st.image(processed_image, use_container_width=True)
        
        # Preparation for standard output download
        st.download_button(
            label="Download Authentic DSLR Render",
            data=uploaded_file.getvalue(),
            file_name="dslr_f2.8_portrait.png",
            mime="image/png"
        )
    else:
        st.info("Awaiting reference photo upload in the left panel to execute camera emulation logic.")
