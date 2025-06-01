function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

function handleKey(event) {
    if (event.key === "Enter") {
      askPokemon();
    }
}

async function askPokemon() {
    const input = document.getElementById("pokemon-input").value.trim();
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
        body: JSON.stringify({ message: input }),
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
