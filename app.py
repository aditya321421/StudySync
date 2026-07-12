import streamlit as st
import pypdf
import json
from google import genai
from google.genai import types

# Setup AI Client
client = genai.Client()

st.set_page_config(page_title="Study-Sync", page_icon="🔄")

st.title("🔄 Study-Sync")
st.subheader("AI Powered Study Planner")

# Sidebar for controls
uploaded_file = st.sidebar.file_uploader("Upload Study PDF", type="pdf")
start_time = st.sidebar.time_input("Start Time")
end_time = st.sidebar.time_input("End Time")

def get_ai_plan(text, start, end):
    prompt = f"Create a study plan for material: {text[:5000]} from {start} to {end}."
    # Simplified call for demonstration
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

if st.sidebar.button("Generate Schedule"):
    if uploaded_file:
        reader = pypdf.PdfReader(uploaded_file)
        text = "".join([p.extract_text() for p in reader.pages[:10]])
        plan = get_ai_plan(text, start_time, end_time)
        st.write(plan)
    else:
        st.error("Please upload a PDF first!")