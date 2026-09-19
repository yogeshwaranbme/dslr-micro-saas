import streamlit as st
import streamlit.components.v1 as components

# Set page configuration to match the title and look professional
st.set_page_config(
    page_title="CodGuard — Stop Fake COD Orders Before They Ship",
    page_icon="🛡️",
    layout="wide",
)

# Custom HTML string containing your exact head elements and assets
codguard_html = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
    <title>CodGuard — Stop Fake COD Orders Before They Ship</title>
    <!-- Note: Ensure absolute paths or relative paths point correctly to your assets -->
    <script type="module" crossorigin src="/assets/index-B2BHnLXs.js"></script>
    <link rel="stylesheet" crossorigin href="/assets/index-BFzxl_TV.css">
  </head>
  <body style="margin:0; padding:0; font-family: 'Inter', sans-serif;">
    <div id="root"></div>
  </body>
</html>
"""

# Render the HTML component inside Streamlit (adjust height as necessary)
components.html(codguard_html, height=800, scrolling=True)
