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
    
    *, html, body, p, label, input, button, h1, h2, h3, h4, h5, h6, [data-testid="stMarkdownContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    body, p, label, input, .hud-body {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.2rem !important;
        font-weight: 400;
    }

    html, body, .stApp {
        background-color: #040612 !important;
        overflow-x: hidden;
    }

    .stApp {
        background-image: 
            linear-gradient(rgba(82, 39, 255, 0.012) 1px, transparent 1px),
            linear-gradient(90deg, rgba(82, 39, 255, 0.012) 1px, transparent 1px) !important;
        background-size: 60px 60px !important;
        background-attachment: fixed !important;
    }
    
    /* Flowing Gradient Animation */
    .laser-title {
        background: linear-gradient(90deg, #5227ff, #ff9ffc, #b497cf, #5227ff) !important;
        background-size: 300% 100% !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        display: inline-block !important;
        animation: flow-gradient 6s linear infinite !important;
    }

    @keyframes flow-gradient {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
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
    
    /* Centered Submit Button Styling */
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
    
    /* Static Hover (No Animation/Shift) */
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

import streamlit.components.v1 as components

def render_galaxy_component(height=340):
    html_code = """
    <div id="galaxy-container" style="width:100%; height:100%; position:relative; border-radius:12px;"></div>
    <script type="module">
        import { Renderer, Program, Mesh, Color, Triangle } from 'https://cdn.jsdelivr.net/npm/ogl@0.0.116/dist/ogl.mjs';
        const ctn = document.getElementById('galaxy-container');
        const renderer = new Renderer({ alpha: true, premultipliedAlpha: false });
        const gl = renderer.gl;
        gl.clearColor(0, 0, 0, 0);
        function resize() { renderer.setSize(ctn.offsetWidth, ctn.offsetHeight); }
        window.addEventListener('resize', resize); resize();
        const geometry = new Triangle(gl);
        const program = new Program(gl, {
            vertex: `attribute vec2 uv; attribute vec2 position; varying vec2 vUv; void main() { vUv = uv; gl_Position = vec4(position, 0, 1); }`,
            fragment: `precision highp float; uniform float uTime; void main() { gl_FragColor = vec4(0.5, 0.2, 1.0, 0.5); }`
        });
        const mesh = new Mesh(gl, { geometry, program });
        function update(t) { requestAnimationFrame(update); renderer.render({ scene: mesh }); }
        requestAnimationFrame(update);
        ctn.appendChild(gl.canvas);
    </script>
    """
    return components.html(html_code, height=height)

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
    st.write("<br>", unsafe_allow_html=True)
    render_galaxy_component()
    st.stop()

else:
    st.markdown('<h1 class="laser-title">Study Sync Dashboard</h1>', unsafe_allow_html=True)
    if st.button("Logout"): logout()