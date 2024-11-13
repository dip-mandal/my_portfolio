// Function to send the user's message to the backend
function sendMessage() {
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const message = userInput.value.trim();

    if (message) {
        // Display the user's message in the chat box
        const userMessage = document.createElement("div");
        userMessage.className = "message user";
        userMessage.innerText = message;
        chatBox.appendChild(userMessage);

        // Scroll to the bottom of the chat
        chatBox.scrollTop = chatBox.scrollHeight;

        // Clear the input field
        userInput.value = "";

        // Call getBotResponse to get the bot's response from the backend
        getBotResponse(message);
    }
}

// Function to fetch the bot's response from the backend
function getBotResponse(message) {
    const chatBox = document.getElementById("chat-box");

    fetch('https://dipmandal303.pythonanywhere.com/', {  // Updated to root URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })  // Send the message to the backend
    })
    .then(response => {
        // Check if the response is ok (status 200)
        if (response.ok) {
            return response.text();  // Return the response as plain text
        } else {
            throw new Error('Network response was not ok');
        }
    })
    .then(data => {
        // Display the bot's response in the chat box
        const botMessage = document.createElement("div");
        botMessage.className = "message bot";
        botMessage.innerText = data;  // Set the response as the bot's message
        chatBox.appendChild(botMessage);

        // Scroll to the bottom of the chat
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
        
        // Display an error message if something goes wrong
        const errorMessage = document.createElement("div");
        errorMessage.className = "message bot error";
        errorMessage.innerText = "Sorry, there was an error with the response.";
        chatBox.appendChild(errorMessage);

        // Scroll to the bottom of the chat
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}
