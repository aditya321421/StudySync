import streamlit as st
import pypdf
import json
import pandas as pd
from groq import Groq

# Initialize Groq Client
client = Groq()

# Configure page settings
st.set_page_config(page_title="Study-Sync | Dashboard", page_icon="🔄", layout="wide")

st.title("🔄 Study-Sync Dashboard")
st.markdown("#### *Granular Day-by-Day Syllabus Roadmap (Powered by Groq)*")
st.markdown("---")

# Initialize persistent session states
if "generated" not in st.session_state:
    st.session_state.generated = False
if "roadmap_list" not in st.session_state:
    st.session_state.roadmap_list = []

# Sidebar Controls
st.sidebar.header("⚡ Configuration Panel")
uploaded_file = st.sidebar.file_uploader("Upload Course Syllabus/PDF", type=["pdf"])
start_time = st.sidebar.time_input("Preferred Daily Start Time")
end_time = st.sidebar.time_input("Preferred Daily End Time")
generate_btn = st.sidebar.button("Generate Complete Roadmap", type="primary", use_container_width=True)

def convert_to_csv(data_list):
    df = pd.DataFrame(data_list)
    return df.to_csv(index=False).encode('utf-8')

if generate_btn:
    if not uploaded_file:
        st.sidebar.error("Please upload a course document first!")
    else:
        with st.spinner("Analyzing syllabus and crafting an extended 45-50 day roadmap..."):
            try:
                # Read text from the target document
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
                  "deadlines": [{{"Subject": "Fundamentals of Computers", "due_date": "2027-01-20"}}],
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

# Render UI Dashboard Safely (Now occupying full screen width)
if st.session_state.generated:
    st.markdown("### 🔄 Interactive Study Roadmap")
    
    roadmap = st.session_state.roadmap_list
    
    if roadmap:
        h_col1, h_col2, h_col3, h_col4 = st.columns([0.6, 1.4, 2.5, 5.5])
        h_col1.markdown("**Status**")
        h_col2.markdown("**Date & Time**")
        h_col3.markdown("**Subject & Unit**")
        h_col4.markdown("**Study Description & Topic Focus**")
        st.markdown("---")
        
        completed_count = 0
        
        # Loop through rows to generate checklist UI elements
        for i, item in enumerate(roadmap):
            r_col1, r_col2, r_col3, r_col4 = st.columns([0.6, 1.4, 2.5, 5.5])
            
            with r_col1:
                # Fixed: Added an internal fallback label string and set visibility to collapsed to satisfy the accessibility engine
                is_checked = st.checkbox("Mark task status completed", key=f"task_{i}", label_visibility="collapsed")
                if is_checked:
                    completed_count += 1
                    
            with r_col2:
                st.caption(f"📅 {item.get('Scheduled Date', '')}\n⏰ {item.get('Time Slot', '')}")
            with r_col3:
                st.markdown(f"**{item.get('Focus Topic', '')}**")
            with r_col4:
                st.write(item.get('Suggested Activity', ''))
        
        # Progress Tracking Calculations
        total_tasks = len(roadmap)
        progress_percent = int((completed_count / total_tasks) * 100) if total_tasks > 0 else 0
        
        st.markdown("---")
        st.markdown(f"**Progress:** {completed_count}/{total_tasks} Milestones Completed ({progress_percent}%)")
        st.progress(progress_percent / 100.0)

    # Export Action Buttons Block
    if st.session_state.roadmap_list:
        csv_bytes = convert_to_csv(st.session_state.roadmap_list)
        st.download_button("📊 Download Roadmap Spreadsheet (.csv)", data=csv_bytes, file_name="study_roadmap.csv", mime="text/csv", use_container_width=True)
else:
    st.info("Configuration parameters pending: Feed a course document file into the sidebar parameters to populate the interactive dashboard.")