# Pokédex Chat Bot 🔍🎮

A web-based Pokédex assistant that uses an LLM backend to answer questions about Pokémon locations, evolution lines, and competitive movesets — with support for specific game versions. Built with a FastAPI backend deployed on Hugging Face Spaces and a frontend hosted via GitHub Pages.

---

## 🌐 Live Demo

👉 **Try it here:** [https://dannyrivasdev.github.io/pokedex-chatbot](https://dannyrivasdev.github.io/pokedex-chatbot)

> Type a Pokémon name and optionally select a game from the dropdown to get a tailored response using information from **Serebii.net** and **Smogon.com**.

---

## 🛠 Tech Stack

### Frontend
- **HTML/CSS/JS** (Vanilla)
- Hosted via **GitHub Pages**
- Features:
  - Auto-suggestions for Pokémon names using PokéAPI
  - Dropdown to select Pokémon games
  - Embedded Pokémon artwork
  - Clean HTML formatting (no Markdown required)
  - Responsive design for mobile and desktop

### Backend
- **FastAPI** with **Pydantic** for data validation
- Deployed to **Hugging Face Spaces** using the **Docker** runtime
- LLM Provider options:
  - `OpenAI` (`gpt-3.5-turbo`)
  - `Gemini` (`gemini-2.0-flash`)
- Environment variables are stored securely using Hugging Face **Secrets**
- CORS configured for secure cross-origin requests

---

## ⚙️ How It Works

1. User types a Pokémon name and selects a game.
2. Frontend sends a POST request to the FastAPI backend with the name and game.
3. Backend uses the appropriate LLM provider to:
   - Retrieve location data from major games
   - Return the full evolution chain
   - Suggest a Smogon-optimized competitive moveset
4. Response is returned and rendered in the browser using HTML formatting.

---

## 🚀 Run Locally

### Requirements

- Python 3.10+
- Node.js (optional for frontend tweaks)

### Backend (FastAPI)

```bash
# Clone the repository
git clone https://github.com/dannyrivasdev/pokedex-chatbot.git
cd pokedex-chatbot

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp backend/.env.example backend/.env
# Edit the .env file with your API keys

# Run the FastAPI server
cd backend
uvicorn server:app --reload
```

### Environment Variables

The project uses a `.env` file in the backend directory with the following structure:

```
# Choose the LLM provider: "openai" or "gemini"
PROVIDER=gemini

# Your API keys
GEMINI_API_KEY="your_gemini_api_key_here"
OPENAI_API_KEY="your_openai_api_key_here"
```

### Frontend

Open `docs/index.html` in your browser locally, or host it using GitHub Pages by setting the GitHub Pages source to the `docs/` folder.

---

## 📦 Hugging Face Space

You can view the live backend or duplicate the space below:

🔗 [https://huggingface.co/spaces/DannyRivasDev/Pokedex-Chat-Bot](https://huggingface.co/spaces/DannyRivasDev/Pokedex-Chat-Bot)

---

## 🧠 System Prompt Design

The LLM is prompted to return:

- 📍 **Location:** where the Pokémon is found (with game, encounter rate, time of day, biome)
- 🧬 **Evolution:** full line and conditions (level/item/trade)
- ⚔️ **Competitive Moveset:** nature, EVs, ability, item, and four moves
- 🧠 **Strategy:** usage insight for competitive formats

> Output is plain text formatted for clean HTML rendering without markdown.

---

## 🔧 Project Structure

```
pokedex-chatbot/
├── backend/
│   ├── .env              # API keys (not committed)
│   ├── .env.example      # Example environment variables
│   └── server.py         # FastAPI server implementation
├── docs/                 # Frontend (GitHub Pages)
│   ├── index.html
│   ├── script.js
│   └── style.css
├── requirements.txt      # Python dependencies
└── README.md
```

---

## 🧠 Credits

- [Serebii.net](https://serebii.net) - Comprehensive Pokémon data
- [Smogon](https://www.smogon.com) - Competitive Pokémon strategies
- [PokéAPI](https://pokeapi.co/) - Pokémon data API
- [Hugging Face](https://huggingface.co/) - Backend hosting
- [OpenAI](https://openai.com/) / [Gemini](https://ai.google.dev/) - LLM providers

---

## 📜 License

MIT License. Free to use, remix, and improve!