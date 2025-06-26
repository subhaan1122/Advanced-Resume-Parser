## 🧠 Project Title: Resume Parser AI using Gemini & Streamlit

**📌 Overview**

This project is an intelligent resume parsing web application built with Streamlit and powered by Google Gemini Pro (Generative AI).
It enables users to upload resumes (PDF/DOCX), automatically extracts structured information (skills, education, experience, etc.), and provides insights using conversational AI.

## 🚀 Features

- 📄 Uploads and processes resumes in PDF or DOCX format
- 🤖 Uses Gemini Pro to extract and summarize candidate information
- 💬 Provides a chat-like interface to analyze and discuss resume content
- 🌐 Lightweight, interactive Streamlit UI
- 📅 Extracts metadata like date, education, skills, experience

## 🧠 Tech Stack

**Frontend** : Streamlit
**Backend** : Python, Gemini Pro (via Google Generative AI API)
**Parsing Libraries** : pdfplumber, python-docx
**Other** : Regular Expressions, datetime, OS

## 🧪 How it Works

- 📤 User uploads a resume (PDF/DOCX)
- 📃 The app reads and extracts text using pdfplumber or python-docx
- 🧠 The extracted content is sent to Google Gemini Pro API
- 🧾 Gemini returns a structured summary of the resume (skills, education, etc.)
-  🗨️ The app displays results in a friendly, interactive format

## 🧪 Sample Output

**Resume Summary**:

- 👩 Name: [Extracted from resume]
- 💼 Skills: Python, Data Science, SQL, Excel
- 🎓 Education: BS in Computer Science
- 🏢 Experience: 2 years in software development

## 📦 Installation & Usage

# Step 1: Clone the repo
git clone https://github.com/your-username/resume-parser-ai.git
cd resume-parser-ai

# Step 2: Install requirements
pip install -r requirements.txt

# Step 3: Run the Streamlit app
streamlit run Resume_Parser.py

**🔐 API Key Setup**

- To use Gemini API:
  
1- Get API key from Google AI Studio
2- Replace the key in the Resume_Parser.py file:  genai.configure(api_key="your-key-here")



