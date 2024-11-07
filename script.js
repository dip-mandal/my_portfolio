document.getElementById("startButton").addEventListener("click", async function() {
    const responseText = await fetchResponse();
    document.getElementById("response").innerText = responseText;
});

async function fetchResponse() {
    try {
        const response = await fetch("http://dipmandal303.pythonanywhere.com/start_voice_assistant");  // Adjust to your backend server's address
        if (!response.ok) {  // Check if the response is successful (status 200-299)
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data.response;  // Assuming the JSON response contains the "response" key
    } catch (error) {
        console.error("Error fetching response:", error);
        return "Error occurred. Please try again.";
    }
}
