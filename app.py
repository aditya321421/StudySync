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
if "roadmap_df" not in st.session_state:
    st.session_state.roadmap_df = pd.DataFrame()

# Sidebar Controls
st.sidebar.header("⚡ Configuration Panel")
uploaded_file = st.sidebar.file_uploader("Upload Course Syllabus/PDF", type=["pdf"])
start_time = st.sidebar.time_input("Preferred Daily Start Time")
end_time = st.sidebar.time_input("Preferred Daily End Time")
generate_btn = st.sidebar.button("Generate Complete Roadmap", type="primary", use_container_width=True)

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def convert_to_ics(df):
    ics_text = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Study-Sync//Study Plan//EN\n"
    for _, row in df.iterrows():
        clean_date = str(row['Scheduled Date']).replace("-", "")
        ics_text += f"BEGIN:VEVENT\nSUMMARY:{row['Focus Topic']}\nDESCRIPTION:{row['Suggested Activity']}\nDTSTART:{clean_date}T090000Z\nDTEND:{clean_date}T100000Z\nEND:VEVENT\n"
    ics_text += "END:VCALENDAR"
    return ics_text.encode('utf-8')

if generate_btn:
    if not uploaded_file:
        st.sidebar.error("Please upload a course document first!")
    else:
        with st.spinner("Analyzing syllabus and building your comprehensive 45-50 day timeline..."):
            try:
                # Read text from the target document
                reader = pypdf.PdfReader(uploaded_file)
                pdf_text = ""
                for page in reader.pages[:15]: 
                    pdf_text += page.extract_text() or ""
                
                start_str = start_time.strftime("%I:%M %p")
                end_str = end_time.strftime("%I:%M %p")
                
                # Optimized text capacity to fit safely right under Groq's 6,000 TPM limit
                prompt = f"""
                You are a helpful personal academic tutor. Analyze this syllabus content:
                ---
                {pdf_text[:14000]}
                ---
                
                Create an extensive day-by-day sequential study roadmap. 
                Daily study session windows: {start_str} to {end_str}.
                
                STRICT COMPLIANCE DIRECTIVES:
                1. You MUST generate an exhaustive roadmap array containing a minimum of 45 to 50 distinct daily row entries.
                2. For the 'Focus Topic' field, write ONLY the Subject Name and Unit Number (e.g., "Fundamentals of Computers - Unit I"). Do not append structural suffixes like "(Part-1)" or "(Part 2)".
                3. For the 'Suggested Activity' field, isolate exactly ONE core topic, theorem, keyword, or concept from that unit for that specific day. Write a clear, student-friendly description explaining what they need to study or define.
                4. Stretch your breakdown out across all available subjects in the text. Break down individual concepts into micro-steps across consecutive days to ensure you hit the 45-50 item requirement easily.
                5. Increment the 'Scheduled Date' string field by exactly 1 calendar day for each progressive milestone entry row starting from 2026-07-01.
                
                Respond ONLY with a valid JSON object matching this structural layout blueprint without markdown wrapper code blocks:
                {{
                  "deadlines": [
                    {{"Subject": "Name of Subject", "due_date": "2027-01-20"}}
                  ],
                  "roadmap": [
                    {{
                      "Status": false,
                      "Scheduled Date": "2026-07-01",
                      "Time Slot": "{start_str}-{end_str}",
                      "Focus Topic": "Fundamentals of Computers - Unit I",
                      "Suggested Activity": "Study Computer System Characteristics: Learn the essential capabilities, speed metrics, and core operational limitations of processing hardware."
                    }}
                  ]
                }}
                """
                
                # Groq API call with explicit output token bandwidth unlocked
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are a precise data parser who outputs raw, strict JSON without commentary. You generate long arrays exactly matching requested item counts."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.2,
                    max_tokens=2500 # Unlocks the maximum output length constraint
                )
                
                raw_json = json.loads(response.choices[0].message.content)
                
                st.session_state.deadlines_data = raw_json.get("deadlines", [])
                st.session_state.roadmap_df = pd.DataFrame(raw_json.get("roadmap", []))
                st.session_state.generated = True
                
            except Exception as e:
                st.error(f"App compilation process encountered an evaluation exception: {e}")

# Render UI Dashboards
if st.session_state.generated:
    left_col, right_col = st.columns([1, 2], gap="large")
    
    with left_col:
        st.markdown("### 📅 Extracted Deadlines")
        st.dataframe(st.session_state.deadlines_data, use_container_width=True, hide_index=True)
        
    with right_col:
        st.markdown("### 🔄 Interactive Study Roadmap")
        df = st.session_state.roadmap_df
        
        if not df.empty:
            edited_df = st.data_editor(
                df,
                column_config={
                    "Status": st.column_config.CheckboxColumn("Status", default=False),
                    "Scheduled Date": st.column_config.TextColumn("Date", disabled=True),
                    "Time Slot": st.column_config.TextColumn("Time Slot", disabled=True),
                    "Focus Topic": st.column_config.TextColumn("Subject & Unit", disabled=True),
                    "Suggested Activity": st.column_config.TextColumn("Study Description & Topic Focus", disabled=True),
                },
                hide_index=True,
                use_container_width=True,
                key="roadmap_editor"
            )
            
            completed_tasks = int(edited_df["Status"].sum())
            total_tasks = len(edited_df)
            progress_percent = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
            
            st.markdown(f"**Progress:** {completed_tasks}/{total_tasks} Milestones Completed ({progress_percent}%)")
            st.progress(progress_percent / 100.0)
            st.session_state.roadmap_df = edited_df

    st.markdown("---")
    btn_col1, btn_col2 = st.columns(2)
    
    if not st.session_state.roadmap_df.empty:
        csv_bytes = convert_df_to_csv(st.session_state.roadmap_df)
        ics_bytes = convert_to_ics(st.session_state.roadmap_df)
        
        with btn_col1:
            st.download_button("🗓️ Export to Calendar (.ics)", data=ics_bytes, file_name="study_schedule.ics", mime="text/calendar", use_container_width=True)
        with btn_col2:
            st.download_button("📊 Download Spreadsheet (.csv)", data=csv_bytes, file_name="study_roadmap.csv", mime="text/csv", use_container_width=True)
else:
    st.info("Configuration parameters pending: Feed a course document file into the sidebar parameters to populate the interactive dashboard.")