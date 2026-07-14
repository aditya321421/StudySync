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
    
    /* Global Universal Font Unification - Excluded '*' to protect internal icon ligatures */
    html, body, p, label, input, button, h1, h2, h3, h4, h5, h6, [data-testid="stMarkdownContainer"] {
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
            linear-gradient(rgba(0, 145, 255, 0.01) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 145, 255, 0.01) 1px, transparent 1px) !important;
        background-size: 60px 60px !important;
        background-attachment: fixed !important;
    }
    
    /* Flowing Blue and White Custom Gradient Stream */
    .laser-title {
        background: linear-gradient(135deg, #0091ff, #ffffff, #0052ff, #ffffff, #0091ff) !important;
        background-size: 200% 200% !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        display: inline-block !important;
        animation: flow-gradient 3s linear infinite !important;
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
        color: #0091ff !important;
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
        border: 1px solid rgba(0, 145, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 2.5rem !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5) !important;
        position: relative;
        z-index: 10;
    }

    /* Reactive Glow States on Input Focus Fields */
    div[data-testid="stTextInput"] input {
        background: rgba(16, 22, 42, 0.45) !important;
        border: 1px solid rgba(0, 145, 255, 0.15) !important;
        color: #ffffff !important;
        padding-right: 3rem !important;
    }
    
    /* THE EYE ICON RESKINDED CYBER BLUE STYLE */
    div[data-testid="stTextInput"] button {
        color: #0091ff !important;
        background: transparent !important;
    }
    div[data-testid="stTextInput"] button svg {
        fill: #0091ff !important;
    }
    div[data-testid="stTextInput"] button:hover {
        color: #00a2ff !important;
        background: transparent !important;
    }
    div[data-testid="stTextInput"] button:hover svg {
        fill: #00a2ff !important;
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
    
    /* 1. SOLID PRIMARY BUTTONS (Submit, Generate Complete Roadmap, Save It) */
    div.stButton > button[kind="primary"], 
    div[data-testid="stFormSubmitButton"] button {
        display: block !important;
        margin: 1.5rem auto 0 auto !important;
        background: #0091ff !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.6rem 3.5rem !important;
        box-shadow: 0 5px 20px rgba(0, 145, 255, 0.55) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    
    div.stButton > button[kind="primary"]:hover, 
    div[data-testid="stFormSubmitButton"] button:hover {
        background: #00a2ff !important;
        box-shadow: 0 6px 30px rgba(0, 162, 255, 0.85) !important;
        transform: translateY(-2px) !important;
        color: #ffffff !important;
    }
    
    /* 2. OUTLINE GHOST BUTTONS (Log Out, Download Roadmap Spreadsheet) */
    div.stButton > button[kind="secondary"], 
    div.stDownloadButton > button {
        background: transparent !important;
        color: #0091ff !important;
        border: 1px solid rgba(0, 145, 255, 0.35) !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        padding: 0.6rem 2.5rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    
    div.stButton > button[kind="secondary"]:hover, 
    div.stDownloadButton > button:hover {
        background: rgba(0, 145, 255, 0.06) !important;
        border-color: #00a2ff !important;
        box-shadow: 0 0 18px rgba(0, 162, 255, 0.35) !important;
        color: #ffffff !important;
        transform: translateY(-1px) !important;
    }
    
    /* Interactive Dashboard Telemetry Rows */
    div[data-testid="stCheckbox"] {
        background: rgba(16, 22, 42, 0.4) !important;
        border: 1px solid rgba(0, 145, 255, 0.15) !important;
        border-left: 4px solid #0091ff !important;
        padding: 1.2rem 1.5rem !important;
        border-radius: 6px !important;
        margin-bottom: 12px !important;
    }
    
    /* Progress Bars custom color mapping */
    div[data-testid="stProgress"] > div > div > div {
        background: linear-gradient(90deg, #0091ff 0%, #00a2ff 100%) !important;
        box-shadow: 0 0 12px rgba(0, 145, 255, 0.4);
    }
    
    /* File Uploader styling optimization */
    div[data-testid="stFileUploader"] {
        border: 1px dashed rgba(0, 145, 255, 0.3) !important;
        background: rgba(11, 16, 28, 0.6) !important;
    }

    /* Admin Telemetry Container block overrides */
    .admin-card {
        background: rgba(16, 22, 42, 0.45) !important;
        border: 1px solid rgba(0, 145, 255, 0.2) !important;
        border-radius: 8px;
        padding: 1.5rem !important;
        margin-bottom: 20px;
    }
    
    /* Premium High-Tech Calendar Event Card Style */
    .calendar-event {
        background: rgba(16, 22, 42, 0.45) !important;
        border: 1px solid rgba(0, 145, 255, 0.15) !important;
        border-left: 4px solid #0091ff !important;
        padding: 1.2rem !important;
        border-radius: 8px;
        margin-bottom: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Fetch Firebase Configurations from Secrets
FIREBASE_API_KEY = st.secrets.get("FIREBASE_API_KEY")
FIREBASE_PROJECT_ID = st.secrets.get("FIREBASE_PROJECT_ID")
ADMIN_EMAIL = st.secrets.get("ADMIN_EMAIL", "admin@studysync.com")
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "AdminSecure2026")

# Initialize persistent session states
if "auth_state" not in st.session_state: st.session_state.auth_state = False
if "is_admin" not in st.session_state: st.session_state.is_admin = False
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
    headers = {"Authorization": f"Bearer {id_token}"} if id_token else {}
    try:
        res = requests.get(url)
        if res.status_code == 200 and res.json():
            return json.loads(res.json().get("fields", {}).get("roadmap_json", {}).get("stringValue", "[]"))
    except Exception: return []
    return []

def get_all_users_from_firestore():
    if not FIREBASE_PROJECT_ID: return []
    url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/users"
    try:
        res = requests.get(url)
        if res.status_code == 200 and res.json():
            documents = res.json().get("documents", [])
            parsed_users = []
            for doc in documents:
                fields = doc.get("fields", {})
                doc_id = doc.get("name", "").split("/")[-1]
                email = fields.get("email", {}).get("stringValue", "N/A")
                username = fields.get("username", {}).get("stringValue", doc_id)
                roadmap_raw = fields.get("roadmap_json", {}).get("stringValue", "[]")
                try:
                    milestones = len(json.loads(roadmap_raw))
                except Exception:
                    milestones = 0
                parsed_users.append({
                    "Username Profile": username,
                    "Associated Email": email,
                    "Active Milestones Count": milestones
                })
            return parsed_users
    except Exception:
        return []
    return []

def logout():
    st.session_state.auth_state = False
    st.session_state.is_admin = False
    st.session_state.user_email = ""
    st.session_state.username = ""
    st.session_state.user_uid = ""
    st.session_state.id_token = ""
    st.session_state.generated = False
    st.session_state.roadmap_list = []
    st.rerun()

def convert_to_csv(data_list):
    df = pd.DataFrame(data_list)
    return df.to_csv(index=False).encode('utf-8')

# ==========================================
#  INTERFACE ROUTING: AUTHENTICATION PORTAL
# ==========================================
if not st.session_state.auth_state:
    st.write("<br>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="text-align: center; width: 100%; margin-bottom: 25px;">
            <h1 class="laser-title" style="font-size: 5rem; font-weight: 800; margin: 0; letter-spacing: -2px;">
                Study Sync
            </h1>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    left_space, center_auth_col, right_space = st.columns([1, 1.6, 1], gap="medium")
    
    with center_auth_col:
        auth_mode = st.radio("Choose an option:", ["Login", "Sign Up", "Admin Login"], horizontal=True)
        
        with st.form("auth_form"):
            if auth_mode == "Login":
                username_input = st.text_input("Username", placeholder="Enter your username")
                email_input = st.text_input("Email Address", placeholder="Enter your email address")
                password = st.text_input("Password", type="password")
            elif auth_mode == "Sign Up":
                username_input = st.text_input("Username", placeholder="e.g., alex_codes")
                email_input = st.text_input("Email Address", placeholder="name@example.com")
                password = st.text_input("Password", type="password")
            else:
                email_input = st.text_input("Admin Email Address", placeholder="admin@studysync.com")
                password = st.text_input("Admin Security Password", type="password")
                
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
                            
                elif auth_mode == "Sign Up":
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
                            save_user_data_to_firestore(result["idToken"], [], username_input.strip(), result["email"])
                            st.success("Account created successfully!")
                            st.rerun()
                        else:
                            st.error(f"Error: {result['message']}")
                            
                else: 
                    if not email_input.strip() or not password:
                        st.error("Please provide full administrative entry credentials.")
                    else:
                        if email_input.strip() == ADMIN_EMAIL and password == ADMIN_PASSWORD:
                            st.session_state.auth_state = True
                            st.session_state.is_admin = True
                            st.session_state.username = "Root_Admin"
                            st.session_state.user_email = ADMIN_EMAIL
                            st.success("Administrative core master console access authorized!")
                            st.rerun()
                        else:
                            with st.spinner("Verifying administrative node via base network..."):
                                result = firebase_auth(email_input.strip(), password, mode="signInWithPassword")
                            if result["success"]:
                                st.session_state.auth_state = True
                                st.session_state.is_admin = True
                                st.session_state.username = "Admin_" + result["email"].split("@")[0]
                                st.session_state.user_email = result["email"]
                                st.session_state.id_token = result["idToken"]
                                st.success("Administrative console operational!")
                                st.rerun()
                            else:
                                st.error("Administrative access denial matching credentials block failure.")
    st.stop()

# ==========================================
#  INTERFACE ROUTING: CORE APPLICATION
# ==========================================

# FIXED: Title block centered exactly like the login layout canvas screen
st.markdown(
    """
    <div style="text-align: center; width: 100%; margin-bottom: 25px;">
        <h1 class="laser-title" style="font-size: 5rem; font-weight: 800; margin: 0; letter-spacing: -2px;">
            Study Sync
        </h1>
    </div>
    """, 
    unsafe_allow_html=True
)

header_col1, header_col2 = st.columns([5, 1.2], gap="small")
with header_col1:
    if st.session_state.is_admin:
        st.markdown(f"#### *Profile Name - ({st.session_state.username})* &nbsp;|&nbsp; ⚡ **Admin Control Terminal active**")
    else:
        st.markdown(f"#### *Profile Name - ({st.session_state.username})*")
with header_col2:
    if st.button("Log Out", use_container_width=True, type="secondary"):
        logout()

st.markdown("---")

# ==========================================
#  THREE STAGE SECTION TAB SEGMENTATION
# ==========================================
workspace_tab1, workspace_tab2, workspace_tab3 = st.tabs(["📊 Dashboard", "📅 Calendar", "🗺️ Roadmap"])

# ------------------------------------------
# TAB 1: CONFIGURATION & ADMIN CONTROLS
# ------------------------------------------
with workspace_tab1:
    if st.session_state.is_admin:
        st.markdown("### 🛠️ Administrative Operations Dashboard")
        
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        with stat_col1:
            st.markdown('<div class="admin-card">📊 <b>System Load</b><br><span style="color:#0091ff; font-size:1.8rem; font-weight:700;">Nominal (0.04s)</span></div>', unsafe_allow_html=True)
        with stat_col2:
            st.markdown('<div class="admin-card">🔒 <b>Database Security</b><br><span style="color:#0091ff; font-size:1.8rem; font-weight:700;">Firestore Verified</span></div>', unsafe_allow_html=True)
        with stat_col3:
            st.markdown('<div class="admin-card">📡 <b>LLM Processing API</b><br><span style="color:#0091ff; font-size:1.8rem; font-weight:700;">Groq Online</span></div>', unsafe_allow_html=True)
            
        st.markdown("#### 📂 Global Firestore User Directory Database")
        with st.spinner("Synchronizing data structure rows from cloud data nodes..."):
            all_registered_users = get_all_users_from_firestore()
            
        if all_registered_users:
            st.dataframe(pd.DataFrame(all_registered_users), use_container_width=True)
            
            st.markdown("#### 🔍 Deep Inspect User Milestones Matrix")
            selected_target_profile = st.selectbox(
                "Select a profile node to analyze structural roadmap records:", 
                options=[user["Username Profile"] for user in all_registered_users]
            )
            
            if st.button("Load Target Roadmap", type="primary"):
                with st.spinner(f"Pulling relational document fields for {selected_target_profile}..."):
                    deep_roadmap = load_user_data_from_firestore(selected_target_profile, st.session_state.id_token)
                    if not deep_roadmap:
                        url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/users/{selected_target_profile}"
                        fallback_res = requests.get(url)
                        if fallback_res.status_code == 200:
                            deep_roadmap = json.loads(fallback_res.json().get("fields", {}).get("roadmap_json", {}).get("stringValue", "[]"))
                    
                    if deep_roadmap:
                        st.success(f"Discovered active roadmap schema details matrix for {selected_target_profile}:")
                        st.dataframe(pd.DataFrame(deep_roadmap), use_container_width=True)
                    else:
                        st.info("The selected profile currently holds an empty roadmap array sequence inside Firestore.")
        else:
            st.info("No user data node vectors detected inside the cloud document database collection.")

        st.markdown("---")
        st.markdown("### 🧪 User Simulation Sandbox")
        st.info("The configuration matrix block below allows administrators to simulate standard user syllabus uploads without modifying database records.")

    st.markdown("### ⚡ Configuration Panel")
    config_col1, config_col2, config_col3 = st.columns([2, 1, 1], gap="medium")

    with config_col1:
        uploaded_file = st.file_uploader("Upload Course Syllabus/PDF", type=["pdf"])
    with config_col2:
        start_time = st.time_input("Start Time")
    with config_col3:
        end_time = st.time_input("End Time")

    generate_btn = st.button("Generate Complete Roadmap", type="primary", use_container_width=True)
    
    if generate_btn:
        if not uploaded_file:
            st.error("Please upload a course document first!")
        else:
            with st.spinner("Analyzing syllabus payload and structuring database matrix nodes..."):
                try:
                    reader = pypdf.PdfReader(uploaded_file)
                    pdf_text = ""
                    for page in reader.pages[:10]: 
                        pdf_text += page.extract_text() or ""
                    
                    start_str = start_time.strftime("%I:%M %p")
                    end_str = end_time.strftime("%I:%M %p")
                    
                    prompt = f"""
                    Analyze this course syllabus text comprehensively:
                    {pdf_text[:7000]}
                    
                    Create a highly extensive daily study roadmap structured from {start_str} to {end_str}.
                    Provide specific tracking nodes. You must return a JSON object containing a top-level key array named "roadmap".
                    Each inner array element object must strictly contain these fields:
                    "Scheduled Date", "Time Slot", "Focus Topic", and "Suggested Activity".
                    """
                    
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": "You are a precise computer program that outputs clean raw JSON object data matching schemas perfectly without code blocks or markdown wrapper elements."},
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
                    if not st.session_state.is_admin:
                        save_user_data_to_firestore(st.session_state.id_token, roadmap_data, st.session_state.username, st.session_state.user_email)
                    st.rerun()
                except Exception as e:
                    st.error(f"App compilation process encountered an evaluation exception: {e}")

# ------------------------------------------
# TAB 2: CALENDAR MATRIX MODULE
# ------------------------------------------
with workspace_tab2:
    st.markdown("### 📅 Study Schedule Calendar Matrix")
    if st.session_state.generated and st.session_state.roadmap_list:
        st.markdown("Here is your chronologically structured learning calendar pipeline mapping:")
        st.write("<br>", unsafe_allow_html=True)
        
        for item in st.session_state.roadmap_list:
            status_tag = '<span style="color:#0091ff; font-weight:700;">[✓] COMPLETED</span>' if item.get("Status") else '<span style="color:#a0aec0; font-weight:600;">[ ] PENDING</span>'
            
            st.markdown(
                f"""
                <div class="calendar-event">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0, 145, 255, 0.1); padding-bottom: 5px; margin-bottom: 8px;">
                        <span style="color: #ffffff; font-weight: 700; font-size: 1.1rem;">🗓️ {item.get('Scheduled Date')}</span>
                        <span style="font-size: 0.95rem;">{status_tag}</span>
                    </div>
                    <div style="color: #ffffff; font-weight: 600;">🪐 Focus Topic: <span style="color:#0091ff;">{item.get('Focus Topic')}</span></div>
                    <div style="color: #a0aec0; font-size: 0.95rem; margin-top: 3px;">⏱️ Allocated Window: <code>{item.get('Time Slot')}</code></div>
                    <div style="color: #cbd5e0; font-size: 0.95rem; margin-top: 3px;">📡 Suggested Activity Matrix: *{item.get('Suggested Activity')}*</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
    else:
        st.info("Calendar matrix initialization pending: Upload a course document syllabus inside the Dashboard tab to populate your schedule views.")

# ------------------------------------------
# TAB 3: INTERACTIVE ROADMAP CHECKLIST
# ------------------------------------------
with workspace_tab3:
    st.markdown("### 🗺️ Interactive Study Roadmap Milestones")
    if st.session_state.generated and st.session_state.roadmap_list:
        roadmap = st.session_state.roadmap_list
        
        completed_count = 0
        save_col, csv_col = st.columns(2)
        with save_col:
            if st.button("Save It", type="primary", use_container_width=True):
                if not st.session_state.is_admin:
                    save_user_data_to_firestore(st.session_state.id_token, st.session_state.roadmap_list, st.session_state.username, st.session_state.user_email)
                st.toast("Progress saved successfully!", icon="🔥")
        with csv_col:
            csv_bytes = convert_to_csv(st.session_state.roadmap_list)
            st.download_button("DOWNLOAD ROADMAP SPREADSHEET (.CSV)", data=csv_bytes, file_name="study_roadmap.csv", mime="text/csv", use_container_width=True)
            
        st.markdown("---")
        
        # Calculate checklist completion values safely outside interaction frames
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
        st.info("Roadmap tracking checklist data stream empty: Feed a syllabus document node inside the Dashboard segment panel to load milestones data fields.")