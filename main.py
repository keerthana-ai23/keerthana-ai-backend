from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

# 🔐 CORS — allow your Netlify frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hilarious-alpaca-bc6ce0.netlify.app",  # ← replace if your domain changed
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Question(BaseModel):
    message: str

# 📄 Load profile data
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
                    "content": f"""
You are Keerthana's professional AI assistant.
Answer ONLY using the information below.
If the question is unrelated, respond:
"I don’t have that specific information. Please contact Keerthana directly."

PROFILE:
{profile_content}
"""
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
            "response": "⚠️ The AI service is temporarily unavailable. Please try again."
        }
