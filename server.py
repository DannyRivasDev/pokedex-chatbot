from fastapi import FastAPI, Request
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()


class ChatRequest(BaseModel):
    message: str

# @app.post("/chat")
# async def chat(request: ChatRequest):
#     return {"response": f"You said: {request.message}"}

@app.post("/chat")
async def chat(request: ChatRequest):
    # data = request.json()
    user_input = request.message

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": user_input}])

    return {"response": response.choices[0].message.content}

