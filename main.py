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



