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
    allow_origins=["https://dannyrivasdev.github.io/"],  # frontend domain
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
    game: str = ""

@app.post("/chat")

async def chat(request: ChatRequest):
    user_input = request.message
    game = request.game.strip()

    system_prompt = f"""
        You are a helpful Pokémon expert assistant trained with information from Serebii.net and Smogon.com.

        {"The user is asking specifically about the game " + game + "." if game else "If the game is not specified, provide results across all generations."}

        Your response should include:

        📍 Location:
        - Where the Pokémon can be found in {f'the game {game}' if game else 'each major game'}
        - Include encounter rates, time of day, and biome (if available)

        🧬 Evolution:
        - Full evolution line, including methods of evolution (level, item, trade, friendship, etc.)

        ⚔️ Competitive Moveset (Smogon Gen 9 Singles):
        - Suggested nature, EV spread, ability, item, and four competitive moves
        - Use valid information from the Smogon Gen 9 OU/UU/UBers metagame

        🧠 Strategy:
        - One or two sentences describing the usage or viability of the set

        Formatting Rules:
        - DO NOT use markdown symbols like **, ###, or bullet points
        - Use line breaks and emojis for section headers (📍, 🧬, ⚔️, 🧠)
        - Output should be readable in plain HTML without needing Markdown styling
    """
    if PROVIDER == "openai":
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        return {"response": response["choices"][0]["message"]["content"]}

    elif PROVIDER == "gemini":
        convo = model.start_chat()
        convo.send_message(system_prompt)
        response = convo.send_message(request.message)
        return {"response": response.text}  

    return {"response": "LLM provider not supported."}


