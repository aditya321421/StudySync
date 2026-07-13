import streamlit as st
import pypdf
import json
import pandas as pd
import requests
from groq import Groq

# Initialize Groq Client
client = Groq()

# Configure page settings
st.set_page_config(page_title="Study-Sync | Core Terminal", page_icon="🔄", layout="wide")

# ==========================================
#  ENTERPRISE TECH HIGH-RESPONSIVE STYLING
# ==========================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');
    
    /* Global Universal Font Unification */
    *, html, body, p, label, input, button, h1, h2, h3, h4, h5, h6, [data-testid="stMarkdownContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    body, p, label, input, .hud-body {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.2rem !important;
        font-weight: 400;
    }

    /* Core Canvas Deep Background Base */
    html, body, .stApp {
        background-color: #040612 !important;
        overflow-x: hidden;
    }

    /* Hardware-Accelerated Smooth Moving Cyber Grid Backdrop */
    .stApp {
        background-image: 
            linear-gradient(rgba(82, 39, 255, 0.012) 1px, transparent 1px),
            linear-gradient(90deg, rgba(82, 39, 255, 0.012) 1px, transparent 1px) !important;
        background-size: 60px 60px !important;
        background-attachment: fixed !important;
    }
    
    /* Exact React Bits Diagonal Non-Yoyo 6-Color Gradient Stream */
    .laser-title {
        background: linear-gradient(135deg, #3b82f6, #ffffff, #ff0000, #ec4899, #10b981, #06b6d4, #3b82f6) !important;
        background-size: 200% 200% !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        display: inline-block !important;
        animation: flow-gradient 2s linear infinite !important;
    }

    @keyframes flow-gradient {
        0% { background-position: 0% 0%; }
        100% { background-position: 200% 200%; }
    }
    
    /* Centering CSS Overrides for Streamlit Radio Blocks */
    div[data-testid="stRadio"] {
        text-align: center !important;
    }
    div[data-testid="stRadio"] > label {
        text-align: center !important;
        display: block !important;
        color: #b497cf !important;
        font-weight: 600 !important;
    }
    div[data-testid="stRadio"] > div {
        justify-content: center !important;
    }
    
    /* Glassmorphic Card Wrapper */
    div[data-testid="stForm"] {
        background: rgba(9, 12, 26, 0.6) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(82, 39, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 2.5rem !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5) !important;
        position: relative;
        z-index: 10;
    }

    /* Reactive Glow States on Input Focus Fields */
    div[data-testid="stTextInput"] input {
        background: rgba(16, 22, 42, 0.45) !important;
        border: 1px solid rgba(82, 39, 255, 0.15) !important;
        color: #ffffff !important;
    }
    
    /* Custom Cosmic Submit Button - Block display + Auto margins guarantees absolute centering */
    div[data-testid="stFormSubmitButton"] button {
        display: block !important;
        margin: 1.5rem auto 0 auto !important;
        background: linear-gradient(90deg, #5227ff 0%, #ff9ffc 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.6rem 3.5rem !important;
        box-shadow: 0 0 15px rgba(82, 39, 255, 0.35) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Frozen hover block preventing unexpected shifting/scaling animations */
    div[data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(90deg, #5227ff 0%, #ff9ffc 100%) !important;
        box-shadow: 0 0 15px rgba(82, 39, 255, 0.35) !important;
        color: #ffffff !important;
        transform: none !important;
    }
    
    /* Interactive Dashboard Telemetry Rows */
    div[data-testid="stCheckbox"] {
        background: rgba(16, 22, 42, 0.4) !important;
        border: 1px solid rgba(82, 39, 255, 0.15) !important;
        border-left: 4px solid #5227ff !important;
        padding: 1.2rem 1.5rem !important;
        border-radius: 6px !important;
        margin-bottom: 12px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- APP LOGIC ---
if "auth_state" not in st.session_state: st.session_state.auth_state = False
if "username" not in st.session_state: st.session_state.username = ""
if "generated" not in st.session_state: st.session_state.generated = False
if "roadmap_list" not in st.session_state: st.session_state.roadmap_list = []

def logout():
    st.session_state.auth_state = False
    st.rerun()

if not st.session_state.auth_state:
    st.markdown(
        """
        <div style="text-align: center; width: 100%; margin-bottom: 25px;">
            <h1 class="laser-title" style="font-size: 5rem; font-weight: 800; margin: 0;">Study Sync</h1>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    left_space, center_auth_col, right_space = st.columns([1, 1.6, 1], gap="medium")
    
    with center_auth_col:
        auth_mode = st.radio("Choose an option:", ["Login", "Sign Up"], horizontal=True)
        with st.form("auth_form"):
            st.text_input("Username", placeholder="Enter your username")
            st.text_input("Email Address", placeholder="Enter your email address")
            st.text_input("Password", type="password")
            if st.form_submit_button("Submit"):
                st.session_state.auth_state = True
                st.rerun()
    st.stop()

else:
    st.markdown('<h1 class="laser-title">Study Sync Dashboard</h1>', unsafe_allow_html=True)
    if st.button("Logout"): logout()