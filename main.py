### ---- Imports ----- ###
import streamlit as st
import PyPDF2 #used to load pdf files
import io
import os 
from openai import OpenAI
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from docx  import Document

load_dotenv()  # Load environment variables from .env file

###------------------- Set Streamlit Page Configurations -----------------------------------###
st.set_page_config(page_title = "AI Resume Critique Agent", page_icon = ":📑", layout = "centered")
st.title("AI Resume Critique Agent")
st.markdown("## Get AI-powered feedback on your resume")
st.markdown("Upload your resume in PDF format and get AI feedback on how to improve it. \n Also, upload a job description to get tailored feedback on how your resume compares to that role.")
st.markdown(
    """
    <hr style="border: 1px solid #ccc; margin: 20px 0;">
    """,
    unsafe_allow_html=True
)

### --------- Load in OpenAI API Key ---- ###
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


###------------------- Functions for Embedding and Similarity Calculation -----------------------------------###
def get_embedding(text):
    """Fetch OpenAI embedding for text."""
    text = text.replace("\n", " ")
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def calculate_similarity(text1, text2):
    """Calculate cosine similarity between two texts."""
    emb1 = np.array(get_embedding(text1)).reshape(1, -1)
    emb2 = np.array(get_embedding(text2)).reshape(1, -1)
    similarity = cosine_similarity(emb1, emb2)[0][0]
    return round(similarity * 100, 2)  # return percentage


###------------------- User Inputs for file and text input -----------------------------------###
upload_file = st.file_uploader("Upload your resume (PDF, TXT, or DOC)", type=["pdf", "txt", "docx"])
job_role = st.text_input("Enter the job role you are targeting:")
job_description = st.text_area("Paste the job description here (optional):", height=200)
analyze_button = st.button("Analyze Resume")


###------------------- Load text from PDF or Text File -----------------------------------###
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

def extract_docx(docx_file):
    doc = Document(docx_file)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)

if analyze_button and upload_file:
    try: 
        file_content = extract_text(upload_file)
        
        if not file_content.strip():
            st.error("File does not have content")
            st.stop
            
        
        similarity_score = None
        if job_description.strip():
            similarity_score = calculate_similarity(file_content, job_description)
            st.info(f"**Resume-Job Description Match:** {similarity_score}%")

            
        prompt = f"""Please analyze this resume and provide constructive feedback. 
        Focus on the following aspects: 
        1) Content clarity 
        2) Presentation of skills/tools
        3) Experience descriptions
        4) Specific improvements/suggestions for {job_role if job_role else 'general job applications'}
        
        Resume content: 
        {file_content}
        
        Please provide recommendations in a clear, structured format. Highlight any relevant lines with specific recommendations."""
        
        if job_description.strip():
            prompt += f""" Compare this resume with the job description provided. {job_description}
            Provide tailored feedback on how well the resume aligns with the job requirements.
            Suggest specific changes to improve the match."""
        client = OpenAI(api_key=OPENAI_API_KEY) 
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert resume reviewer with experience in HR and recruiting"}, ## gives context to the model
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens = 1000
        )
        
        st.markdown("###Analysis Results")
        st.markdown(response.choices[0].message.content) #get first response (if more than 1) 
    except Exception as e: 
        st.error(f"""An error occured: {str(e)}""")