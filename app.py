import streamlit as st
import ollama
from PyPDF2 import PdfReader

# --- PAGE SETUP 
st.set_page_config(page_title="AI Resume Matcher", layout="centered")
st.title("📄 AI Resume Matcher (Local LLM)")

# --- PDF TEXT EXTRACTOR 
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# --- SIDEBAR: JOB DESCRIPTION 
st.sidebar.header("Job Details")
job_description = st.sidebar.text_area("Paste the Job Description here:", height=300)

# --- MAIN: RESUME UPLOADER 
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")

if st.button("Analyze Match"):
    if uploaded_file and job_description:
        with st.spinner("Analyzing with local AI..."):
            # 1. Extract Text
            resume_text = extract_text_from_pdf(uploaded_file)
            
            # 2. Construct the Prompt
            prompt = f"""
            Analyze the following Resume against the Job Description. 
            1. Give a 'Match Score' out of 100.
            2. List 3 missing keywords or skills.
            3. Suggest 1 sentence to improve the resume summary.

            Job Description: {job_description}
            Resume: {resume_text}
            """
            
            # 3. Call Ollama (Local LLM)
            response = ollama.chat(model='llama3', messages=[
                {'role': 'user', 'content': prompt}
            ])
            
            # 4. Show Result
            st.success("Analysis Complete!")
            st.markdown("### **AI Feedback:**")
            st.write(response['message']['content'])
    else:
        st.warning("Please upload a PDF and paste a Job Description first.")