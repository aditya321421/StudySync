from flask import Flask, render_template, request
import pypdf
import os
import json
from google import genai
from google.genai import types

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the Gemini client (looks for GEMINI_API_KEY environment variable automatically)
client = genai.Client()

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as f:
            reader = pypdf.PdfReader(f)
            # Read first 15 pages maximum to protect processing window boundaries
            for page in reader.pages[:15]: 
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def generate_ai_study_plan(pdf_text, start_time, end_time):
    prompt = f"""
    You are an expert academic tutor. 
    Create a highly realistic study schedule broken down into chronological blocks based on this material:
    ---
    {pdf_text[:10000]}
    ---
    The study session runs exactly from {start_time} to {end_time}.
    Include 5-10 minute breaks if the session is long.
    
    You must respond ONLY with a valid JSON array of objects.
    Each object must have exactly two keys: "time" and "activity".
    Example format:
    [
      {{"time": "{start_time}", "activity": "Review introduction chapter basics"}},
      {{"time": "Next Interval", "activity": "Take a short break"}}
    ]
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3
            ),
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return [
            {"time": start_time, "activity": "Error connecting to AI. Please verify your Render Environment Variables config layout."},
            {"time": end_time, "activity": "Session complete."}
        ]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf_file = request.files.get('syllabus')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        
        if pdf_file and pdf_file.filename != '':
            filepath = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
            pdf_file.save(filepath)
            
            pdf_text = extract_text_from_pdf(filepath)
            study_plan = generate_ai_study_plan(pdf_text, start_time, end_time)
            
            os.remove(filepath) # Cleans up server disk storage automatically
            return render_template('index.html', plan=study_plan, generated=True)
            
    return render_template('index.html', plan=None, generated=False)

if __name__ == '__main__':
    app.run(debug=True)