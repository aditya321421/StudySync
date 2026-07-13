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
    
    /* Continuous looping gradient text effect matching custom React Bits parameters */
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
    
    /* Glassmorphic Card Wrapper with Dynamic Proximity Glow Flare */
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

    /* Reactive Glow States on Input Focus Fields */
    div[data-testid="stTextInput"] input {
        background: rgba(16, 22, 42, 0.45) !important;
        border: 1px solid rgba(82, 39, 255, 0.15) !important;
        color: #ffffff !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div[data-testid="stTextInput"] input:hover {
        border-color: rgba(255, 159, 252, 0.25) !important;
        background: rgba(16, 22, 42, 0.55) !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #ff9ffc !important;
        box-shadow: 0 0 20px rgba(255, 159, 252, 0.2) !important;
        background: rgba(16, 22, 42, 0.65) !important;
    }
    
    /* Target the invisible outer wrapper block to force absolute centering */
    div[data-testid="element-container"]:has(div[data-testid="stFormSubmitButton"]) {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        text-align: center !important;
    }
    
    /* Center alignment stack layouts */
    div[data-testid="stFormSubmitButton"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        margin-top: 1.5rem !important;
    }
    div[data-testid="stFormSubmitButton"] > div {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    
    /* Custom Cosmic Submit Button Base Stylesheet */
    div[data-testid="stFormSubmitButton"] button {
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
    
    /* FIXED: Statically freeze the hover state to eliminate scaling and switching animations */
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
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div[data-testid="stCheckbox"]:hover {
        background: rgba(16, 22, 42, 0.7) !important;
        border-color: rgba(255, 159, 252, 0.25) !important;
        border-left-color: #ffffff !important;
        box-shadow: 0 0 20px rgba(82, 39, 255, 0.15) !important;
        transform: translateX(3px);
    }
    
    /* File/Document Module Configurations */
    div[data-testid="stFileUploader"] {
        border: 1px dashed rgba(82, 39, 255, 0.35) !important;
        background: rgba(16, 22, 42, 0.3) !important;
        border-radius: 6px;
        padding: 6px;
    }
    div[data-testid="stProgress"] > div > div > div {
        background: linear-gradient(90deg, #5227ff 0%, #ff9ffc 100%) !important;
        box-shadow: 0 0 12px rgba(82, 39, 255, 0.4);
    }
    </style>
    """,
    unsafe_allow_html=True
)

import streamlit.components.v1 as components

def render_galaxy_component(
    height=340,
    density=1.4,
    glow_intensity=0.5,
    saturation=0.8,
    hue_shift=260,
    star_speed=0.5,
    mouse_repulsion=True,
    repulsion_strength=2.5,
    twinkle_intensity=0.4,
    rotation_speed=0.08,
    transparent=True
):
    """
    Compiles and bundles the open-source React Bits WebGL Galaxy Component natively inside Streamlit.
    """
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            html, body { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: transparent; }
            #galaxy-container { width: 100%; height: 100%; position: relative; border-radius: 12px; }
        </style>
    </head>
    <body>
        <div id="galaxy-container"></div>
        <script type="module">
            import { Renderer, Program, Mesh, Color, Triangle } from 'https://cdn.jsdelivr.net/npm/ogl@0.0.116/dist/ogl.mjs';

            const vertexShader = `
            attribute vec2 uv;
            attribute vec2 position;
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = vec4(position, 0, 1);
            }
            `;

            const fragmentShader = `
            precision highp float;
            uniform float uTime;
            uniform vec3 uResolution;
            uniform vec2 uFocal;
            uniform vec2 uRotation;
            uniform float uStarSpeed;
            uniform float uDensity;
            uniform float uHueShift;
            uniform float uSpeed;
            uniform vec2 uMouse;
            uniform float uGlowIntensity;
            uniform float uSaturation;
            uniform bool uMouseRepulsion;
            uniform float uTwinkleIntensity;
            uniform float uRotationSpeed;
            uniform float uRepulsionStrength;
            uniform float uMouseActiveFactor;
            uniform float uAutoCenterRepulsion;
            uniform bool uTransparent;

            varying vec2 vUv;

            #define NUM_LAYER 4.0
            #define STAR_COLOR_CUTOFF 0.2
            #define MAT45 mat2(0.7071, -0.7071, 0.7071, 0.7071)
            #define PERIOD 3.0

            float Hash21(vec2 p) {
                p = fract(p * vec2(123.34, 456.21));
                p += dot(p, p + 45.32);
                return fract(p.x * p.y);
            }

            float tri(float x) { return abs(fract(x) * 2.0 - 1.0); }
            float tris(float x) {
                float t = fract(x);
                return 1.0 - smoothstep(0.0, 1.0, abs(2.0 * t - 1.0));
            }
            float trisn(float x) {
                float t = fract(x);
                return 2.0 * (1.0 - smoothstep(0.0, 1.0, abs(2.0 * t - 1.0))) - 1.0;
            }

            vec3 hsv2rgb(vec3 c) {
                vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
                vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
                return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
            }

            float Star(vec2 uv, float flare) {
                float d = length(uv);
                float m = (0.05 * uGlowIntensity) / d;
                float rays = smoothstep(0.0, 1.0, 1.0 - abs(uv.x * uv.y * 1000.0));
                m += rays * flare * uGlowIntensity;
                uv *= MAT45;
                rays = smoothstep(0.0, 1.0, 1.0 - abs(uv.x * uv.y * 1000.0));
                m += rays * 0.3 * flare * uGlowIntensity;
                m *= smoothstep(1.0, 0.2, d);
                return m;
            }

            vec3 StarLayer(vec2 uv) {
                vec3 col = vec3(0.0);
                vec2 gv = fract(uv) - 0.5; 
                vec2 id = floor(uv);

                for (int y = -1; y <= 1; y++) {
                    for (int x = -1; x <= 1; x++) {
                        vec2 offset = vec2(float(x), float(y));
                        vec2 si = id + vec2(float(x), float(y));
                        float seed = Hash21(si);
                        float size = fract(seed * 345.32);
                        float glossLocal = tri(uStarSpeed / (PERIOD * seed + 1.0));
                        float flareSize = smoothstep(0.9, 1.0, size) * glossLocal;

                        float red = smoothstep(STAR_COLOR_CUTOFF, 1.0, Hash21(si + 1.0)) + STAR_COLOR_CUTOFF;
                        float blu = smoothstep(STAR_COLOR_CUTOFF, 1.0, Hash21(si + 3.0)) + STAR_COLOR_CUTOFF;
                        float grn = min(red, blu) * seed;
                        vec3 base = vec3(red, grn, blu);
                        
                        float hue = atan(base.g - base.r, base.b - base.r) / (2.0 * 3.14159) + 0.5;
                        hue = fract(hue + uHueShift / 360.0);
                        float sat = length(base - vec3(dot(base, vec3(0.299, 0.587, 0.114)))) * uSaturation;
                        float val = max(max(base.r, base.g), base.b);
                        base = hsv2rgb(vec3(hue, sat, val));

                        vec2 pad = vec2(tris(seed * 34.0 + uTime * uSpeed / 10.0), tris(seed * 38.0 + uTime * uSpeed / 30.0)) - 0.5;
                        float star = Star(gv - offset - pad, flareSize);
                        vec3 color = base;

                        float twinkle = trisn(uTime * uSpeed + seed * 6.2831) * 0.5 + 1.0;
                        twinkle = mix(1.0, twinkle, uTwinkleIntensity);
                        star *= twinkle;
                        col += star * size * color;
                    }
                }
                return col;
            }

            void main() {
                vec2 focalPx = uFocal * uResolution.xy;
                vec2 uv = (vUv * uResolution.xy - focalPx) / uResolution.y;
                
                if (uMouseRepulsion) {
                    vec2 mousePosUV = (uMouse * uResolution.xy - focalPx) / uResolution.y;
                    float mouseDist = length(uv - mousePosUV);
                    vec2 repulsion = normalize(uv - mousePosUV) * (uRepulsionStrength / (mouseDist + 0.1));
                    uv += repulsion * 0.05 * uMouseActiveFactor;
                }

                float autoRotAngle = uTime * uRotationSpeed;
                mat2 autoRot = mat2(cos(autoRotAngle), -sin(autoRotAngle), sin(autoRotAngle), cos(autoRotAngle));
                uv = autoRot * uv;
                uv = mat2(uRotation.x, -uRotation.y, uRotation.y, uRotation.x) * uv;

                vec3 col = vec3(0.0);
                for (float i = 0.0; i < 1.0; i += 1.0 / NUM_LAYER) {
                    float depth = fract(i + uStarSpeed * uSpeed);
                    float scale = mix(20.0 * uDensity, 0.5 * uDensity, depth);
                    float fade = depth * smoothstep(1.0, 0.9, depth);
                    col += StarLayer(uv * scale + i * 453.32) * fade;
                }

                if (uTransparent) {
                    float alpha = length(col);
                    alpha = smoothstep(0.0, 0.3, alpha);
                    gl_FragColor = vec4(col, min(alpha, 1.0));
                } else {
                    gl_FragColor = vec4(col, 1.0);
                }
            }
            `;

            const config = {
                density: __DENSITY__,
                glowIntensity: __GLOW_INTENSITY__,
                saturation: __SATURATION__,
                hueShift: __HUE_SHIFT__,
                starSpeed: __STAR_SPEED__,
                mouseRepulsion: __MOUSE_REPULSION__,
                repulsionStrength: __REPULSION_STRENGTH__,
                twinkleIntensity: __TWINKLE_INTENSITY__,
                rotationSpeed: __ROTATION_SPEED__,
                transparent: __TRANSPARENT__
            };

            const ctn = document.getElementById('galaxy-container');
            const targetMousePos = { x: 0.5, y: 0.5 };
            const smoothMousePos = { x: 0.5, y: 0.5 };
            let targetMouseActive = 0.0;
            let smoothMouseActive = 0.0;

            const renderer = new Renderer({ alpha: config.transparent, premultipliedAlpha: false });
            const gl = renderer.gl;

            if (config.transparent) {
                gl.enable(gl.BLEND);
                gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
                gl.clearColor(0, 0, 0, 0);
            } else {
                gl.clearColor(0, 0, 0, 1);
            }

            let program;

            function resize() {
                renderer.setSize(ctn.offsetWidth, ctn.offsetHeight);
                if (program) {
                    program.uniforms.uResolution.value = new Color(gl.canvas.width, gl.canvas.height, gl.canvas.width / gl.canvas.height);
                }
            }
            window.addEventListener('resize', resize, false);

            const geometry = new Triangle(gl);
            program = new Program(gl, {
                vertex: vertexShader,
                fragment: fragmentShader,
                uniforms: {
                    uTime: { value: 0 },
                    uResolution: { value: new Color(gl.canvas.width, gl.canvas.height, gl.canvas.width / gl.canvas.height) },
                    uFocal: { value: new Float32Array([0.5, 0.5]) },
                    uRotation: { value: new Float32Array([1.0, 0.0]) },
                    uStarSpeed: { value: config.starSpeed },
                    uDensity: { value: config.density },
                    uHueShift: { value: config.hueShift },
                    uSpeed: { value: 1.0 },
                    uMouse: { value: new Float32Array([0.5, 0.5]) },
                    uGlowIntensity: { value: config.glowIntensity },
                    uSaturation: { value: config.saturation },
                    uMouseRepulsion: { value: config.mouseRepulsion },
                    uTwinkleIntensity: { value: config.twinkleIntensity },
                    uRotationSpeed: { value: config.rotationSpeed },
                    uRepulsionStrength: { value: config.repulsionStrength },
                    uMouseActiveFactor: { value: 0.0 },
                    uAutoCenterRepulsion: { value: 0.0 },
                    uTransparent: { value: config.transparent }
                }
            });

            resize();
            const mesh = new Mesh(gl, { geometry, program });
            ctn.appendChild(gl.canvas);

            function update(t) {
                requestAnimationFrame(update);
                program.uniforms.uTime.value = t * 0.001;
                program.uniforms.uStarSpeed.value = (t * 0.001 * config.starSpeed) / 10.0;

                const lerpFactor = 0.05;
                smoothMousePos.x += (targetMousePos.x - smoothMousePos.x) * lerpFactor;
                smoothMousePos.y += (targetMousePos.y - smoothMousePos.y) * lerpFactor;
                smoothMouseActive += (targetMouseActive - smoothMouseActive) * lerpFactor;

                program.uniforms.uMouse.value[0] = smoothMousePos.x;
                program.uniforms.uMouse.value[1] = smoothMousePos.y;
                program.uniforms.uMouseActiveFactor.value = smoothMouseActive;

                renderer.render({ scene: mesh });
            }
            requestAnimationFrame(update);

            ctn.addEventListener('mousemove', (e) => {
                const rect = ctn.getBoundingClientRect();
                targetMousePos.x = (e.clientX - rect.left) / rect.width;
                targetMousePos.y = 1.0 - (e.clientY - rect.top) / rect.height;
                targetMouseActive = 1.0;
            });

            ctn.addEventListener('mouseleave', () => {
                targetMouseActive = 0.0;
            });
        </script>
    </body>
    </html>
    """
    final_html = (html_code
        .replace("__DENSITY__", str(density))
        .replace("__GLOW_INTENSITY__", str(glow_intensity))
        .replace("__SATURATION__", str(saturation))
        .replace("__HUE_SHIFT__", str(hue_shift))
        .replace("__STAR_SPEED__", str(star_speed))
        .replace("__MOUSE_REPULSION__", str(mouse_repulsion).lower())
        .replace("__REPULSION_STRENGTH__", str(repulsion_strength))
        .replace("__TWINKLE_INTENSITY__", str(twinkle_intensity))
        .replace("__ROTATION_SPEED__", str(rotation_speed))
        .replace("__TRANSPARENT__", str(transparent).lower())
    )
    return components.html(final_html, height=height, scrolling=False)

# Fetch Firebase Configurations from Secrets
FIREBASE_API_KEY = st.secrets.get("FIREBASE_API_KEY")
FIREBASE_PROJECT_ID = st.secrets.get("FIREBASE_PROJECT_ID")

# Initialize persistent session states
if "auth_state" not in st.session_state: st.session_state.auth_state = False
if "user_email" not in st.session_state: st.session_state.user_email = ""
if "username" not in st.session_state: st.session_state.username = ""
if "user_uid" not in st.session_state: st.session_state.user_uid = ""
if "id_token" not in st.session_state: st.session_state.id_token = ""
if "generated" not in st.session_state: st.session_state.generated = False
if "roadmap_list" not in st.session_state: st.session_state.roadmap_list = []

# --- FIREBASE AUTHENTICATION FUNCTIONS ---
def firebase_auth(email, password, mode="signInWithPassword"):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:{mode}?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        response = requests.post(url, json=payload)
        res_data = response.json()
        if response.status_code == 200:
            return {
                "success": True, 
                "email": res_data["email"], 
                "uid": res_data["localId"],
                "idToken": res_data["idToken"]
            }
        else:
            return {"success": False, "message": res_data.get("error", {}).get("message", "Authentication Failed")}
    except Exception as e:
        return {"success": False, "message": str(e)}

def get_email_from_username(username):
    if not FIREBASE_PROJECT_ID: return None
    url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/users/{username}"
    try:
        res = requests.get(url)
        if res.status_code == 200 and res.json():
            return res.json().get("fields", {}).get("email", {}).get("stringValue", None)
    except Exception: return None
    return None

def get_username_from_email(email):
    if not FIREBASE_PROJECT_ID: return None
    url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents:runQuery"
    payload = {"structuredQuery": {"from": [{"collectionId": "users"}], "where": {"fieldFilter": {"field": {"fieldPath": "email"}, "op": "EQUAL", "value": {"stringValue": email}}}, "limit": 1}}
    try:
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            res_data = res.json()
            if res_data and isinstance(res_data, list) and "document" in res_data[0]:
                return res_data[0]["document"]["name"].split("/")[-1]
    except Exception: return None
    return None

def save_user_data_to_firestore(id_token, roadmap_list, username, email):
    if not FIREBASE_PROJECT_ID: return False
    url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/users/{username}"
    payload = {"fields": {"roadmap_json": {"stringValue": json.dumps(roadmap_list)}, "username": {"stringValue": username}, "email": {"stringValue": email}}}
    headers = {"Authorization": f"Bearer {id_token}"}
    try:
        res = requests.patch(url, json=payload, headers=headers)
        return res.status_code == 200
    except Exception: return False

def load_user_data_from_firestore(username, id_token):
    if not FIREBASE_PROJECT_ID: return []
    url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/users/{username}"
    headers = {"Authorization": f"Bearer {id_token}"}
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200 and res.json():
            return json.loads(res.json().get("fields", {}).get("roadmap_json", {}).get("stringValue", "[]"))
    except Exception: return []
    return []

def logout():
    st.session_state.auth_state = False
    st.session_state.user_email = ""
    st.session_state.username = ""
    st.session_state.user_uid = ""
    st.session_state.id_token = ""
    st.session_state.generated = False
    st.session_state.roadmap_list = []
    st.rerun()

# ==========================================
#  INTERFACE ROUTING: AUTHENTICATION PORTAL
# ==========================================
if not st.session_state.auth_state:
    st.write("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; width: 100%; margin-bottom: 0px; padding-bottom: 0px;">
            <h1 class="laser-title" style="font-size: 5rem; font-weight: 800; margin: 0; line-height: 1.1; letter-spacing: -2px;">
                Study Sync
            </h1>
            <h4 style="color: #b497cf; font-weight: 500; margin-top: 10px; margin-bottom: 25px;">
                Please sign in or create an account to access your daily study plans.
            </h4>
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.markdown("<hr style='margin-top:0px; margin-bottom:20px; border-color:rgba(82, 39, 255, 0.2);'>", unsafe_allow_html=True)
    
    # Balanced 3-column grid positioning layout cards dead center
    left_space, center_auth_col, right_space = st.columns([1, 1.6, 1], gap="medium")
    
    with center_auth_col:
        auth_mode = st.radio("Choose an option:", ["Login", "Sign Up"], horizontal=True)
        
        with st.form("auth_form"):
            if auth_mode == "Login":
                username_input = st.text_input("Username", placeholder="Enter your username")
                email_input = st.text_input("Email Address", placeholder="Enter your email address")
                password = st.text_input("Password", type="password")
            else:
                username_input = st.text_input("Username", placeholder="e.g., alex_codes")
                email_input = st.text_input("Email Address", placeholder="name@example.com")
                password = st.text_input("Password", type="password")
                
            submit_btn = st.form_submit_button("Submit")
            
            if submit_btn:
                if auth_mode == "Login":
                    if not username_input.strip() and not email_input.strip():
                        st.error("Please provide either your Username or Email Address to log in.")
                    elif not password:
                        st.error("Please enter your password.")
                    else:
                        resolved_email = email_input.strip()
                        if not resolved_email and username_input.strip():
                            with st.spinner("Resolving username matching profile..."):
                                resolved_email = get_email_from_username(username_input.strip())
                            if not resolved_email:
                                st.error("Username profile record not found. Please double check or use your Email Address.")
                                st.stop()
                        
                        with st.spinner("Verifying credentials with Firebase Auth..."):
                            result = firebase_auth(resolved_email, password, mode="signInWithPassword")
                        
                        if result["success"]:
                            st.session_state.auth_state = True
                            st.session_state.user_email = result["email"]
                            st.session_state.user_uid = result["uid"]
                            st.session_state.id_token = result["idToken"]
                            
                            if email_input.strip():
                                resolved_username = get_username_from_email(result["email"])
                                st.session_state.username = resolved_username if resolved_username else result["email"]
                            else:
                                st.session_state.username = username_input.strip()
                                
                            cloud_data = load_user_data_from_firestore(st.session_state.username, result["idToken"])
                            if cloud_data:
                                st.session_state.roadmap_list = cloud_data
                                st.session_state.generated = True
                                
                            st.success("Logged in successfully!")
                            st.rerun()
                        else:
                            st.error(f"Error: {result['message']}")
                else:
                    if not username_input.strip() or not email_input.strip() or not password:
                        st.error("Please fill out all registration fields.")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters long.")
                    else:
                        with st.spinner("Creating profile account with Firebase Auth..."):
                            result = firebase_auth(email_input.strip(), password, mode="signUp")
                        
                        if result["success"]:
                            st.session_state.auth_state = True
                            st.session_state.user_email = result["email"]
                            st.session_state.user_uid = result["uid"]
                            st.session_state.id_token = result["idToken"]
                            st.session_state.username = username_input.strip()
                            save_user_data_to_firestore(st.session_state.id_token, [], username_input.strip(), result["email"])
                            st.success("Account created successfully!")
                            st.rerun()
                        else:
                            st.error(f"Error: {result['message']}")

    # Render interactive React Bits WebGL engine layer directly framing elements
    st.write("<br>", unsafe_allow_html=True)
    render_galaxy_component()
    st.stop()

# ==========================================
#  INTERFACE ROUTING: CORE APPLICATION
# ==========================================
st.markdown("<h1 class='laser-title' style='font-family: \"Plus Jakarta Sans\", sans-serif; font-size: 5rem; margin-bottom: 0px; padding-bottom: 10px; line-height: 1.2; letter-spacing: -2px;'>Study Sync</h1>", unsafe_allow_html=True)

header_col1, header_col2 = st.columns([5, 1], gap="small")
with header_col1:
    st.markdown(f"#### *Profile Name - ({st.session_state.username})*")
with header_col2:
    st.write("<br><br>", unsafe_allow_html=True)
    if st.button("🚪 Log Out", use_container_width=True):
        logout()

st.markdown("---")

st.markdown("### ⚡ Configuration Panel")
config_col1, config_col2, config_col3 = st.columns([2, 1, 1], gap="medium")

with config_col1:
    uploaded_file = st.file_uploader("Upload Course Syllabus/PDF", type=["pdf"])
with config_col2:
    start_time = st.time_input("Preferred Daily Start Time")
with config_col3:
    end_time = st.time_input("Preferred Daily End Time")

generate_btn = st.button("Generate Complete Roadmap", type="primary", use_container_width=True)
st.markdown("---")

def convert_to_csv(data_list):
    df = pd.DataFrame(data_list)
    return df.to_csv(index=False).encode('utf-8')

if generate_btn:
    if not uploaded_file:
        st.error("Please upload a course document first!")
    else:
        with st.spinner("Analyzing syllabus and crafting an extended 45-50 day roadmap..."):
            try:
                reader = pypdf.PdfReader(uploaded_file)
                pdf_text = ""
                for page in reader.pages[:10]: 
                    pdf_text += page.extract_text() or ""
                
                start_str = start_time.strftime("%I:%M %p")
                end_str = end_time.strftime("%I:%M %p")
                
                prompt = f"""
                Analyze this syllabus text:
                {pdf_text[:7000]}
                Create a highly extensive daily study roadmap from {start_str} to {end_str}.
                """
                
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are a precise computer program that outputs raw JSON objects without code blocks."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.2,
                    max_tokens=2500  
                )
                
                raw_json = json.loads(response.choices[0].message.content)
                roadmap_data = raw_json.get("roadmap", [])
                for item in roadmap_data: item["Status"] = False
                st.session_state.roadmap_list = roadmap_data
                st.session_state.generated = True
                save_user_data_to_firestore(st.session_state.id_token, roadmap_data, st.session_state.username, st.session_state.user_email)
            except Exception as e:
                st.error(f"App compilation process encountered an evaluation exception: {e}")

if st.session_state.generated:
    st.markdown("### 🔄 Interactive Study Roadmap")
    roadmap = st.session_state.roadmap_list
    if roadmap:
        completed_count = 0
        save_col, csv_col = st.columns(2)
        with save_col:
            if st.button("Save It", type="primary", use_container_width=True):
                save_user_data_to_firestore(st.session_state.id_token, st.session_state.roadmap_list, st.session_state.username, st.session_state.user_email)
                st.toast("Progress saved successfully!", icon="🔥")
        with csv_col:
            csv_bytes = convert_to_csv(st.session_state.roadmap_list)
            st.download_button("📊 Download Roadmap Spreadsheet (.csv)", data=csv_bytes, file_name="study_roadmap.csv", mime="text/csv", use_container_width=True)
            
        st.markdown("---")
        for i, item in enumerate(roadmap):
            label_markdown = f"⚡ **{item.get('Scheduled Date')}** &nbsp;|&nbsp; ⏱️ `{item.get('Time Slot')}` &nbsp;|&nbsp; 🪐 **{item.get('Focus Topic')}**  \n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📡 *Modules Matrix: {item.get('Suggested Activity')}*"
            is_checked = st.checkbox(label_markdown, value=item.get('Status', False), key=f"task_{i}")
            if is_checked: completed_count += 1
            st.session_state.roadmap_list[i]["Status"] = is_checked
            st.markdown("---")
        
        total_tasks = len(roadmap)
        progress_percent = int((completed_count / total_tasks) * 100) if total_tasks > 0 else 0
        st.markdown(f"**Progress Check:** {completed_count}/{total_tasks} Milestones Completed ({progress_percent}%)")
        st.progress(progress_percent / 100.0)
else:
    st.info("Configuration parameters pending: Feed a course document file into the parameters block above to populate your interactive dashboard.")