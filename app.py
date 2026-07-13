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
    
    .laser-title {
        background: linear-gradient(90deg, #5227ff 0%, #ff9ffc 50%, #b497cf 100%) !important;
        background-size: 200% 100% !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        display: inline-block !important;
        animation: continuousWave 4s ease-in-out infinite !important;
    }

    @keyframes continuousWave {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
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
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div[data-testid="stForm"]:hover {
        border-color: rgba(255, 159, 252, 0.3) !important;
        box-shadow: 0 0 40px rgba(82, 39, 255, 0.15), 0 20px 50px rgba(0, 0, 0, 0.6) !important;
        transform: translateY(-2px);
    }
    </style>
    """,
    unsafe_allow_html=True
)

def render_galaxy_component(height=460, density=1.6, glow_intensity=0.6, saturation=1.0, hue_shift=260, star_speed=0.6, mouse_repulsion=True, repulsion_strength=2.5, twinkle_intensity=0.4, rotation_speed=0.08, transparent=True):
    html_code = """
    <div id="galaxy-container" style="width:100%; height:100%; position:relative; border-radius:12px;"></div>
    <script type="module">
        import { Renderer, Program, Mesh, Color, Triangle } from 'https://cdn.jsdelivr.net/npm/ogl@0.0.116/dist/ogl.mjs';
        const ctn = document.getElementById('galaxy-container');
        const renderer = new Renderer({ alpha: true, premultipliedAlpha: false });
        const gl = renderer.gl;
        gl.clearColor(0, 0, 0, 0);
        
        function resize() { renderer.setSize(ctn.offsetWidth, ctn.offsetHeight); }
        window.addEventListener('resize', resize);
        resize();
        
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
if "roadmap_list" not in st.session_state: st.session_state.roadmap_list = []
if "generated" not in st.session_state: st.session_state.generated = False

def logout():
    st.session_state.auth_state = False
    st.rerun()

if not st.session_state.auth_state:
    p1, p2 = st.columns([1.1, 1], gap="large")
    with p1:
        st.markdown('<h1 class="laser-title" style="font-size: 5rem; font-weight: 800;">Study Sync</h1>', unsafe_allow_html=True)
        render_galaxy_component()
    with p2:
        with st.form("auth"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Submit"):
                st.session_state.auth_state = True
                st.rerun()
else:
    st.markdown('<h1 class="laser-title">Study Sync Dashboard</h1>', unsafe_allow_html=True)
    if st.button("Logout"): logout()