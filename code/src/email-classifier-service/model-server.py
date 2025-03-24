from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
from dotenv import load_dotenv
from transformers import pipeline


# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Allowing all origins for testing purposes, restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Hugging Face model for text classification
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

class EmailRequest(BaseModel):
    email_text: str

@app.post("/classify")
async def classify_email(request: EmailRequest):
    try:
        result = classifier(request.email_text)
        classification = result[0]['label']  # Extract the label
        score = result[0]['score']  # Extract the confidence score
        return {"classification": classification, "confidence_score": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#Unable to use openai due to quota issues

# set your OpenAI API key as an environment variable

# class EmailRequest(BaseModel):
#     email_text: str

# @app.post("/classify")
# async def classify_email(request: EmailRequest):
#     try:
#         response = client.chat.completions.create(model="gpt-3.5-turbo",  # You can use "gpt-3.5-turbo" if GPT-4 is unavailable
#         messages=[
#             {"role": "system", "content": "You are an email classification assistant."},
#             {"role": "user", "content": request.email_text}
#         ])
#         classification = response.choices[0].message.content
#         return {"classification": classification}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
