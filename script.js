async function askChatbot() {
    const question = document.getElementById("question").value;
    const responseDiv = document.getElementById("response");
    responseDiv.innerText = "Thinking...";
  
    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: question })
    });
  
    const data = await res.json();
    responseDiv.innerText = data.response || data.error || "Something went wrong.";
  }
  