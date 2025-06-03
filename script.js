let pokemonList = [];

async function fetchPokemonNames() {
  const response = await fetch("https://pokeapi.co/api/v2/pokemon?limit=1000");
  const data = await response.json();
  pokemonList = data.results.map(p => capitalizeFirst(p.name));
}

function capitalizeFirst(str) {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

function showSuggestions() {
  const input = document.getElementById("pokemon-input").value.toLowerCase();
  const suggestions = document.getElementById("suggestions");
  suggestions.innerHTML = "";

  if (!input) return;

  const matches = pokemonList.filter(name => name.toLowerCase().startsWith(input)).slice(0, 10);
  
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

function handleKey(event) {
  if (event.key === "Enter") {
    askPokemon();
    document.getElementById("suggestions").innerHTML = "";
  }
}

async function askPokemon() {
    const input = document.getElementById("pokemon-input").value.trim();
    const game = document.getElementById("game-select").value;
    const responseBox = document.getElementById("response");
    const imgBox = document.getElementById("pokemon-display");
    const img = document.getElementById("pokemon-image");
  
    if (!input) return;
  
    responseBox.textContent = "Computing...";
    const name = input.split(" ")[0].toLowerCase(); // First word is assumed to be the Pokémon
  
    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          message: input,
          game: game 
        }),
      });
      const data = await res.json();
  
      responseBox.textContent = data.response;
  
      // Try to display Pokémon image
      img.src = `https://img.pokemondb.net/artwork/${name}.jpg`;
      img.onerror = () => (imgBox.classList.add("hidden"));
      img.onload = () => imgBox.classList.remove("hidden");
    } catch (err) {
      responseBox.textContent = "Error: Could not get a response.";
      imgBox.classList.add("hidden");
    }
}

// Run this on page load
window.onload = fetchPokemonNames;