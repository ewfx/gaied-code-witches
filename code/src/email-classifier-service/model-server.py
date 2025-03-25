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
import spacy
from fuzzywuzzy import process
import io
from docx import Document
from typing import List, Dict

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Load spaCy's English NLP model
nlp = spacy.load("en_core_web_sm")

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

MAIN_REQUESTS = ["Adjustments", "AU transfer", "Closing Notice", "Commitment Change"]

# Define possible sub-requests
SUB_REQUESTS = [
    "reallocation fees", "amendment fees", "reallocation principal",
    "cashless", "increase", "decrease", "principal", "interest"
]

def extract_text_from_docx(file_bytes):
    try:
        file_stream = io.BytesIO(file_bytes)  # Convert bytes to file-like object
        doc = Document(file_stream)
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

def extract_main_request(text):
    """Extract main request using simple keyword matching."""
    for req in MAIN_REQUESTS:
        if req.lower() in text.lower():
            return req
    return None


def extract_sub_requests(text):
    """Extract sub-requests using NLP and fuzzy matching."""
    doc = nlp(text)
    found_sub_requests = set()

    # First, check exact keyword match
    for sub_req in SUB_REQUESTS:
        if sub_req.lower() in text.lower():
            found_sub_requests.add(sub_req)

    # Then, use NLP + fuzzy matching
    for token in doc:
        match, score = process.extractOne(token.text, SUB_REQUESTS)
        if score > 85 and match not in found_sub_requests:  # Avoid duplicates
            found_sub_requests.add(match)

    return list(found_sub_requests)


def extract_loan_requests(text):
    """Extract both main request and sub-requests from email text."""
    main_request = extract_main_request(text)
    sub_requests = extract_sub_requests(text)
    return main_request, sub_requests

def classify_text(text):
    """Classify email text into main request and sub-requests"""
    if not classifier:
        raise ValueError("Classifier model not loaded.")

    # Run classification model
    result = classifier(text)
    main_request = next((req for req in MAIN_REQUESTS if req.lower() in text.lower()), "Unknown")
    sub_requests = [sub for sub in SUB_REQUESTS if sub.lower() in text.lower()]
    
    return {
        "main_request": main_request,
        "sub_requests": sub_requests,
        "confidence_score": result[0]['score']
    }

def shutdown_server():
    """
    Gracefully shutdown the server.
    """
    uvicorn_server = uvicorn.Server(uvicorn.Config(app))
    uvicorn_server.should_exit = True

@app.post("/classify")
async def classify_emails(files: list[UploadFile] = File(...)):
    results = []

    try:
        for file in files:
            file_content = await file.read()
            
            # Extract text from different file types
            if file.filename.endswith(".pdf"):
                email_text = extract_text_from_pdf(file_content)
            elif file.filename.endswith(".docx"):
                email_text = extract_text_from_docx(file_content)
            elif file.filename.endswith(".eml"):
                email_text = extract_text_from_eml(file_content)
            else:
                results.append({
                    "filename": file.filename,
                    "error": "Unsupported file type."
                })
                continue

            # Extract main request and sub-requests
            main_request, sub_requests = extract_loan_requests(email_text)

            # Run classification using the model
            result = classifier(email_text)
            classification = result[0]['label']
            confidence_score = result[0]['score']

            # Append result for this file
            results.append({
                "filename": file.filename,
                "classification": classification,
                "confidence_score": confidence_score,
                "main_request": main_request,
                "sub_requests": sub_requests
            })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return results

        
        
    



