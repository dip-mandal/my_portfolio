document.getElementById("startButton").addEventListener("click", async function() {
    const responseText = await fetchResponse();
    document.getElementById("response").innerText = responseText;
});

async function fetchResponse() {
    try {
        const response = await fetch("http://127.0.0.1:5000/start_voice_assistant");  // Adjust to your backend server's address
        const data = await response.json();
        return data.response;  // Assuming the JSON response contains "response" key
    } catch (error) {
        console.error("Error fetching response:", error);
        return "Error occurred. Please try again.";
    }
}
