import streamlit as st
import pypdf
import json
import pandas as pd
from groq import Groq
from io import BytesIO

# Initialize Groq Client
client = Groq()

# Configure page settings
st.set_page_config(page_title="Study-Sync | Dashboard", page_icon="🔄", layout="wide")

st.title("🔄 Study-Sync Dashboard")
st.markdown("#### *Interactive Study Roadmap & Deadline Tracker*")
st.markdown("---")

# Initialize persistent session states so interactive checkboxes don't clear on click
if "generated" not in st.session_state:
    st.session_state.generated = False
if "deadlines_data" not in st.session_state:
    st.session_state.deadlines_data = []
if "roadmap_df" not in st.session_state:
    st.session_state.roadmap_df = pd.DataFrame()

# Sidebar Setup for Input Controls
st.sidebar.header("⚡ Configuration Panel")
uploaded_file = st.sidebar.file_uploader("Upload Course Syllabus/PDF", type=["pdf"])
start_time = st.sidebar.time_input("Preferred Daily Start Time")
end_time = st.sidebar.time_input("Preferred Daily End Time")
generate_btn = st.sidebar.button("Generate Complete Roadmap", type="primary", use_container_width=True)

# Helper function to generate standard CSV data bytes
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Helper function to generate basic .ics calendar file format layout strings
def convert_to_ics(df):
    ics_text = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Study-Sync//Study Plan//EN\n"
    for _, row in df.iterrows():
        clean_date = str(row['Scheduled Date']).replace("-", "")
        ics_text += f"BEGIN:VEVENT\nSUMMARY:{row['Focus Topic']}\nDESCRIPTION:{row['Suggested Activity']}\nDTSTART:{clean_date}T090000Z\nDTEND:{clean_date}T100000Z\nEND:VEVENT\n"
    ics_text += "END:VCALENDAR"
    return ics_text.encode('utf-8')

# Main Action Execution Engine
if generate_btn:
    if not uploaded_file:
        st.sidebar.error("Please upload a course document first!")
    else:
        with st.spinner("AI Engine running: Extracting structural tracking timelines..."):
            try:
                # Read text layout layers out of the target document
                reader = pypdf.PdfReader(uploaded_file)
                pdf_text = ""
                for page in reader.pages[:15]: 
                    pdf_text += page.extract_text() or ""
                
                start_str = start_time.strftime("%H:%M")
                end_str = end_time.strftime("%H:%M")
                
                # Specialized complex system prompt to extract the split-panel dashboard metrics
                prompt = f"""
                You are a senior academic coordinator. Analyze this textbook syllabus context completely:
                ---
                {pdf_text[:12000]}
                ---
                Generate two balanced target datasets structured into a single unified valid JSON object:
                1. "deadlines": A list tracking all distinct core courses/subjects mentioned, assigning logical future target evaluation dates sequentially spread out between late 2026 and 2027 based on current year 2026.
                2. "roadmap": A detailed progressive sequence of exact study tasks breaking the syllabus contents down item by item. Use incremental calendar dates starting from 2026-07-01 onwards. Use the time slots matching the constraints {start_str} to {end_str}.
                
                Respond ONLY with a valid JSON object matching this structural layout blueprint without markdown blocks:
                {{
                  "deadlines": [
                    {{"Subject": "Fundamentals of Computers", "due_date": "2027-01-20"}}
                  ],
                  "roadmap": [
                    {{"Status": false, "Scheduled Date": "2026-07-01", "Time Slot": "{start_str}-{end_str}", "Focus Topic": "Control Unit Functionality (CSA5001T)", "Suggested Activity": "Read text layout docs"}}
                  ]
                }}
                """
                
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are a precise data scientist outputting strict JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.2
                )
                
                # Store structural response fragments cleanly inside dataframes
                raw_json = json.loads(response.choices[0].message.content)
                
                st.session_state.deadlines_data = raw_json.get("deadlines", [])
                st.session_state.roadmap_df = pd.DataFrame(raw_json.get("roadmap", []))
                st.session_state.generated = True
                
            except Exception as e:
                st.error(f"App compilation process encountered an evaluation exception: {e}")

# Render Interactive Elements Dashboard Interface
if st.session_state.generated:
    # Set up the split-column layout grid mirroring your visual reference screenshot
    left_col, right_col = st.columns([2, 3], gap="large")
    
    with left_col:
        st.markdown("### 📅 Extracted Deadlines")
        st.dataframe(
            st.session_state.deadlines_data, 
            use_container_width=True, 
            hide_index=True
        )
        
    with right_col:
        st.markdown("### 🔄 Interactive Study Roadmap")
        
        # Calculate progress completion metrics programmatically out of our state container
        df = st.session_state.roadmap_df
        
        if not df.empty:
            # Render the interactive data grid editor component
            edited_df = st.data_editor(
                df,
                column_config={
                    "Status": st.column_config.CheckboxColumn("Status", default=False),
                    "Scheduled Date": st.column_config.TextColumn("Scheduled Date", disabled=True),
                    "Time Slot": st.column_config.TextColumn("Time Slot", disabled=True),
                    "Focus Topic": st.column_config.TextColumn("Focus Topic", disabled=True),
                    "Suggested Activity": st.column_config.TextColumn("Suggested Activity", disabled=True),
                },
                hide_index=True,
                use_container_width=True,
                key="roadmap_editor"
            )
            
            # Recalculate progress values live as checkboxes cycle
            completed_tasks = int(edited_df["Status"].sum())
            total_tasks = len(edited_df)
            progress_percent = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
            
            # Display tracking metrics header layout block
            st.markdown(f"**Progress:** {completed_tasks}/{total_tasks} Milestones Completed ({progress_percent}%)")
            st.progress(progress_percent / 100.0)
            
            # Keep state updated
            st.session_state.roadmap_df = edited_df

    # Bottom Actions Utility Block Layout Row
    st.markdown("---")
    btn_col1, btn_col2 = st.columns(2)
    
    if not st.session_state.roadmap_df.empty:
        csv_bytes = convert_df_to_csv(st.session_state.roadmap_df)
        ics_bytes = convert_to_ics(st.session_state.roadmap_df)
        
        with btn_col1:
            st.download_button(
                label="🗓️ Export to Calendar (.ics)",
                data=ics_bytes,
                file_name="study_schedule.ics",
                mime="text/calendar",
                use_container_width=True
            )
        with btn_col2:
            st.download_button(
                label="📊 Download Spreadsheet (.csv)",
                data=csv_bytes,
                file_name="study_roadmap.csv",
                mime="text/csv",
                use_container_width=True
            )
else:
    st.info("Configuration parameters pending: Feed a course document file into the sidebar parameters to populate the interactive planning dashboard grid layout panel.")