import streamlit as st
import pypdf
import json
import pandas as pd
import requests
from groq import Groq

# Initialize Groq Client
client = Groq()

# Configure page settings
st.set_page_config(page_title="Study-Sync | Dashboard", page_icon="🔄", layout="wide")

# Fetch Firebase API Key from Secrets
FIREBASE_API_KEY = st.secrets.get("FIREBASE_API_KEY")

# Initialize persistent session states for Auth and Planner data
if "auth_state" not in st.session_state:
    st.session_state.auth_state = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "generated" not in st.session_state:
    st.session_state.generated = False
if "roadmap_list" not in st.session_state:
    st.session_state.roadmap_list = []

# --- FIREBASE AUTHENTICATION FUNCTIONS ---
def firebase_auth(email, password, mode="signInWithPassword"):
    """Handles both Sign In and Sign Up requests via Firebase Rest API."""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:{mode}?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    
    try:
        response = requests.post(url, json=payload)
        res_data = response.json()
        
        if response.status_code == 200:
            return {"success": True, "email": res_data["email"]}
        else:
            error_msg = res_data.get("error", {}).get("message", "Authentication Failed")
            return {"success": False, "message": error_msg}
    except Exception as e:
        return {"success": False, "message": str(e)}

# --- LOGOUT UTILITY ---
def logout():
    st.session_state.auth_state = False
    st.session_state.user_email = ""
    st.session_state.generated = False
    st.session_state.roadmap_list = []
    st.rerun()

# ==========================================
#  INTERFACE ROUTING: AUTHENTICATION PORTAL
# ==========================================
if not st.session_state.auth_state:
    st.title("🔒 Welcome to Study-Sync")
    st.markdown("#### *Please sign in or create an account to access your daily study plans.*")
    st.markdown("---")
    
    auth_mode = st.radio("Choose an option:", ["Login", "Sign Up"], horizontal=True)
    
    with st.form("auth_form"):
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        submit_btn = st.form_submit_button("Submit")
        
        if submit_btn:
            if not email or not password:
                st.error("Please fill out all fields.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long.")
            else:
                mode_action = "signInWithPassword" if auth_mode == "Login" else "signUp"
                with st.spinner("Verifying credentials with Firebase..."):
                    result = firebase_auth(email, password, mode=mode_action)
                
                if result["success"]:
                    st.session_state.auth_state = True
                    st.session_state.user_email = result["email"]
                    st.success(f"Welcome back, {result['email']}!")
                    st.rerun()
                else:
                    st.error(f"Error: {result['message']}")
    st.stop() # Halts app execution here until user passes authorization checks

# ==========================================
#  INTERFACE ROUTING: CORE APPLICATION
# ==========================================
st.title("🔄 Study-Sync Dashboard")
st.markdown(f"#### *Active Session: User Identity logged in as **{st.session_state.user_email}***")
st.markdown("---")

# Sidebar Controls
st.sidebar.header("⚡ Configuration Panel")
uploaded_file = st.sidebar.file_uploader("Upload Course Syllabus/PDF", type=["pdf"])
start_time = st.sidebar.time_input("Preferred Daily Start Time")
end_time = st.sidebar.time_input("Preferred Daily End Time")
generate_btn = st.sidebar.button("Generate Complete Roadmap", type="primary", use_container_width=True)

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Log Out Session", use_container_width=True):
    logout()

def convert_to_csv(data_list):
    df = pd.DataFrame(data_list)
    return df.to_csv(index=False).encode('utf-8')

if generate_btn:
    if not uploaded_file:
        st.sidebar.error("Please upload a course document first!")
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
                      "Scheduled Date": "2026-07-01",
                      "Time Slot": "{start_str}-{end_str}",
                      "Focus Topic": "Fundamentals of Computers - Unit I",
                      "Suggested Activity": "Study Core Hardware Frameworks: Learn the processing speeds, data capacities, and fundamental design limitations of computer hardware."
                    }},
                    {{
                      "Scheduled Date": "2026-07-02",
                      "Time Slot": "{start_str}-{end_str}",
                      "Focus Topic": "Fundamentals of Computers - Unit I",
                      "Suggested Activity": "Examine Machine Classifications: Understand architectural and processing performance variations between micro, mini, and mainframe systems."
                    }},
                    {{
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
                st.session_state.roadmap_list = raw_json.get("roadmap", [])
                st.session_state.generated = True
                
            except Exception as e:
                st.error(f"App compilation process encountered an evaluation exception: {e}")

# Render UI Dashboard Safely (Flat Layout protects against memory crash conditions)
if st.session_state.generated:
    st.markdown("### 🔄 Interactive Study Roadmap")
    
    roadmap = st.session_state.roadmap_list
    
    if roadmap:
        completed_count = 0
        
        for i, item in enumerate(roadmap):
            date_str = item.get('Scheduled Date', '')
            time_str = item.get('Time Slot', '')
            topic_str = item.get('Focus Topic', '')
            activity_str = item.get('Suggested Activity', '')
            
            label_markdown = f"🗓️ **{date_str}** | ⏰ {time_str} | 📘 **{topic_str}**\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📝 *{activity_str}*"
            
            is_checked = st.checkbox(label_markdown, key=f"task_{i}")
            if is_checked:
                completed_count += 1
                
            st.markdown("---")
        
        total_tasks = len(roadmap)
        progress_percent = int((completed_count / total_tasks) * 100) if total_tasks > 0 else 0
        
        st.markdown(f"**Progress:** {completed_count}/{total_tasks} Milestones Completed ({progress_percent}%)")
        st.progress(progress_percent / 100.0)

    if st.session_state.roadmap_list:
        csv_bytes = convert_to_csv(st.session_state.roadmap_list)
        st.download_button("📊 Download Roadmap Spreadsheet (.csv)", data=csv_bytes, file_name="study_roadmap.csv", mime="text/csv", use_container_width=True)
else:
    st.info("Configuration parameters pending: Feed a course document file into the sidebar parameters to populate the interactive dashboard.")