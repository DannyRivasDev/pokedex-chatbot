"""
Pokédex Chatbot FastAPI Backend
This server handles requests from the frontend, processes them using an LLM (OpenAI or Gemini),
and returns formatted Pokémon information.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the LLM provider from environment variables
PROVIDER = os.getenv("PROVIDER")

# Initialize FastAPI app
app = FastAPI()

# Configure CORS to allow requests from the frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dannyrivasdev.github.io/"],  # frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the appropriate LLM client based on the provider
if PROVIDER == "openai":
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")

elif PROVIDER == "gemini":
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# Define the request model for chat endpoint
class ChatRequest(BaseModel):
    message: str  # The Pokémon name or query
    game: str = ""  # Optional game version, empty string means all games

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Process a chat request about a Pokémon.
    
    Args:
        request: ChatRequest object containing the message and optional game version
        
    Returns:
        JSON response with the LLM-generated information about the Pokémon
    """
    user_input = request.message
    game = request.game.strip()

    # Construct the system prompt with conditional formatting based on game selection
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
    
    # Use the appropriate LLM provider to generate a response
    if PROVIDER == "openai":
        # Call OpenAI API with the system prompt and user input
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        return {"response": response["choices"][0]["message"]["content"]}

    elif PROVIDER == "gemini":
        # Use Gemini API to generate a response
        convo = model.start_chat()
        convo.send_message(system_prompt)  # Set the system prompt
        response = convo.send_message(request.message)  # Send the user's message
        return {"response": response.text}  

    # Fallback response if no valid provider is configured
    return {"response": "LLM provider not supported."}
