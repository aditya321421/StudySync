import streamlit as st
import pypdf
import json
from google import genai
from google.genai import types

# Initialize Gemini Client (looks for GEMINI_API_KEY environment variable automatically)
client = genai.Client()

# Configure the browser tab title and wide dashboard layout
st.set_page_config(page_title="Study-Sync", page_icon="🔄", layout="wide")

# App Header Layout
st.title("🔄 Study-Sync")
st.markdown("#### *Your AI-Powered Chronological Study Planner*")
st.markdown("---")

# Setup a clean, responsive two-column layout grid
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader("⚡ Set Your Session")
    
    # Core User Inputs handled entirely by Streamlit
    uploaded_file = st.file_uploader("Upload Study PDF (Syllabus/Chapter)", type=["pdf"])
    
    start_time = st.time_input("Select Start Time")
    end_time = st.time_input("Select End Time")
    
    generate_btn = st.button("Sync My Schedule", type="primary", use_container_width=True)

with col2:
    st.subheader("📅 Your Custom Plan")
    
    if generate_btn:
        # Input Validation Guardrails
        if not uploaded_file:
            st.error("Please upload a PDF document first!")
        elif start_time >= end_time:
            st.error("Invalid Range: Start time must occur before your end time boundary.")
        else:
            # Display loader animation while Python handles text parsing and AI communication
            with st.spinner("AI is analyzing your material and building your timeline..."):
                try:
                    # Extract Text from the uploaded PDF stream directly out of RAM memory
                    reader = pypdf.PdfReader(uploaded_file)
                    pdf_text = ""
                    for page in reader.pages[:15]: # Process up to 15 pages max
                        pdf_text += page.extract_text() or ""
                    
                    # Formatting times into clean strings
                    start_str = start_time.strftime("%I:%M %p")
                    end_str = end_time.strftime("%I:%M %p")
                    
                    # Prompt structure requesting strict data arrays from Gemini
                    prompt = f"""
                    You are an expert academic tutor. 
                    Create a highly realistic study schedule broken down into chronological blocks based on this material:
                    ---
                    {pdf_text[:10000]}
                    ---
                    The study session runs exactly from {start_str} to {end_str}.
                    Include 5-10 minute breaks if the session is long.
                    
                    You must respond ONLY with a valid JSON array of objects.
                    Each object must have exactly two keys: "time" and "activity".
                    Example format:
                    [
                      {{"time": "{start_str}", "activity": "Review introduction basics"}},
                      {{"time": "Next Interval", "activity": "Take a short break"}}
                    ]
                    """
                    
                    # Generate content with structured configuration constraints
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            temperature=0.3
                        ),
                    )
                    
                    # Convert response JSON text string into an actionable Python list array
                    study_plan = json.loads(response.text)
                    
                    # Render the finalized UI components
                    for item in study_plan:
                        with st.container(border=True):
                            st.markdown(f"⏳ **{item['time']}**")
                            st.write(item['activity'])
                            
                except Exception as e:
                    st.error(f"An unexpected system processing exception occurred: {e}")
    else:
        # Default screen placeholder state
        st.info("Upload your document and set your targets on the left column panel to view your timeline grid.")