import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter

# Configure Streamlit page layout
st.set_page_config(
    page_title="4K DSLR Color & Clarity Engine",
    page_icon="📸",
    layout="wide"
)

# Render main UI headers
st.title("📸 Authentic 4K DSLR Clarity & Color Engine")
st.markdown("Upscale reference photos to 4K UHD resolution, enhance pore textures without AI smoothing, and apply high-end cinematic grading with **zero blur**.")

# Setup sidebar for precise camera parameters
st.sidebar.header("🎛️ Camera & Texture Controls")

target_resolution = st.sidebar.checkbox(
    "Upscale to 4K UHD (3840 x 2160)", 
    value=True,
    help="Resamples the image up to high-fidelity 4K dimensions using sharp bicubic interpolation."
)

pore_definition = st.sidebar.slider(
    "Natural Skin Pore Clarity (Unsharp Mask)", 
    min_value=0.0, 
    max_value=2.0, 
    value=0.8, 
    step=0.1
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
    st.subheader("Authentic 4K DSLR Rendered Output")
    if uploaded_file is not None:
        # Load the source image safely as RGB
        src_image = Image.open(uploaded_file).convert("RGB")
        col1.image(src_image, use_container_width=True)
        
        processed_image = src_image.copy()

        # --- 1. High-Fidelity 4K Resolution Upscaling ---
        if target_resolution:
            # Standard 4K UHD Aspect Ratio target (3840 x 2160)
            # We calculate proportional scaling to hit 4K limits without stretching features
            target_w = 3840
            target_h = 2160
            
            src_w, src_h = processed_image.size
            scale = max(target_w / src_w, target_h / src_h)
            new_w = int(src_w * scale)
            new_h = int(src_h * scale)
            
            # Using Image.Resampling.BICUBIC for crisp pixel texture without AI plastic artifacts
            processed_image = processed_image.resize((new_w, new_h), Image.Resampling.BICUBIC)
        
        # --- 2. Skin Pore and Detail Preservation (No Blur) ---
        if pore_definition > 0:
            # Applies a clean camera-lens sharpness mask to pull out crisp textures
            processed_image = processed_image.filter(
                ImageFilter.UnsharpMask(radius=1.5, percent=int(pore_definition * 100), threshold=3)
            )

        # --- 3. Professional Studio Lighting Adjustment ---
        contrast_adjuster = ImageEnhance.Contrast(processed_image)
        processed_image = contrast_adjuster.enhance(lighting_contrast)
        
        # --- 4. Cinematic Color Grading Remapping ---
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
        
        # Output the finished 4K photograph
        st.image(processed_image, use_container_width=True)
        
        # Save output image locally into a bytes buffer for direct 4K download
        import io
        img_buffer = io.BytesIO()
        processed_image.save(img_buffer, format="PNG", quality=100)
        byte_data = img_buffer.getvalue()

        # Preparation for standard output download
        st.download_button(
            label="Download Authentic 4K DSLR Render",
            data=byte_data,
            file_name="dslr_4k_portrait.png",
            mime="image/png"
        )
    else:
        st.info("Awaiting reference photo upload in the left panel to execute camera emulation logic.")
