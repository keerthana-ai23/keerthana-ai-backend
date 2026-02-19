from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# ✅ ADD CORS (THIS FIXES NETLIFY ERROR)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For now allow all (safe for portfolio)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Question(BaseModel):
    message: str

# Load profile data
with open("profile_data.txt", "r", encoding="utf-8") as f:
    profile_content = f.read()

@app.get("/")
def root():
    return {"status": "Backend is running"}

@app.post("/chat")
def chat(question: Question):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"You are an AI assistant that answers questions based only on this profile:\n\n{profile_content}"
                },
                {
                    "role": "user",
                    "content": question.message
                }
            ],
            temperature=0.5,
        )

        return {
            "response": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "response": f"Error: {str(e)}"
        }
