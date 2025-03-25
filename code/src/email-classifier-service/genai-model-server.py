from fastapi import FastAPI, HTTPException, UploadFile, File
import google.generativeai as genai
import os
from dotenv import load_dotenv
import io
import json
from docx import Document
import fitz  # PyMuPDF
from email.parser import BytesParser
from email import policy

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY. Set it in your environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

def extract_text_from_docx(file_bytes):
    file_stream = io.BytesIO(file_bytes)
    doc = Document(file_stream)
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])

def extract_text_from_pdf(file_bytes):
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_eml(file_bytes):
    msg = BytesParser(policy=policy.default).parsebytes(file_bytes)
    text = ""

    if msg.is_multipart():
        for part in msg.iter_parts():
            if part.get_content_type() == "text/plain":
                text += part.get_content()
    else:
        text = msg.get_payload()

    return text.strip()

def classify_email_gemini(text):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        
        prompt = f"""
        Classify the following email based on its intent. Provide structured JSON output with:
        - classification (main category)
        - sub_requests (list of subcategories)
        - confidence_score (0-1 scale)

        Email Content:
        {text}

        Return JSON only.
        """

        response = model.generate_content(prompt)

        if hasattr(response, "candidates") and response.candidates:
            result_text = response.candidates[0].content.parts[0].text.strip()
        else:
            result_text = "{}"

        # Ensure valid JSON
        try:
            result_json = json.loads(result_text)
        except json.JSONDecodeError:
            result_json = {"classification": "Unknown", "sub_requests": [], "confidence_score": 0.0}

        return result_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error with Gemini API: {str(e)}")

app = FastAPI()

@app.post("/classify")
async def classify_emails(files: list[UploadFile] = File(...)):
    results = []
    for file in files:
        file_content = await file.read()
        
        if file.filename.endswith(".pdf"):
            email_text = extract_text_from_pdf(file_content)
        elif file.filename.endswith(".docx"):
            email_text = extract_text_from_docx(file_content)
        elif file.filename.endswith(".eml"):
            email_text = extract_text_from_eml(file_content)
        else:
            results.append({"filename": file.filename, "error": "Unsupported file type."})
            continue
        
        classification = classify_email_gemini(email_text)
        results.append({"filename": file.filename, **classification})
    
    return results
