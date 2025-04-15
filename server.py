from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("PROVIDER")

app = FastAPI()

if PROVIDER == "openai":
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")

elif PROVIDER == "gemini":
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")

async def chat(request: ChatRequest):
    user_input = request.message

    if PROVIDER == "openai":
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        return {"response": response["choices"][0]["message"]["content"]}

    elif PROVIDER == "gemini":
        response = model.generate_content(user_input)
        return {"response": response.text}  

    return {"response": "LLM provider not supported."}


