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
    user_message = question.message.lower()

    # Handle greetings naturally
    greetings = ["hi", "hello", "hey", "how are you", "good morning"]

    if any(greet in user_message for greet in greetings):
        return {
            "response": "Hey 👋 I'm doing great! You can ask me about Keerthana’s experience, projects, or skills."
        }

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""
You are Keerthana's professional AI assistant.

Answer questions using her profile information below.
If the question is outside her resume, politely redirect to contact her.

PROFILE:
{profile_content}
"""
                },
                {
                    "role": "user",
                    "content": question.message
                }
            ],
            temperature=0.6,
        )

        return {
            "response": response.choices[0].message.content
        }

    except:
        return {
            "response": "⚠️ AI service temporarily unavailable."
        }
