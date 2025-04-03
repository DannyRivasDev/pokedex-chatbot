from fastapi import FastAPI, Request
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/chat")
async def chat(request: Request):
    data = request.json()
    user_input = data.get("message")

    response = open.openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_input}]
    )

    return {"response": response["choices"][0]["message"]["content"]}