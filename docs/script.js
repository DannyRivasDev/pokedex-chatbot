/**
 * Pokédex Chatbot Frontend Script
 * Handles user interactions, API calls, and UI updates for the Pokédex chatbot.
 */

// Store the list of Pokémon names for autocomplete
let pokemonList = [];

/**
 * Fetches Pokémon names from the PokéAPI for autocomplete suggestions
 */
async function fetchPokemonNames() {
  const response = await fetch("https://pokeapi.co/api/v2/pokemon?limit=1000");
  const data = await response.json();
  pokemonList = data.results.map(p => capitalizeFirst(p.name));
}

/**
 * Capitalizes the first letter of a string
 * @param {string} str - The string to capitalize
 * @returns {string} The capitalized string
 */
function capitalizeFirst(str) {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

/**
 * Displays autocomplete suggestions based on user input
 */
function showSuggestions() {
  const input = document.getElementById("pokemon-input").value.toLowerCase();
  const suggestions = document.getElementById("suggestions");
  suggestions.innerHTML = "";

  if (!input) return;

  // Filter Pokémon names that start with the input text (limit to 10 results)
  const matches = pokemonList.filter(name => name.toLowerCase().startsWith(input)).slice(0, 10);
  
  // Create suggestion elements
  matches.forEach(name => {
    const div = document.createElement("div");
    div.className = "suggestion";
    div.textContent = name;
    div.onclick = () => {
      document.getElementById("pokemon-input").value = name;
      suggestions.innerHTML = "";
    };
    suggestions.appendChild(div);
  });
}

/**
 * Handles keyboard events in the input field
 * @param {KeyboardEvent} event - The keyboard event
 */
function handleKey(event) {
  if (event.key === "Enter") {
    askPokemon();
    document.getElementById("suggestions").innerHTML = "";
  }
}

// Backend API URL (Hugging Face Spaces deployment)
const backendURL = "https://dannyrivasdev-pokedex-chat-bot.hf.space/chat"; 

/**
 * Sends the user query to the backend and displays the response
 */
async function askPokemon() {
    const input = document.getElementById("pokemon-input").value.trim();
    const game = document.getElementById("game-select").value;
    const responseBox = document.getElementById("response");
    const imgBox = document.getElementById("pokemon-display");
    const img = document.getElementById("pokemon-image");
  
    if (!input) return;
  
    // Show loading state
    responseBox.textContent = "Computing...";
    
    // Extract the Pokémon name (assumed to be the first word)
    const name = input.split(" ")[0].toLowerCase();
  
    try {
      // Send request to the backend API
      const res = await fetch(backendURL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          message: input,
          game: game 
        }),
      });
      const data = await res.json();
  
      // Display the response
      responseBox.textContent = data.response;
  
      // Try to display Pokémon image from pokemondb.net
      img.src = `https://img.pokemondb.net/artwork/${name}.jpg`;
      img.onerror = () => (imgBox.classList.add("hidden"));  // Hide image if it fails to load
      img.onload = () => imgBox.classList.remove("hidden");  // Show image when loaded
    } catch (err) {
      responseBox.textContent = "Error: Could not get a response.";
      imgBox.classList.add("hidden");
    }
}

// Initialize the app when the page loads
window.onload = fetchPokemonNames;