import streamlit as st
import replicate
import os
import requests
from PIL import Image, ImageFilter
import io

# Ensure API Key exists
if "REPLICATE_API_TOKEN" not in os.environ:
    st.error("🔑 REPLICATE_API_TOKEN environment variable not set. Please set it in your Streamlit Cloud Secrets.")
    st.stop()

st.set_page_config(page_title="DSLR AI Engine", page_icon="📸", layout="centered")

# --- REPLACE WITH YOUR ACTUAL GITHUB PAGES URL ---
# This points directly to where your repository's public WebGL canvas is hosted
UNITY_WEBGL_URL = "https://github.com/yogeshwaranbme/dslr-micro-saas/blob/main/public/webgl/index.html"

# --- INITIALIZE STATE ENGINE ---
if "step" not in st.session_state:
    st.session_state.step = "upload"  # Steps: upload -> processing -> ad_gate -> unlocked
if "original_img" not in st.session_state:
    st.session_state.original_img = None
if "blurred_preview" not in st.session_state:
    st.session_state.blurred_preview = None
if "hd_url" not in st.session_state:
    st.session_state.hd_url = None

st.title("📸 DSLR Professional AI Enhancer")
st.caption("Instantly convert grainy mobile photos into crystal clear DSLR-quality captures.")

# --- STEP 1: UPLOAD PIPELINE ---
if st.session_state.step == "upload":
    uploaded_file = st.file_uploader("Choose a portrait or photo to enhance...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.session_state.original_img = Image.open(uploaded_file)
        
        # Buffer original bytes for the AI payload
        buf = io.BytesIO()
        st.session_state.original_img.save(buf, format="JPEG")
        st.session_state.img_bytes = buf.getvalue()
        
        if st.button("✨ Enhance to DSLR Quality", use_container_width=True):
            st.session_state.step = "processing"
            st.rerun()

# --- STEP 2: BACKEND AI PROCESSING ---
elif st.session_state.step == "processing":
    st.info("⚙️ AI is sharpening details and building realistic depth-of-field blur...")
    progress_bar = st.progress(0)
    
    try:
        input_data = io.BytesIO(st.session_state.img_bytes)
        
        # Fire payload to Replicate using the Real-ESRGAN package
        # face_enhance=True applies optimized face feature recovery to simulate an authentic DSLR portrait
        output = replicate.run(
            "nightmareai/real-esrgan:latest",
            input={
                "image": input_data,
                "scale": 2,
                "face_enhance": True
            }
        )
        
        if isinstance(output, list) and len(output) > 0:
            st.session_state.hd_url = output[0]
        else:
            st.session_state.hd_url = output
            
        progress_bar.progress(100)
        
        # Create a heavily blurred proxy image from the original asset for the ad gate UI
        st.session_state.blurred_preview = st.session_state.original_img.filter(ImageFilter.GaussianBlur(radius=15))
        
        st.session_state.step = "ad_gate"
        st.rerun()
        
    except Exception as e:
        st.error(f"AI Processing Failed: {str(e)}")
        if st.button("↩️ Try Again"):
            st.session_state.step = "upload"
            st.rerun()

# --- STEP 3: THE UNITY AD GATE ---
elif st.session_state.step == "ad_gate":
    st.warning("🔒 Your DSLR photo is ready! Watch a quick video to unlock the HD version.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(st.session_state.original_img, caption="Original Mobile Shot", use_container_width=True)
    with col2:
        st.image(st.session_state.blurred_preview, caption="✨ DSLR Premium (Locked)", use_container_width=True)

    # SECURE WEB CALLBACK ENTRY:
    # Catch custom URL parameters passed back from the inner WebGL iframe upon ad completion
    params = st.context.query_params
    if "status" in params and params["status"] == "reward_success":
        st.context.query_params.clear()  # Purge token to prevent re-execution exploits
        st.session_state.step = "unlocked"
        st.rerun()

    # INJECT PRODUCTION NATIVE UNITY AD IFRAME 
    st.components.v1.html(
        f"""
        <iframe src="{UNITY_WEBGL_URL}" 
                style="width:100%; height:180px; border:none; scrollbar:none; border-radius:10px; background:#f0f2f6;">
        </iframe>
        """,
        height=200
    )

# --- STEP 4: DELIVER VALUE (UNLOCKED PIPELINE) ---
elif st.session_state.step == "unlocked":
    st.balloons()
    st.success("🎉 High Definition DSLR Enhancement Complete!")
    
    # Securely retrieve the file from cloud servers directly onto our backend environment
    try:
        response = requests.get(st.session_state.hd_url)
        hd_bytes = response.content
        
        st.image(st.session_state.hd_url, caption="📸 Final Pro-Tier DSLR Photo", use_container_width=True)
        
        st.download_button(
            label="💾 Save to Camera Roll (HD)",
            data=hd_bytes,
            file_name="dslr_enhanced.png",
            mime="image/png",
            use_container_width=True
        )
    except Exception as e:
        st.error("Could not fetch the enhanced photo from server storage. Please try again.")
    
    if st.button("🔄 Enhance Another Photo", use_container_width=True):
        st.session_state.step = "upload"
        st.session_state.original_img = None
        st.session_state.blurred_preview = None
        st.session_state.hd_url = None
        st.rerun()
