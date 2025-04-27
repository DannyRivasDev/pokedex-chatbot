from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("PROVIDER")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if PROVIDER == "openai":
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")

elif PROVIDER == "gemini":
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")

class ChatRequest(BaseModel):
    message: str

# System prompt
system_prompt = """
You are a helpful Pokémon expert assistant trained with information from Serebii.net and Smogon.com.

When a user gives you a Pokémon name (with or without the game), return the following:

1. Locations where the Pokémon can be found in every mainline Pokémon game, including encounter rate percentage, and time of day if applicalbe.
2. The evolution line.
3. The best competitive moveset (based on Smogon) including held items, nature, and EV spread.
4. If the game is not specified, show locations for all major games.
5. Keep your response clear, accurate, and well-structured with headings and bullet points.

Assume all questions are from a Pokémon fan or competitive player. Be concise but complete.
"""

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
        convo = model.start_chat()
        convo.send_message(system_prompt)
        response = convo.send_message(request.message)
        return {"response": response.text}  

    return {"response": "LLM provider not supported."}


