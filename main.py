from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load profile data
with open("profile_data.txt", "r") as f:
    profile_info = f.read()

class Question(BaseModel):
    message: str

@app.post("/chat")
def chat(question: Question):
    prompt = f"""
    You are the AI assistant for Keerthana Bellam's portfolio.

    Only answer using the information below.
    If unknown, respond exactly with:

    "I don't have that information yet.
    You can contact Keerthana at:
    Email: keerthanabellam23@gmail.com
    LinkedIn: https://linkedin.com/in/YOUR-LINK"

    Information:
    {profile_info}

    Question:
    {question.message}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"reply": response.choices[0].message.content}
