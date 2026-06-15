import streamlit as st
from google import genai
from PyPDF2 import PdfReader
import os

# --- PAGE SETUP 
st.set_page_config(page_title="AI Resume Matcher", layout="centered")
st.title("📄 AI Resume Matcher (Cloud Production)")

# --- INITIALIZE GEMINI CLIENT
# It automatically looks for an environment variable named GEMINI_API_KEY
@st.cache_resource
def get_ai_client():
    try:
        return genai.Client()
    except Exception:
        return None

client = get_ai_client()

# --- PDF TEXT EXTRACTOR 
def extract_text_from_pdf(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

# --- SIDEBAR: JOB DESCRIPTION 
st.sidebar.header("Job Details")
job_description = st.sidebar.text_area("Paste the Job Description here:", height=300)

# --- MAIN: RESUME UPLOADER 
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")

if st.button("Analyze Match"):
    if uploaded_file and job_description:
        with st.spinner("Analyzing with Production AI..."):
            # 1. Extract Text
            resume_text = extract_text_from_pdf(uploaded_file)
            
            if not resume_text.strip():
                st.warning("Could not extract text from this PDF. Please ensure it is not a scanned image.")
            else:
                # 2. Construct the Prompt
                prompt = f"""
                Analyze the following Resume against the Job Description. 
                1. Give a 'Match Score' out of 100.
                2. List 3 missing keywords or skills.
                3. Suggest 1 sentence to improve the resume summary.

                Job Description: {job_description}
                Resume: {resume_text}
                """
                
                # 3. Call Gemini API (Free Tier Flash Model)
                if client:
                    try:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=prompt,
                        )
                        
                        # 4. Show Result
                        st.success("Analysis Complete!")
                        st.markdown("### **AI Feedback:**")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"API Error: {e}. Check if your API key is configured correctly.")
                else:
                    st.error("AI Client configuration failed. Please set up your GEMINI_API_KEY.")
    else:
        st.warning("Please upload a PDF and paste a Job Description first.")
