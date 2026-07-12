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
if "deadlines_data" not in st.session_state:
    st.session_state.deadlines_data = []
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
        with st.spinner("Analyzing syllabus and crafting your safe 45-50 day timeline..."):
            try:
                # Read text from the target document
                reader = pypdf.PdfReader(uploaded_file)
                pdf_text = ""
                for page in reader.pages[:10]: 
                    pdf_text += page.extract_text() or ""
                
                start_str = start_time.strftime("%I:%M %p")
                end_str = end_time.strftime("%I:%M %p")
                
                prompt = f"""
                Analyze this syllabus:
                {pdf_text[:9000]}
                
                Create a daily study roadmap from {start_str} to {end_str}.
                
                RULES:
                1. You MUST generate between 45 to 50 entries in the roadmap array.
                2. 'Focus Topic' must ONLY be Subject Name and Unit (e.g., "Fundamentals of Computers - Unit I"). No structural suffixes like "(Part-1)".
                3. 'Suggested Activity' must be ONE specific topic with a short, helpful 1-sentence explanation of what to learn. No comma lists.
                4. Split units sequentially over multiple days to easily hit the 45-50 row requirement.
                5. Increment 'Scheduled Date' by 1 day per row starting 2026-07-01.
                
                Return raw JSON matching this format:
                {{
                  "deadlines": [{{"Subject": "Name", "due_date": "2027-01-20"}}],
                  "roadmap": [
                    {{
                      "Scheduled Date": "2026-07-01",
                      "Time Slot": "{start_str}-{end_str}",
                      "Focus Topic": "Fundamentals of Computers - Unit I",
                      "Suggested Activity": "Study Computer System Characteristics: Learn core hardware processing capabilities and operational limitations."
                    }}
                  ]
                }}
                """
                
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are a data parser outputting raw JSON objects without code blocks or filler text."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.2,
                    max_tokens=2000 
                )
                
                raw_json = json.loads(response.choices[0].message.content)
                st.session_state.deadlines_data = raw_json.get("deadlines", [])
                st.session_state.roadmap_list = raw_json.get("roadmap", [])
                st.session_state.generated = True
                
            except Exception as e:
                st.error(f"App compilation process encountered an evaluation exception: {e}")

# Render UI Dashboards Safely
if st.session_state.generated:
    left_col, right_col = st.columns([1, 2], gap="large")
    
    with left_col:
        st.markdown("### 📅 Extracted Deadlines")
        st.dataframe(st.session_state.deadlines_data, use_container_width=True, hide_index=True)
        
    with right_col:
        st.markdown("### 🔄 Interactive Study Roadmap")
        
        roadmap = st.session_state.roadmap_list
        
        if roadmap:
            # Table Header Layout
            h_col1, h_col2, h_col3, h_col4 = st.columns([0.5, 1.2, 2.3, 4.0])
            h_col1.markdown("**Status**")
            h_col2.markdown("**Date & Time**")
            h_col3.markdown("**Subject & Unit**")
            h_col4.markdown("**Study Description & Topic Focus**")
            st.markdown("---")
            
            completed_count = 0
            
            # Loop through rows to generate native checkboxes instead of using the complex data_editor
            for i, item in enumerate(roadmap):
                r_col1, r_col2, r_col3, r_col4 = st.columns([0.5, 1.2, 2.3, 4.0])
                
                with r_col1:
                    # Maintain individual checked states persistently in session memory
                    is_checked = st.checkbox("", key=f"task_{i}")
                    if is_checked:
                        completed_count += 1
                        
                with r_col2:
                    st.caption(f"📅 {item.get('Scheduled Date', '')}\n⏰ {item.get('Time Slot', '')}")
                with r_col3:
                    st.markdown(f"**{item.get('Focus Topic', '')}**")
                with r_col4:
                    st.write(item.get('Suggested Activity', ''))
            
            # Progress Tracking Header Metrics
            total_tasks = len(roadmap)
            progress_percent = int((completed_count / total_tasks) * 100) if total_tasks > 0 else 0
            
            st.markdown("---")
            st.markdown(f"**Progress:** {completed_count}/{total_tasks} Milestones Completed ({progress_percent}%)")
            st.progress(progress_percent / 100.0)

    # Export Action Row
    if st.session_state.roadmap_list:
        csv_bytes = convert_to_csv(st.session_state.roadmap_list)
        st.download_button("📊 Download Roadmap Spreadsheet (.csv)", data=csv_bytes, file_name="study_roadmap.csv", mime="text/csv", use_container_width=True)
else:
    st.info("Configuration parameters pending: Feed a course document file into the sidebar parameters to populate the interactive dashboard.")