document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("chat-form");
  const messageArea = document.getElementById("message-area");
  const userInput = document.getElementById("user-input");
  const toggleThemeButton = document.getElementById("toggle-theme");
  const changeBackgroundButton = document.getElementById("change-background");

  let darkMode = false;
  let backgrounds = ["#e5ddd5", "#f0f0f0", "#cce5ff", "#d4edda"];
  let currentBackground = 0;

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    const messageText = userInput.value.trim();

    if (messageText === "") {
      return;
    }

    appendMessage(messageText, "sent");
    userInput.value = "";

    fetch("/get_meaning", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: messageText }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.response) {
          const { meaning, synonyms, antonyms } = data.response;
          const responseMessage = `
                    Meaning: ${meaning}<br>
                    Synonyms: ${synonyms}<br>
                    Antonyms: ${antonyms}
                `;
          appendMessage(responseMessage, "received");
        } else if (data.error) {
          appendMessage(data.error, "received");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        appendMessage("An error occurred. Please try again.", "received");
      });
  });

  toggleThemeButton.addEventListener("click", function () {
    darkMode = !darkMode;
    document.body.classList.toggle("dark-mode", darkMode);
    toggleThemeButton.textContent = darkMode ? "Light Mode" : "Dark Mode";
  });

  changeBackgroundButton.addEventListener("click", function () {
    currentBackground = (currentBackground + 1) % backgrounds.length;
    document.querySelector(".chat-box").style.backgroundColor =
      backgrounds[currentBackground];
  });

  function appendMessage(text, type) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", type);
    messageDiv.innerHTML = `<p>${text}</p>`;
    messageArea.appendChild(messageDiv);
    messageArea.scrollTop = messageArea.scrollHeight; // Auto-scroll to the bottom
  }
});
