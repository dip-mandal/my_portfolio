// Send message function
function sendMessage() {
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const message = userInput.value.trim();

    if (message) {
        const userMessage = document.createElement("div");
        userMessage.className = "message user";
        userMessage.innerText = message;
        chatBox.appendChild(userMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
        userInput.value = "";

        getBotResponse(message);
    }
}

// Fetch chatbot response
function getBotResponse(message) {
    const chatBox = document.getElementById("chat-box");

    fetch('https://dipmandal303.pythonanywhere.com/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
    })
    .then(response => {
        if (response.ok) {
            return response.text();
        }
        throw new Error('Error fetching bot response');
    })
    .then(data => {
        const botMessage = document.createElement("div");
        botMessage.className = "message bot";
        botMessage.innerText = data;
        chatBox.appendChild(botMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(() => {
        const errorMessage = document.createElement("div");
        errorMessage.className = "message bot error";
        errorMessage.innerText = "Sorry, there was an error with the response.";
        chatBox.appendChild(errorMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}

// Voice recognition function with animation
function startVoiceRecognition() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    const voiceAnimation = document.getElementById("voice-animation");
    const userInput = document.getElementById("user-input");

    recognition.lang = "en-US";
    voiceAnimation.style.display = "block"; // Show animation
    recognition.start();

    recognition.onresult = function (event) {
        const speechResult = event.results[0][0].transcript;
        userInput.value = speechResult;
        sendMessage();
        voiceAnimation.style.display = "none"; // Hide animation
    };

    recognition.onspeechend = function () {
        recognition.stop();
        voiceAnimation.style.display = "none"; // Hide animation
    };

    recognition.onerror = function () {
        voiceAnimation.style.display = "none"; // Hide animation
        alert("Sorry, we couldn't process your voice input.");
    };
}

// Dark mode toggle
document.getElementById("dark-mode-btn").addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
});

// Trigger sendMessage on pressing Enter
document.getElementById("user-input").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});
