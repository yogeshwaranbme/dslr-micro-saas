import random
import time
import streamlit as st

# Set page config
st.set_page_config(
    page_title="CodGuard - COD Fraud & Address Verification",
    page_icon="🛡️",
    layout="centered",
)

# Initialize session state for multi-step checkout simulation
if "step" not in st.session_state:
    st.session_state.step = "cart"  # steps: cart, checkout, otp_modal, success, blocked
if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = None
if "otp_input" not in st.session_state:
    st.session_state.otp_input = ""
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "cart_data" not in st.session_state:
    st.session_state.cart_data = {
        "name": "Yogeshwaran R",
        "phone": "+91 9876543210",
        "pincode": "614628",
        "city": "Avikkottai",
        "product": "Wireless Earbuds Pro",
        "amount": 1499,
    }

# Mock database of valid postal codes for offline validation
VALID_PINCODES = {
    "614628": "Avikkottai / Pattukkottai Region",
    "613001": "Thanjavur Head Office",
    "614001": "Mannargudi Region",
    "600001": "Chennai NSC Bose Road",
    "560001": "Bangalore GPO",
}


def reset_flow():
    st.session_state.step = "cart"
    st.session_state.attempts = 0
    st.session_state.generated_otp = None
    st.session_state.otp_input = ""


# --- HEADER ---
st.title("🛡️ CodGuard Micro-SaaS Demo")
st.markdown(
    "*Lightweight COD Fraud & Address Verification Checkout Simulation (Zero External APIs/Tokens)*"
)
st.divider()

# --- STEP 1: MERCHANT CONFIGURATION SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Merchant Settings")
    st.markdown("Configure widget rules for your store simulation.")
    otp_channel = st.selectbox(
        "Verification Channel", ["WhatsApp Business", "SMS Gateway"]
    )
    max_attempts = st.slider("Max OTP Tries", 1, 5, 3)
    auto_fail_fake = st.checkbox(
        "Auto-flag invalid postal codes", value=True
    )

    st.divider()
    st.markdown("### 📊 Live Analytics")
    st.metric(label="Protected COD Orders", value="1,284")
    st.metric(label="RTO Prevented", value="24.2%")
    st.metric(label="Widget Latency", value="240 ms")

# --- STEP 2: SIMULATED STOREFRONT (CART) ---
if st.session_state.step == "cart":
    st.subheader("🛍️ Demo D2C Brand Storefront (Checkout Page)")
    st.markdown(
        "You have added a product to your cart. Proceed to fill out your details and choose **Cash on Delivery (COD)**."
    )

    with st.form("checkout_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", value=st.session_state.cart_data["name"])
            phone = st.text_input(
                "Phone Number", value=st.session_state.cart_data["phone"]
            )
        with col2:
            pincode = st.text_input(
                "Postal / ZIP Code", value=st.session_state.cart_data["pincode"]
            )
            city = st.text_input("City", value=st.session_state.cart_data["city"])

        product = st.selectbox(
            "Selected Product",
            [
                "Wireless Earbuds Pro (₹1,499)",
                "Smart Fitness Band (₹2,199)",
                "RGB Mechanical Keyboard (₹3,499)",
            ],
        )

        payment_method = st.radio(
            "Payment Method",
            ["Cash on Delivery (COD)", "Credit/Debit Card (Prepaid)"],
            index=0,
        )

        submitted = st.form_submit_button("Place Order")

        if submitted:
            # Save state
            st.session_state.cart_data["name"] = name
            st.session_state.cart_data["phone"] = phone
            st.session_state.cart_data["pincode"] = pincode
            st.session_state.cart_data["city"] = city

            # Postal code check
            if auto_fail_fake and pincode not in VALID_PINCODES:
                st.error(
                    f"❌ Invalid Postal Code '{pincode}'. Please enter a valid delivery region code (e.g., 614628, 613001, 600001)."
                )
            elif "Cash on Delivery" in payment_method:
                # Trigger CodGuard Interception Modal Workflow
                st.session_state.step = "otp_modal"
                st.session_state.generated_otp = str(
                    random.randint(1000, 9999)
                )  # Simulated OTP generated locally
                st.rerun()
            else:
                st.session_state.step = "success"
                st.rerun()

# --- STEP 3: THE INTERCEPTION MODAL (OTP VERIFICATION) ---
elif st.session_state.step == "otp_modal":
    st.info(
        "⚡ **CodGuard Widget Intercepted:** Cash on Delivery order detected. Verifying buyer authenticity to prevent RTO loss..."
    )

    # Simulated notification banner showing local mock dispatch
    st.warning(
        f"📱 **[SIMULATED {otp_channel.upper()}]** OTP sent to **{st.session_state.cart_data['phone']}**. "
        f"(For testing purposes, your verification code is: **{st.session_state.generated_otp}**)"
    )

    st.markdown("### 🔐 Enter Verification Code")
    st.markdown(
        f"Please enter the 4-digit code sent via {otp_channel} to confirm your COD order for `{st.session_state.cart_data['product']}`."
    )

    with st.form("otp_form"):
        entered_otp = st.text_input(
            "4-Digit OTP", max_chars=4, type="default"
        )
        col_verify, col_cancel = st.columns(2)
        verify_submitted = col_verify.form_submit_button("Verify & Place Order")
        cancel_submitted = col_cancel.form_submit_button("Cancel Order")

        if cancel_submitted:
            st.session_state.step = "blocked"
            st.rerun()

        if verify_submitted:
            if entered_otp == st.session_state.generated_otp:
                st.session_state.step = "success"
                st.rerun()
            else:
                st.session_state.attempts += 1
                remaining = max_attempts - st.session_state.attempts
                if remaining <= 0:
                    st.session_state.step = "blocked"
                    st.rerun()
                else:
                    st.error(
                        f"❌ Incorrect OTP. You have {remaining} attempt(s) remaining."
                    )

# --- STEP 4A: ORDER SUCCESS (VERIFIED & SAFE) ---
elif st.session_state.step == "success":
    st.success("🎉 Order Successfully Placed & Verified!")
    st.balloons()

    st.markdown("### Order Summary")
    st.success(
        f"""
- **Status:** Verified & Safe (CodGuard Protected)
- **Customer:** {st.session_state.cart_data['name']} ({st.session_state.cart_data['phone']})
- **Location:** Pincode {st.session_state.cart_data['pincode']} ({VALID_PINCODES.get(st.session_state.cart_data['pincode'], 'Verified Zone')})
- **Payment:** Cash on Delivery (OTP Authenticated)
- **Risk Score:** 0.02% (Low Risk)
    """
    )

    if st.button("Simulate Another Checkout"):
        reset_flow()
        st.rerun()

# --- STEP 4B: ORDER BLOCKED / HIGH RISK ---
elif st.session_state.step == "blocked":
    st.error("🚫 Order Blocked / Flagged as High Risk")
    st.markdown(
        """
    **Reason:** Maximum OTP verification attempts exceeded or checkout abandoned at security confirmation step.
    
    *CodGuard Action:* The order has been suppressed from syncing to Shopify/WooCommerce fulfillment, saving the merchant forward and return shipping logistics costs.
    """
    )

    if st.button("Retry Checkout Simulation"):
        reset_flow()
        st.rerun()
