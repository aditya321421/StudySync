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
        background-color: #1a1d24 !important;
        overflow-x: hidden;
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
    
    /* Glassmorphic Form Authentication Card Wrapper */
    div[data-testid="stForm"] {
        background: rgba(28, 31, 38, 0.8) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 2.5rem !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4) !important;
    }

    /* Layout Card Block Profiles Matching Screenshot */
    .workspace-card {
        background: #22262f !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 1.8rem !important;
        margin-bottom: 20px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25) !important;
    }
    
    .workspace-card h3 {
        color: #ffffff !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin-top: 0px !important;
        margin-bottom: 1.2rem !important;
    }

    /* Reactive Inputs Styling optimization */
    div[data-testid="stTextInput"] input {
        background: #1c1f26 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
    }

    /* Exact Profile Tab Box Element Top Right */
    .profile-badge-container {
        display: flex;
        align-items: center;
        background: #2d323f;
        padding: 6px 14px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        float: right;
    }
    .profile-avatar-circle {
        width: 28px;
        height: 28px;
        background: #0091ff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ffffff;
        font-size: 0.85rem;
        font-weight: 700;
        margin-right: 8px;
    }
    .profile-caret {
        color: #8a92a6;
        font-size: 0.75rem;
        margin-left: 6px;
    }
    
    /* ==========================================
       EXACT COLOR EXTRACTIONS & HOVER EFFECTS
       ========================================== */
    div.stButton > button[kind="primary"], 
    div[data-testid="stFormSubmitButton"] button {
        display: block !important;
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
        width: 100% !important;
    }
    
    div.stButton > button[kind="primary"]:hover, 
    div[data-testid="stFormSubmitButton"] button:hover {
        background: #00a2ff !important;
        box-shadow: 0 6px 30px rgba(0, 162, 255, 0.85) !important;
        transform: translateY(-2px) !important;
        color: #ffffff !important;
    }
    
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
    }
    
    /* Interactive Dashboard Checkbox Telemetry Rows */
    div[data-testid="stCheckbox"] {
        background: #1c1f26 !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-left: 4px solid #0091ff !important;
        padding: 1.2rem 1.5rem !important;
        border-radius: 6px !important;
        margin-bottom: 12px !important;
    }
    
    /* Progress Bars custom color mapping matching user analytics nodes */
    div[data-testid="stProgress"] > div > div > div {
        background: linear-gradient(90deg, #0091ff 0%, #00a2ff 100%) !important;
        box-shadow: 0 0 12px rgba(0, 145, 255, 0.4);
    }
    
    /* File Uploader styling optimization matching the empty container canvas card look */
    div[data-testid="stFileUploader"] {
        border: 1px dashed rgba(255, 255, 255, 0.12) !important;
        background: #1c1f26 !important;
        border-radius: 8px !important;
    }
    
    /* Custom Sidebar adjustments matching modern design matrix profiles */
    [data-testid="stSidebar"] {
        background-color: #14161d !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
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
        res = requests.get(url, headers=headers)
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
#  VERTICAL NAVIGATION SIDEBAR MATRIX
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color:#ffffff; margin-bottom:20px; font-weight:800;'>🔄 Study Sync</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Render operational navigation router selectors tracking dashboard views
    nav_selection = st.radio(
        "Navigation",
        options=["🏠 Workspace Home", "📅 Calendar Schedule Matrix", "🛠️ Admin Operations"],
        label_visibility="collapsed"
    )
    
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    if st.button("🚪 Log Out", use_container_width=True, type="secondary"):
        logout()

# ==========================================
#  TOP PROFILE CAP badge INFRASTRUCTURE
# ==========================================
top_spacer_col, top_profile_col = st.columns([5, 1])
with top_profile_col:
    # Extracted user profile tab matrix element layout matching top-right box
    initial_letter = st.session_state.username[0].upper() if st.session_state.username else "U"
    st.markdown(
        f"""
        <div class="profile-badge-container">
            <div class="profile-avatar-circle">{initial_letter}</div>
            <span style="color:#ffffff; font-weight:600; font-size:0.95rem;">{st.session_state.username}</span>
            <span class="profile-caret">▼</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# GIANT GREETING ROW MATCHING SCREENSHOT
st.markdown(f"<h1 style='color:#ffffff; font-size:2.8rem; font-weight:800; margin-top:-10px; margin-bottom:25px;'>Welcome Back, {st.session_state.username}!</h1>", unsafe_allow_html=True)

# ------------------------------------------
# VIEW ROUTER: CALENDAR SCHEDULE MATRIX
# ------------------------------------------
if nav_selection == "📅 Calendar Schedule Matrix":
    st.markdown("### 📅 Study Schedule Calendar Matrix")
    if st.session_state.generated and st.session_state.roadmap_list:
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
        st.info("Calendar matrix initialization pending: Upload a course document syllabus inside the Workspace Home layout to populate your active schedule.")

# ------------------------------------------
# VIEW ROUTER: ADMINISTRATIVE MODULE
# ------------------------------------------
elif nav_selection == "🛠️ Admin Operations":
    if st.session_state.is_admin:
        st.markdown("### 🛠️ Administrative Operations Dashboard")
        all_registered_users = get_all_users_from_firestore()
        if all_registered_users:
            st.dataframe(pd.DataFrame(all_registered_users), use_container_width=True)
            selected_target_profile = st.selectbox("Analyze Roadmap Records:", options=[user["Username Profile"] for user in all_registered_users])
            if st.button("Load Target Roadmap", type="primary"):
                deep_roadmap = load_user_data_from_firestore(selected_target_profile, st.session_state.id_token)
                if deep_roadmap:
                    st.dataframe(pd.DataFrame(deep_roadmap), use_container_width=True)
                else:
                    st.info("No records found inside this document node.")
        else:
            st.info("No active databases collections.")
    else:
        st.error("Access Denied: Administrative node clearance required.")

# ------------------------------------------
# VIEW ROUTER: MAIN WORKSPACE HOME
# ------------------------------------------
else:
    # TWO COLUMN BALANCED PANELS ARCHITECTURE MATCHING PHOTOGRAPH LAYOUT
    panel_left, panel_right = st.columns([1.1, 1], gap="large")
    
    with panel_left:
        # Card Wrapper 1: Create Your Roadmap Container
        st.markdown('<div class="workspace-card"><h3>Create Your Roadmap</h3>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Course Syllabus/PDF", type=["pdf"], label_visibility="collapsed")
        
        time_col1, time_col2 = st.columns(2)
        with time_col1:
            start_time = st.time_input("Daily Start Time")
        with time_col2:
            end_time = st.time_input("End Time")
            
        generate_btn = st.button("Generate Roadmap", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if generate_btn:
            if not uploaded_file:
                st.error("Please upload a course document first!")
            else:
                with st.spinner("Analyzing syllabus text data nodes..."):
                    try:
                        reader = pypdf.PdfReader(uploaded_file)
                        pdf_text = "".join([page.extract_text() or "" for page in reader.pages[:10]])
                        start_str = start_time.strftime("%I:%M %p")
                        end_str = end_time.strftime("%I:%M %p")
                        
                        prompt = f"Create daily roadmap from {start_str} to {end_str} for syllabus text: {pdf_text[:5000]}"
                        response = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[
                                {"role": "system", "content": "Return raw JSON object containing top-level key array named 'roadmap'. Inner objects contain fields: 'Scheduled Date', 'Time Slot', 'Focus Topic', 'Suggested Activity'."},
                                {"role": "user", "content": prompt}
                            ],
                            response_format={"type": "json_object"},
                            temperature=0.2
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
                        st.error(f"App compilation exception: {e}")

    with panel_right:
        # Card Wrapper 2: My Current Roadmaps Progress Tracker
        st.markdown('<div class="workspace-card"><h3>My Current Roadmaps</h3>', unsafe_allow_html=True)
        
        if st.session_state.generated and st.session_state.roadmap_list:
            completed = sum(1 for item in st.session_state.roadmap_list if item.get("Status"))
            total = len(st.session_state.roadmap_list)
            percent = int((completed / total) * 100) if total > 0 else 0
            
            # Formatted list metrics block matching target text tracking specs
            st.markdown(f"**Core Active Pipeline** Matrix &nbsp;|&nbsp; `{percent}% Complete`")
            st.progress(percent / 100.0)
            st.markdown(f"<span style='color:#a0aec0; font-size:0.9rem;'>Topic Summary: Discovered study sequences tracking {total} micro goals.</span>", unsafe_allow_html=True)
        else:
            # Fallback placeholder indicators
            st.markdown("**No Active Roadmaps Loaded**")
            st.progress(0.0)
            st.markdown("<span style='color:#a0aec0; font-size:0.9rem;'>Topic Summary: Feed a syllabus inside the creator panel to start your tracking timeline matrix.</span>", unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    #  INTERACTIVE SPREADSHEET MICRO-CHECKLIST TABLE
    # ==========================================
    if st.session_state.generated and st.session_state.roadmap_list:
        st.markdown("### 🔄 Interactive Study Roadmap Milestones Checklist")
        
        save_action, download_action = st.columns(2)
        with save_action:
            if st.button("Save Progress Nodes", use_container_width=True, type="primary"):
                if not st.session_state.is_admin:
                    save_user_data_to_firestore(st.session_state.id_token, st.session_state.roadmap_list, st.session_state.username, st.session_state.user_email)
                st.toast("Progress coordinates saved to Firestore document cluster!", icon="🔥")
        with download_action:
            csv_bytes = convert_to_csv(st.session_state.roadmap_list)
            st.download_button("Export Tracking Sheet (.CSV)", data=csv_bytes, file_name="study_roadmap.csv", mime="text/csv", use_container_width=True)
            
        st.markdown("---")
        for i, item in enumerate(st.session_state.roadmap_list):
            label_markdown = f"⚡ **{item.get('Scheduled Date')}** &nbsp;|&nbsp; ⏱️ `{item.get('Time Slot')}` &nbsp;|&nbsp; 🪐 **{item.get('Focus Topic')}**  \n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📡 *Modules Matrix: {item.get('Suggested Activity')}*"
            is_checked = st.checkbox(label_markdown, value=item.get('Status', False), key=f"task_home_{i}")
            st.session_state.roadmap_list[i]["Status"] = is_checked