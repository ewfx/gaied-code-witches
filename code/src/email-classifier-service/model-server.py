from fastapi import FastAPI, HTTPException, UploadFile, File, Request, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from docx import Document
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
import email
from email.parser import BytesParser
from email import policy
from email.policy import default
import uvicorn
import tensorflow as tf
from transformers import pipeline

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Initialize Hugging Face model for text classification
classifier = None  # Declare classifier at the module level

try:
    print("Loading model...")
    classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
    if classifier:
        print("✅ Model loaded successfully.")
        print(f"Classifier Type: {type(classifier)}")  # Verifying classifier type
except Exception as e:
    print(f"❌ Error loading model: {e}")


# Allowing all origins for testing purposes, restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test if TensorFlow is properly installed and usable
print(f"TensorFlow version: {tf.__version__}")
print(f"Is GPU available: {tf.config.list_physical_devices('GPU')}")


def extract_text_from_docx(file):
    try:
        doc = Document(file)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        raise ValueError(f"Error processing DOCX file: {e}")


def extract_text_from_pdf(file):
    try:
        text = ""
        with fitz.open(stream=file, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        raise ValueError(f"Error processing PDF file: {e}")


def extract_text_from_eml(file):
    try:
        msg = BytesParser(policy=policy.default).parsebytes(file)
        text = ""
        if msg.is_multipart():
            for part in msg.iter_parts():
                if part.get_content_type() == "text/plain":
                    text += part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
            text = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        return text
    except Exception as e:
        raise ValueError(f"Error processing EML file: {e}")



def shutdown_server():
    """
    Gracefully shutdown the server.
    """
    uvicorn_server = uvicorn.Server(uvicorn.Config(app))
    uvicorn_server.should_exit = True


@app.post("/classify")
async def classify_email(file: UploadFile = File(...)):
    global classifier  # Ensure we're accessing the global classifier variable
    try:
        if classifier is None:
            raise HTTPException(status_code=500, detail="Classifier model not loaded.")

        file_content = await file.read()
        
        if file.filename.endswith(".pdf"):
            email_text = extract_text_from_pdf(file_content)
        elif file.filename.endswith(".docx"):
            email_text = extract_text_from_docx(file_content)
        elif file.filename.endswith(".eml"):
            email_text = extract_text_from_eml(file_content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type.")

        if not email_text.strip():
            raise HTTPException(status_code=400, detail="Extracted text is empty or invalid.")
        
        # Debugging logs
        print(f"Extracted Text (First 500 chars): {email_text[:500]}")
        
        result = classifier(email_text)
        classification = result[0]['label']
        score = result[0]['score']

        return {"classification": classification, "confidence_score": score}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))



