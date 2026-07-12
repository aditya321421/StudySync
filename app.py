import streamlit as st
import pypdf
import json
from groq import Groq

# Initialize Groq Client (automatically reads the GROQ_API_KEY environment variable)
client = Groq()

# Configure page settings
st.set_page_config(page_title="Study-Sync", page_icon="🔄", layout="wide")

st.title("🔄 Study-Sync")
st.markdown("#### *Your AI-Powered Chronological Study Planner (Powered by Groq)*")
st.markdown("---")

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader("⚡ Set Your Session")
    uploaded_file = st.file_uploader("Upload Study PDF (Syllabus/Chapter)", type=["pdf"])
    start_time = st.time_input("Select Start Time")
    end_time = st.time_input("Select End Time")
    generate_btn = st.button("Sync My Schedule", type="primary", use_container_width=True)

with col2:
    st.subheader("📅 Your Custom Plan")
    
    if generate_btn:
        if not uploaded_file:
            st.error("Please upload a PDF document first!")
        elif start_time >= end_time:
            st.error("Invalid Range: Start time must occur before your end time boundary.")
        else:
            with st.spinner("Groq is rapidly analyzing your material..."):
                try:
                    # Extract text from PDF
                    reader = pypdf.PdfReader(uploaded_file)
                    pdf_text = ""
                    for page in reader.pages[:15]: 
                        pdf_text += page.extract_text() or ""
                    
                    start_str = start_time.strftime("%I:%M %p")
                    end_str = end_time.strftime("%I:%M %p")
                    
                    # Formulate the prompt
                    prompt = f"""
                    You are an expert academic tutor.
                    Create a realistic study schedule broken down into chronological blocks based on this material:
                    ---
                    {pdf_text[:12000]}
                    ---
                    The study session runs exactly from {start_str} to {end_str}. Include short breaks.
                    
                    You must respond ONLY with a valid JSON object containing a "plan" key which holds an array of items. Do not include markdown formatting like ```json.
                    
                    Expected structure:
                    {{
                      "plan": [
                        {{"time": "{start_str}", "activity": "Review introduction basics"}},
                        {{"time": "Next Interval", "activity": "Take a short break"}}
                      ]
                    }}
                    """
                    
                    # Groq API call using llama3-8b-8192
                    response = client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant designed to output strict JSON."},
                            {"role": "user", "content": prompt}
                        ],
                        response_format={"type": "json_object"},
                        temperature=0.3
                    )
                    
                    # Parse JSON safely
                    result_json = json.loads(response.choices[0].message.content)
                    study_plan = result_json.get("plan", [])
                    
                    # Render layout timeline items
                    for item in study_plan:
                        with st.container(border=True):
                            st.markdown(f"⏳ **{item['time']}**")
                            st.write(item['activity'])
                            
                except Exception as e:
                    st.error(f"An unexpected system processing exception occurred: {e}")
    else:
        st.info("Upload your document and set your targets on the left column panel to view your timeline grid.")