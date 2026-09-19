import streamlit as st

st.set_page_config(
    page_title="CodGuard — Stop Fake COD Orders Before They Ship",
    page_icon="🛡️",
    layout="wide",
)

# Custom Styling to match a modern SaaS look
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e293b;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748b;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<p class="main-header">CodGuard 🛡️</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Stop Fake COD Orders Before They Ship</p>', unsafe_allow_html=True)
st.divider()

# Sidebar for controls or navigation
st.sidebar.title("CodGuard Navigation")
app_mode = st.sidebar.selectbox("Choose Mode", ["Order Verification Dashboard", "Risk Analytics", "Settings"])

if app_mode == "Order Verification Dashboard":
    st.subheader("Verify Incoming Order Risk")
    
    col1, col2 = st.columns(2)
    with col1:
        customer_name = st.text_input("Customer Name", "John Doe")
        phone = st.text_input("Phone Number", "+91 9876543210")
        pincode = st.text_input("Delivery Pincode", "614625")
    
    with col2:
        order_amount = st.number_input("Order Amount (₹)", min_value=100, value=1499)
        previous_orders = st.number_input("Past Orders", min_value=0, value=2)
        rto_history = st.selectbox("Previous RTO (Return to Origin) History", ["None", "Low", "High"])

    if st.button("Analyze Risk Score", type="primary"):
        # Dummy risk logic for demonstration
        risk_score = 15 if rto_history == "None" else 85
        
        if risk_score < 40:
            st.success(f"Low Risk (Score: {risk_score}%). Recommended Action: **Ship Order** ✅")
        elif risk_score < 75:
            st.warning(f"Moderate Risk (Score: {risk_score}%). Recommended Action: **Verify via WhatsApp/OTP** ⚠️")
        else:
            st.error(f"High Risk (Score: {risk_score}%). Recommended Action: **Cancel / Require Prepaid** ❌")

elif app_mode == "Risk Analytics":
    st.subheader("RTO & Fraud Trends")
    st.info("Analytics dashboard will display metrics on prevented RTOs, verified phone numbers, and saved shipping costs.")

else:
    st.subheader("CodGuard Settings")
    st.text_input("API Key Integration", "cg_live_************************")
    st.checkbox("Enable Auto-Verification via WhatsApp", value=True)
    st.button("Save Changes")
