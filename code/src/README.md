# Email Classifier Service

This project provides an **Email Classification Service** that processes uploaded files (e.g., PDFs, DOCX, EML) and classifies them into categories using machine learning models. It includes a backend API built with **FastAPI** and a frontend built with **React** for user interaction.

---

## Features

### Backend (FastAPI)
- Accepts multiple file uploads (PDF, DOCX, EML).
- Extracts text from uploaded files using:
  - **PyMuPDF** for PDFs.
  - **python-docx** for DOCX files.
  - **email.parser** for EML files.
- Classifies extracted text using:
  - **Hugging Face Transformers** for text classification.
  - **spaCy** for NLP tasks.
  - **FuzzyWuzzy** for matching requests and sub-requests.
- Supports environment variable configuration using **python-dotenv**.

### Frontend (React)
- Drag-and-drop file upload functionality.
- Displays classification results, including:
  - Filename.
  - Main request.
  - Sub-requests.
  - Confidence score (as a percentage).
- Allows clearing file selections and results.

---

## Installation

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
   cd gaied-code-witches/code/src/email-classifier-service
2. Create a virtual environment and activate it
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies
    pip install -r requirements.txt
4. Download the spaCy model
    python -m spacy download en_core_web_sm
5. Run the FastAPI server
    uvicorn genai-model-server:app --reload

### Frontend Setup
1. Navigate to the frontend directory:
    cd ../email-classifier-web
2. Install dependencies:
    npm install
3. Start the development server:
    npm start

### Usage
1. Open the frontend in your browser at http://localhost:3000.
2. Drag and drop files (PDF, DOCX, EML) or click to upload.
3. Click Upload and Classify to process the files.
4. View the classification results, including:
    - Filename.
    - Main request.
    - Sub-requests.
    - Confidence score.

## File Structure

### Backend

email-classifier-service
- model-server.py       # FastAPI backend for file processing and classification
- requirements.txt      # Python dependencies
- .env                  # Environment variables

### Frontend

email-classifier-web
- src/
  - App.js            # Main React component
  - App.css           # Styling for the frontend
  - index.js          # React entry point

