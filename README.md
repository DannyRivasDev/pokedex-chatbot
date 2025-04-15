# Pokémon Chatbot Web App

This is a full-stack web application that allows users to enter the name of a Pokémon (and optionally a game version) and receive detailed information including evolution chains, locations across various Pokémon games, competitive movesets, and held items — all powered by a large language model (LLM).

---

## 🛠 Technologies Used

### 🔗 Frontend
- **HTML / CSS / JavaScript** – Simple UI for user input and response display
- **Fetch API** – For calling the backend asynchronously

### 🧠 Backend
- **FastAPI** – Python web framework to handle API routing
- **Google Generative AI API (Gemini 2.0 Flash)** – Powers natural language responses
- **Pydantic** – For request validation
- **CORS Middleware** – Enables frontend-backend communication during local development

### 🚀 Deployment
- **Frontend:** GitHub Pages  
- **Backend:** Hugging Face Spaces *(optional future step)*

---

## ⚡ Features

- Enter a Pokémon name to retrieve evolution details, locations, and optimal competitive setups
- Intelligent fallback when game version isn't specified — shows info across multiple games
- Professionally structured responses styled like a Pokédex using custom system prompts
