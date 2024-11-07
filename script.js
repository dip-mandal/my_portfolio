document.getElementById("startButton").addEventListener("click", async function() {
    const responseText = await fetchResponse();
    document.getElementById("response").innerText = responseText;
});

async function fetchResponse() {
    try {
        const response = await fetch("https://dipmandal303.pythonanywhere.com");  // Adjust to your backend server's address
        const data = await response.json();
        return data.response;  // Assuming the JSON response contains "response" key
    } catch (error) {
        console.error("Error fetching response:", error);
        return "Error occurred. Please try again.";
    }
}
