import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            platform TEXT,
            customer_name TEXT,
            mobile_number TEXT,
            item_name TEXT,
            total_amount REAL,
            order_status TEXT,
            order_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- Helper Functions ---
def add_order(order_id, platform, customer_name, mobile_number, item_name, total_amount, order_status, order_date):
    try:
        conn = sqlite3.connect('orders.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO orders (order_id, platform, customer_name, mobile_number, item_name, total_amount, order_status, order_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (order_id, platform, customer_name, mobile_number, item_name, total_amount, order_status, order_date))
        conn.commit()
        conn.close()
        return True, "Order added successfully!"
    except sqlite3.IntegrityError:
        return False, "Order ID already exists!"

def get_orders_by_mobile(mobile_number):
    conn = sqlite3.connect('orders.db')
    query = "SELECT * FROM orders WHERE mobile_number LIKE ?"
    df = pd.read_sql(query, conn, params=(f"%{mobile_number}%",))
    conn.close()
    return df

# --- Streamlit UI ---
st.set_page_config(page_title="Family Order Tracker", page_icon="📦", layout="wide")

st.title("📦 Family E-Commerce Order Tracker")
st.markdown("Track orders from **Amazon, Flipkart, and Meesho** linked to your family's mobile numbers.")

# Sidebar Navigation
menu = st.sidebar.selectbox("Navigation", ["Track Orders", "Add New Order (Manual)"])

if menu == "Track Orders":
    st.header("🔍 Track Orders by Mobile Number")
    
    search_mobile = st.text_input("Enter Mobile Number", placeholder="e.g., 9876543210")
    
    if search_mobile:
        df_orders = get_orders_by_mobile(search_mobile)
        
        if not df_orders.empty:
            st.success(f"Found {len(df_orders)} order(s) for mobile number: {search_mobile}")
            
            # Metrics
            total_spent = df_orders['total_amount'].sum()
            col1, col2 = st.columns(2)
            col1.metric("Total Orders Found", len(df_orders))
            col2.metric("Total Spent (₹)", f"₹{total_spent:,.2f}")
            
            # Display Table
            st.dataframe(df_orders, use_container_width=True)
        else:
            st.warning("No orders found for this mobile number.")

elif menu == "Add New Order (Manual)":
    st.header("➕ Add a Purchase Order")
    st.markdown("*(Tip: You can automate this later by integrating Python's email parsing library `imaplib` to read confirmation emails automatically).*")
    
    with st.form("order_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            order_id = st.text_input("Order ID / Tracking ID")
            platform = st.selectbox("Platform", ["Amazon", "Flipkart", "Meesho", "Other"])
            customer_name = st.text_input("Family Member Name")
            mobile_number = st.text_input("Registered Mobile Number")
            
        with col2:
            item_name = st.text_input("Item Name / Description")
            total_amount = st.number_input("Total Amount (₹)", min_value=0.0, format="%.2f")
            order_status = st.selectbox("Order Status", ["Ordered", "Shipped", "Out for Delivery", "Delivered", "Cancelled"])
            order_date = st.date_input("Order Date", datetime.today())
            
        submit_button = st.form_submit_button("Save Order")
        
        if submit_button:
            if order_id and mobile_number and item_name:
                success, msg = add_order(
                    order_id, platform, customer_name, mobile_number, 
                    item_name, total_amount, order_status, str(order_date)
                )
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                    st.error("Please fill in all mandatory fields (Order ID, Mobile Number, Item Name).")
