# 🚀 Email Classification Orchestrator

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
This project is an AI-powered email classification system designed for loan servicing use cases. It processes emails and their attachments to extract key requests and sub-requests, helping financial institutions streamline their workflow.
## 🎥 Demo
📹 [Video Demo]:[https://github.com/ewfx/gaied-code-witches/tree/main/artifacts/demo]

🖼️ [Screenshots]:[https://github.com/ewfx/gaied-code-witches/tree/main/artifacts/demo](#-demo)

## 💡 Inspiration
Loan servicing teams receive a high volume of emails containing critical requests such as adjustments, AU transfers, closing notices, and commitment changes. Manual processing is time-consuming and prone to errors. This solution streamlines the workflow by automatically classifying emails and extracting key details.
## ⚙️ What It Does
- Reads Emails & Attachments: Supports .eml, .pdf, and .docx files.
- Identifies Request Types: Detects loan-related requests like AU transfers, reallocation fees, amendment fees, principal adjustments, and more.
- Understands Context: Extracts intent from multiple follow-up emails in a conversation thread.
- Provides Structured Output: Returns a categorized summary of the email content.

## 🛠️ How We Built It
- Backend: FastAPI-based Python server for processing email content and classifying intent.
- AI Model: Uses Google's Gemini API for text classification.
- Frontend: React-based web application for uploading emails and viewing classification results.
- Document Parsing: Uses PyMuPDF for PDFs, python-docx for .docx files, and email.parser for .eml files.

## 🚧 Challenges We Faced
- Email Parsing Complexity: Handling various email formats and extracting meaningful text.
- Context Retention: Ensuring that follow-up emails are correctly associated with the main request.
- API Limitations: Managing quotas and optimizing API calls for cost efficiency.

## 🏃 How to Run

### Prerequisites
- Python 3.8 or higher
- Node.js and npm
- pip (Python package manager)

### Environment Variables
Create a `.env` file and add your Google API key:
```plaintext
GOOGLE_API_KEY=your_api_key_here
```

### Generating a New API Key
If your API key expires or needs updating:
1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Click **"Create Credentials"** → **"API Key"**
3. Copy the new API key
4. Update the `.env` file
5. Restart the service

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/gaied-code-witches.git
   ```
   ```sh 
   cd gaied-code-witches/code/src/email-classifier-service
   ```
2. Create a virtual environment and activate it
   ```sh 
   python -m venv venv 
   ```
   ```shell
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies
   ```shell
   pip install -r requirements.txt
   ```
4. Download the spaCy model
   ```shell
   python -m spacy download en_core_web_sm
   ```
5. Run the FastAPI server
   ```shell
   uvicorn genai-model-server:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ``` bash
   cd ../email-classifier-web
   ```
2. Install dependencies:
   ```bash 
   npm install
   ```
3. Start the development server:
   ``` bash 
   npm start
   ```

### Usage
1. Open the frontend in your browser at http://localhost:3000.
2. Drag and drop files (PDF, DOCX, EML) or click to upload.
3. Click Upload and Classify to process the files.
4. View the classification results, including:
   - Filename.
   - Main request.
   - Sub-requests.
   - Confidence score.

## 🏗️ Tech Stack
- 🔹 Frontend: React , Axios
- 🔹 AI Model: Gemini API
- 🔹 Backend: FastAPI, Hugging Face Transformers, spaCy, TensorFlow, PyMuPdf, FuzzyWuzzy, python-docx

## 👥 Team
- **Your Name** - [https://github.com/HemaPonraj05](#) | [https://www.linkedin.com/in/hemavathy-ponraj/](#)
- **Teammate 2** - [https://github.com/priti0301](#) | [https://www.linkedin.com/in/pritipreethi/](#)
