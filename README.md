# 🚀 Email orchestrator

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
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)

## 💡 Inspiration
Managing loan servicing requests manually can be time-consuming and error-prone. Automating this process using NLP and machine learning enhances efficiency, accuracy, and compliance.
## ⚙️ What It Does
- Reads emails and attachments (PDF, DOCX, EML)
- Extracts main requests (e.g., Adjustments, AU Transfer, Closing Notice)
- Identifies sub-requests (e.g., reallocation fees, amendment fees, cashless adjustments)
- Supports multi-file uploads for batch processing 
- Provides confidence scores for classification

## 🛠️ How We Built It
- Backend: FastAPI for handling email classification requests
- AI Model: Hugging Face Transformers for text classification
- NLP Techniques: Named Entity Recognition (NER) and fuzzy matching for request extraction
- Frontend: React-based UI for user interaction
- File Handling: PDF, DOCX, and EML processing using PyMuPDF, python-docx, and email parser
- Infrastructure: Dockerized application for scalable deployment

## 🚧 Challenges We Faced
- Handling multiple follow-up emails and maintaining context
- Extracting text accurately from different file formats
- Ensuring high classification accuracy with limited training data
- Managing real-time processing speed for a seamless user experience

## 🏃 How to Run

### Prerequisites
- Python 3.8 or higher
- Node.js and npm
- pip (Python package manager)

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
   uvicorn model-server:app --reload
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
- 🔹 Backend: FastAPI, Hugging Face Transformers, spaCy, TensorFlow, PyMuPdf, FuzzyWuzzy, python-docx

## 👥 Team
- **Your Name** - [https://github.com/HemaPonraj05](#) | [https://www.linkedin.com/in/hemavathy-ponraj/](#)
- **Teammate 2** - [https://github.com/priti0301](#) | [https://www.linkedin.com/in/pritipreethi/](#)
