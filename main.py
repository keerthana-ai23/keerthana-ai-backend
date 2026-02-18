from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# Load profile data safely
try:
    with open("profile_data.txt", "r", encoding="utf-8") as f:
        profile_data = f.read()
except Exception:
    profile_data = "Profile data not available."

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=30.0
)

# Request model
class Question(BaseModel):
    message: str


@app.post("/chat")
async def chat(question: Question):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""
You are Keerthana's professional AI assistant.

Answer questions ONLY using the information below.
If the question is unrelated or not found in the profile,
say: "I don't have that information. Please contact Keerthana directly at keerthanabellam23@gmail.com or via LinkedIn."

Profile Information:
{profile_data}
"""
                },
                {
                    "role": "user",
                    "content": question.message
                }
            ]
        )

        return {
            "response": response.choices[0].message.content
        }

    except Exception:
        return {
            "response": "Temporary AI connection issue. Please try again in a few seconds."
        }


