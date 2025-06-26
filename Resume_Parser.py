import streamlit as st
import pdfplumber
import docx
import re
import os
from datetime import datetime
import google.generativeai as genai

# Configure Gemini API with direct API key
genai.configure(api_key="AIzaSyBxjbsU0fKL0Bv-wW2c_Rj4V4TF2N2OOiI")

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')


# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text


# Function to extract text from DOCX
def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])


# Function to extract text from uploaded file
def extract_text(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(uploaded_file)
    else:
        return uploaded_file.getvalue().decode("utf-8")


# Function to get AI response from Gemini
def get_ai_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"


# Function to analyze resume and job description
def analyze_resume_job(resume_text, job_desc_text):
    # Job Match Score analysis
    match_prompt = f"""
    Analyze this resume and job description to provide:
    1. A Job Match Score out of 100 based on skills, experience, and qualifications
    2. Top 5 missing or weak keywords/skills from the resume compared to the job description

    Resume:
    {resume_text}

    Job Description:
    {job_desc_text}

    Provide the output in this exact format:
    Match Score: [score]/100
    Missing/Weak Skills:
    1. [skill 1]
    2. [skill 2]
    3. [skill 3]
    4. [skill 4]
    5. [skill 5]
    """
    match_analysis = get_ai_response(match_prompt)

    # ATS Scoring analysis
    ats_prompt = f"""
    Analyze this resume for Applicant Tracking System (ATS) compatibility:
    1. Provide an ATS Compatibility Score out of 100
    2. List any formatting issues or risks that might affect ATS parsing

    Resume:
    {resume_text}

    Provide the output in this exact format:
    ATS Score: [score]/100
    Formatting Issues:
    - [issue 1]
    - [issue 2]
    - [issue 3]
    """
    ats_analysis = get_ai_response(ats_prompt)

    # AI Rewriting Suggestions
    rewrite_prompt = f"""
    Provide suggestions to improve this resume:
    1. Suggestions for better action verbs, metrics, and clarity
    2. Rewrite 2-3 bullet points to demonstrate impact

    Resume:
    {resume_text}

    Provide the output in this exact format:
    Improvement Suggestions:
    - [suggestion 1]
    - [suggestion 2]

    Rewritten Bullet Points:
    1. [original bullet] → [improved bullet]
    2. [original bullet] → [improved bullet]
    """
    rewrite_analysis = get_ai_response(rewrite_prompt)

    # Career Path Optimization
    career_prompt = f"""
    Based on this resume and job description, provide career optimization advice:
    1. Suggested certifications or courses to bridge gaps
    2. Alternate nearby job titles to consider
    3. Long-term growth competencies to develop

    Resume:
    {resume_text}

    Job Description:
    {job_desc_text}

    Provide the output in this exact format:
    Certifications/Courses:
    - [cert 1]
    - [cert 2]

    Alternate Job Titles:
    - [title 1]
    - [title 2]

    Growth Competencies:
    - [competency 1]
    - [competency 2]
    """
    career_analysis = get_ai_response(career_prompt)

    # Resume Refactoring
    refactor_prompt = f"""
    Refactor this resume to be ATS-optimized:
    1. Remove tables, columns, icons
    2. Clean and rewrite the text while preserving all important information

    Resume:
    {resume_text}

    Provide ONLY the cleaned resume text, no additional commentary.
    """
    refactored_resume = get_ai_response(refactor_prompt)

    return {
        "match_analysis": match_analysis,
        "ats_analysis": ats_analysis,
        "rewrite_analysis": rewrite_analysis,
        "career_analysis": career_analysis,
        "refactored_resume": refactored_resume
    }


# Streamlit UI
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("📄 AI-Powered Resume & Job Description Analyzer")
st.markdown("""
Upload your resume and a job description to get:
- Job match score and missing skills
- ATS compatibility analysis
- AI-powered improvement suggestions
- Career optimization advice
- ATS-optimized resume refactoring
""")

# File upload section
col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx", "txt"])
with col2:
    job_desc_file = st.file_uploader("Upload Job Description", type=["pdf", "docx", "txt"])

if st.button("Analyze"):
    if resume_file and job_desc_file:
        with st.spinner("Analyzing your documents..."):
            # Extract text from files
            resume_text = extract_text(resume_file)
            job_desc_text = extract_text(job_desc_file)

            # Analyze the documents
            analysis_results = analyze_resume_job(resume_text, job_desc_text)

            # Display results in tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📊 Job Match Score",
                "🤖 ATS Scoring",
                "🛠️ Rewriting Suggestions",
                "🎯 Career Path",
                "📄 Refactored Resume"
            ])

            with tab1:
                st.subheader("Job Match Analysis")
                st.markdown(f"```\n{analysis_results['match_analysis']}\n```")

            with tab2:
                st.subheader("ATS Compatibility Analysis")
                st.markdown(f"```\n{analysis_results['ats_analysis']}\n```")

            with tab3:
                st.subheader("Resume Improvement Suggestions")
                st.markdown(f"```\n{analysis_results['rewrite_analysis']}\n```")

            with tab4:
                st.subheader("Career Path Optimization")
                st.markdown(f"```\n{analysis_results['career_analysis']}\n```")

            with tab5:
                st.subheader("ATS-Optimized Resume")
                st.download_button(
                    label="Download Refactored Resume",
                    data=analysis_results['refactored_resume'],
                    file_name=f"refactored_resume_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
                st.text_area("Refactored Resume Text",
                             analysis_results['refactored_resume'],
                             height=500)
    else:
        st.warning("Please upload both resume and job description files.")

# Add footer
st.markdown("---")
st.markdown("Built with 🚀 using Streamlit and Gemini AI")