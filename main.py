from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request model
class Question(BaseModel):
    message: str

# Load profile data safely
try:
    with open("profile_data.txt", "r", encoding="utf-8") as f:
        profile_content = f.read()
except Exception:
    profile_content = "Profile data could not be loaded."

@app.get("/")
def root():
    return {"status": "Backend is running successfully"}

@app.post("/chat")
def chat(question: Question):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""
You are Keerthana Bellam's professional AI portfolio assistant.

STRICT RULES:
1. Answer ONLY using the information provided in the profile below.
2. If the question is unrelated or not found in the profile, respond with:
   "I don't have that specific information. Please contact Keerthana directly at keerthanabellam23@gmail.com or connect on LinkedIn."
3. Keep answers concise, professional, and recruiter-friendly.
4. Do not make up information.
5. If asked for contact details, provide:
   Email: keerthanabellam23@gmail.com
   LinkedIn: https://linkedin.com/in/YOUR-LINK

PROFILE DATA:
{profile_content}
"""
                },
                {
                    "role": "user",
                    "content": question.message
                }
            ],
            temperature=0.3,
        )

        return {
            "response": response.choices[0].message.content.strip()
        }

    except Exception as e:
        return {
            "response": "Sorry, I’m currently experiencing a temporary technical issue. Please try again shortly or contact Keerthana directly at keerthanabellam23@gmail.com."
        }
