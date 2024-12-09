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

function getBotResponse(message) {
    const chatBox = document.getElementById("chat-box");

    fetch('https://dipmandal303.pythonanywhere.com/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
    })
    .then(response => response.ok ? response.text() : Promise.reject('Error'))
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

document.getElementById("user-input").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});
