import streamlit as st
import PyPDF2 #used to load pdf files
import io
import os 
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

st.set_page_config(page_title = "AI Resume Critique Agent", page_icon = ":📑", layout = "centered")

st.title("AI Resume Critique Agent")
st.markdown("Upload your resume in PDF format and get AI feedback on how to improve it.")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

upload_file = st.file_uploader("Upload your resume (PDF, TXT, or DOC)", type=["pdf", "txt", "docx"])
job_role = st.text_input("Enter the job role you are targeting:")

analyze_button = st.button("Analyze Resume")

def extract_pdf_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text    

def extract_text(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_pdf_text(io.BytesIO(upload_file.read()))
    return upload.file.read().decode("utf-8")

if analyze_button and upload_file:
    try: 
        file_content = exctract_text(upload_file)
        
        if not file_content.strip():
            st.error("File does not have content")
            st.stop
            
        prompt = f"""Please analyze this resume and provide constructive feedback. 
        Focus on the following aspects: 
        1) Content clarity 
        2) Presentation of skills/tools
        3) Experience descriptions
        4) Specific improvements/suggestions for {job_role if job_role else 'general job applications'}
        
        Resume content: 
        {file_content}
        
        Please provide recommendations in a clear, structured format. Highlight any relevant lines with specific recommendations."""
        
        client = OpenAI(api_key=OPENAI_API_KEY) 