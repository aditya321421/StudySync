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
#  MODERN TECH PURE CSS ANIMATED BACKGROUND
# ==========================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');
    
    /* Global Universal Font Unification */
    *, html, body, p, label, input, button, h1, h2, h3, h4, h5, h6, [data-testid="stMarkdownContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* Premium Corporate UI Body Stack */
    body, p, label, input, .hud-body {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.2rem !important;
        font-weight: 400;
    }
    
    /* Full Viewport Ambient Cosmic Mesh Background Engine */
    .stApp {
        background-color: #060913 !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(0, 242, 254, 0.07) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(127, 0, 255, 0.08) 0px, transparent 50%),
            linear-gradient(rgba(255, 255, 255, 0.005) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.005) 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px !important;
        animation: ambientShift 20s ease-in-out infinite alternate !important;
    }

    /* Elegant CSS Cosmic Drift Animation */
    @keyframes ambientShift {
        0% { background-position: 0% 0%, 0% 0%, 0% 0%, 0% 0%; }
        100% { background-position: 10% 5%, -10% -5%, 20px 20px, 20px 20px; }
    }
    
    /* Central Radiant Laser Gradient Text Effect */
    .laser-title {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #7f00ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        text-shadow: 0 0 35px rgba(0, 242, 254, 0.15);
    }
    
    /* Premium Glassmorphic Form Wrapper for Auth Gate */
    div[data-testid="stForm"] {
        background: rgba(11, 15, 30, 0.45) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(0, 242, 254, 0.12) !important;
        border-radius: 12px !important;
        padding: 2.5rem !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5) !important;
        transition: border-color 0.5s ease;
    }
    div[data-testid="stForm"]:hover {
        border-color: rgba(0, 242, 254, 0.3) !important;
    }
    
    /* Sleek Telemetry Checkbox Data Cards */
    div[data-testid="stCheckbox"] {
        background: rgba(16, 22, 42, 0.4) !important;
        border: 1px solid rgba(0, 242, 254, 0.15) !important;
        border-left: 4px solid #00f2fe !important;
        padding: 1.2rem 1.5rem !important;
        border-radius: 6px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div[data-testid="stCheckbox"]:hover {
        background: rgba(16, 22, 42, 0.7) !important;
        border-color: rgba(0, 242, 254, 0.4) !important;
        border-left-color: #7f00ff !important;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.2) !important;
        transform: translateX(3px);
    }
    
    /* Primary Deck Trigger Controllers (Generate & Save Buttons) */
    button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%) !important;
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 5px !important;
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.4) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    button[data-testid="stBaseButton-primary"]:hover {
        box-shadow: 0 0 30px rgba(0, 198, 255, 0.7) !important;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%) !important;
        transform: translateY(-1px);
    }
    
    /* Secondary Peripheral Controllers (Logout, Download Buttons) */
    button[data-testid="stBaseButton-secondary"] {
        background: rgba(16, 22, 42, 0.6) !important;
        color: #00f2fe !important;
        border: 1px solid rgba(0, 242, 254, 0.35) !important;
        border-radius: 5px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        transition: all 0.3s ease !important;
    }
    button[data-testid="stBaseButton-secondary"]:hover {
        background: rgba(0, 242, 254, 0.12) !important;
        border-color: #00f2fe !important;
        color: #ffffff !important;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.25) !important;
    }
    
    /* Cyber Matrix Dashed File Dropspace Box */
    div[data-testid="stFileUploader"] {
        border: 1px dashed rgba(0, 242, 254, 0.35) !important;
        background: rgba(16, 22, 42, 0.3) !important;
        border-radius: 6px;
        padding: 6px;
    }
    
    /* Radiant Glow Progress Loading Bars */
    div[data-testid="stProgress"] > div > div > div {
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%) !important;
        box-shadow: 0 0 12px rgba(0, 198, 255, 0.6);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Fetch Firebase Configurations from Secrets
FIREBASE_API_KEY = st.secrets.get("FIREBASE_API_KEY")
FIREBASE_PROJECT_ID = st.secrets.get("FIREBASE_PROJECT_ID")

# Initialize persistent session states
if "auth_state" not in st.session_state:
    st.session_state.auth_state = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_uid" not in st.session_state:
    st.session_state.user_uid = ""
if "id_token" not in st.session_state:
    st.session_state.id_token = ""
if "generated" not in st.session_state:
    st.session_state.generated = False
if "roadmap_list" not in st.session_state:
    st.session_state.roadmap_list = []

# --- FIREBASE AUTHENTICATION FUNCTIONS ---
def firebase_auth(email, password, mode="signInWithPassword"):
    """Handles Sign In/Sign Up and returns email, UID, and authorization idToken."""
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
            error_msg = res_data.get("error", {}).get("message", "Authentication Failed")
            return {"success": False, "message": error_msg}
    except Exception as e:
        return {"success": False, "message": str(e)}

# --- GOOGLE CLOUD FIRESTORE REST API INTERACTIONS (USERNAME-CENTRIC) ---
def get_email_from_username(username):
    """Directly fetches the email address field from the username document."""
    if not FIREBASE_PROJECT_ID:
        return None
    url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/users/{username}"
    try:
        res = requests.get(url)
        if res.status_code == 200 and res.json():
            return res.json().get("fields", {}).get("email", {}).get("stringValue", None)
    except Exception:
        return None
    return None

def get_username_from_email(email):
    """Queries Cloud Firestore to locate the username document associated with an email."""
    if not FIREBASE_PROJECT_ID:
        return None
    url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents:runQuery"
    payload = {
        "structuredQuery": {
            "from": [{"collectionId": "users"}],
            "where": {
                "fieldFilter": {
                    "field": {"fieldPath": "email"},
                    "op": "EQUAL",
                    "value": {"stringValue": email}
                }
            },
            "limit": 1
        }
    }
    try:
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            res_data = res.json()
            if res_data and isinstance(res_data, list) and "document" in res_data[0]:
                doc_name = res_data[0]["document"]["name"]
                return doc_name.split("/")[-1] 
    except Exception:
        return None
    return None

def save_user_data_to_firestore(id_token, roadmap_list, username, email):
    """Saves data directly into a Firestore document named after the custom Username."""
    if not FIREBASE_PROJECT_ID:
        st.error("Firebase Project ID is missing from Secrets.")
        return False
        
    url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/users/{username}"
    
    payload = {
        "fields": {
            "roadmap_json": {
                "stringValue": json.dumps(roadmap_list)
            },
            "username": {
                "stringValue": username
            },
            "email": {
                "stringValue": email
            }
        }
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    
    try:
        res = requests.patch(url, json=payload, headers=headers)
        return res.status_code == 200
    except Exception:
        return False

def load_user_data_from_firestore(username, id_token):
    """Fetches data directly from the document named after the Username."""
    if not FIREBASE_PROJECT_ID:
        return []
        
    url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/users/{username}"
    headers = {"Authorization": f"Bearer {id_token}"}
    
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200 and res.json():
            doc_data = res.json()
            roadmap_str = doc_data.get("fields", {}).get("roadmap_json", {}).get("stringValue", "[]")
            return json.loads(roadmap_str)
    except Exception:
        return []
    return []

# --- LOGOUT UTILITY ---
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
    st.markdown(
        """
        <h1 style='
            background: linear-gradient(45deg, #00c6ff, #0072ff, #7f00ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: "Plus Jakarta Sans", sans-serif;
            font-size: 5rem;
            font-weight: 800;
            margin-bottom: 0px;
            padding-bottom: 5px;
            text-shadow: 0 0 25px rgba(0, 198, 255, 0.1);
            line-height: 1.2;
            letter-spacing: -2px;
        '>
            Study Sync
        </h1>
        """, 
        unsafe_allow_html=True
    )
    st.markdown("#### *Please sign in or create an account to access your daily study plans.*")
    st.markdown("---")
    
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
                        
                        save_user_data_to_firestore(result["idToken"], [], username_input.strip(), result["email"])
                        
                        st.success("Account created successfully!")
                        st.rerun()
                    else:
                        st.error(f"Error: {result['message']}")
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
                
                CRITICAL QUANTITY MANDATE:
                You MUST generate between 45 to 50 distinct daily entries in the roadmap array. Do not compress or summarize the units.
                
                UNIT BREAKDOWN RULES:
                For every single Unit identified, you MUST generate exactly 3 consecutive daily rows to thoroughly cover the material:
                - Day 1 of Unit: Cover core definitions and foundational elements.
                - Day 2 of Unit: Cover deep technical concepts, algorithms, or inner mechanisms.
                - Day 3 of Unit: Cover practical exercises, code structures, or numerical applications.
                
                FORMAT CONSTRAINTS:
                1. 'Focus Topic' must ONLY be the Subject Name and Unit (e.g., "Fundamentals of Computers - Unit I"). NEVER append structural tags like "(Part-1)", "Day 1", or "Part A". The string name must be perfectly identical across all consecutive days dedicated to that unit.
                2. 'Suggested Activity' must be a clear 1-sentence description explaining the specific concept to learn that day.
                3. Increment 'Scheduled Date' by 1 day per row starting 2026-07-01.
                
                Follow this exact multi-day structural example format when building the array:
                {{
                  "roadmap": [
                    {{
                      "Status": false,
                      "Scheduled Date": "2026-07-01",
                      "Time Slot": "{start_str}-{end_str}",
                      "Focus Topic": "Fundamentals of Computers - Unit I",
                      "Suggested Activity": "Study Core Hardware Frameworks: Learn the processing speeds, data capacities, and fundamental design limitations of computer hardware."
                    }},
                    {{
                      "Status": false,
                      "Scheduled Date": "2026-07-02",
                      "Time Slot": "{start_str}-{end_str}",
                      "Focus Topic": "Fundamentals of Computers - Unit I",
                      "Suggested Activity": "Examine Machine Classifications: Understand architectural and processing performance variations between micro, mini, and mainframe systems."
                    }},
                    {{
                      "Status": false,
                      "Scheduled Date": "2026-07-03",
                      "Time Slot": "{start_str}-{end_str}",
                      "Focus Topic": "Fundamentals of Computers - Unit I",
                      "Suggested Activity": "Review Computing History: Trace hardware generations from initial electronic vacuum tubes to modern microprocessors."
                    }}
                  ]
                }}
                """
                
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are a precise computer program that outputs raw JSON objects without code blocks or conversational text. You match array length instructions perfectly."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.2,
                    max_tokens=2500  
                )
                
                raw_json = json.loads(response.choices[0].message.content)
                roadmap_data = raw_json.get("roadmap", [])
                
                for item in roadmap_data:
                    if "Status" not in item:
                        item["Status"] = False
                
                st.session_state.roadmap_list = roadmap_data
                st.session_state.generated = True
                
                save_user_data_to_firestore(st.session_state.id_token, roadmap_data, st.session_state.username, st.session_state.user_email)
                
            except Exception as e:
                st.error(f"App compilation process encountered an evaluation exception: {e}")

# Render UI Dashboard Safely
if st.session_state.generated:
    st.markdown("### 🔄 Interactive Study Roadmap")
    
    roadmap = st.session_state.roadmap_list
    
    if roadmap:
        completed_count = 0
        
        save_col, csv_col = st.columns(2)
        with save_col:
            if st.button("Save It", type="primary", use_container_width=True):
                if save_user_data_to_firestore(st.session_state.id_token, st.session_state.roadmap_list, st.session_state.username, st.session_state.user_email):
                    st.toast("Progress saved successfully to Cloud Firestore!", icon="🔥")
                else:
                    st.error("Failed to sync progress changes to Firestore collection.")
        with csv_col:
            csv_bytes = convert_to_csv(st.session_state.roadmap_list)
            st.download_button("📊 Download Roadmap Spreadsheet (.csv)", data=csv_bytes, file_name="study_roadmap.csv", mime="text/csv", use_container_width=True)
            
        st.markdown("---")
        
        for i, item in enumerate(roadmap):
            date_str = item.get('Scheduled Date', '')
            time_str = item.get('Time Slot', '')
            topic_str = item.get('Focus Topic', '')
            activity_str = item.get('Suggested Activity', '')
            current_status = item.get('Status', False)
            
            label_markdown = f"⚡ **{date_str}** &nbsp;|&nbsp; ⏱️ `{time_str}` &nbsp;|&nbsp; 🪐 **{topic_str}**  \n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📡 *Modules Matrix: {activity_str}*"
            
            is_checked = st.checkbox(label_markdown, value=current_status, key=f"task_{i}")
            if is_checked:
                completed_count += 1
            
            st.session_state.roadmap_list[i]["Status"] = is_checked
                
            st.markdown("---")
        
        total_tasks = len(roadmap)
        progress_percent = int((completed_count / total_tasks) * 100) if total_tasks > 0 else 0
        
        st.markdown(f"**Progress Check:** {completed_count}/{total_tasks} Milestones Completed ({progress_percent}%)")
        st.progress(progress_percent / 100.0)
else:
    st.info("Configuration parameters pending: Feed a course document file into the parameters block above to populate your interactive dashboard.")