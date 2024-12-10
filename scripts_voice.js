const toggleButton = document.getElementById("toggleButton");
const responseDisplay = document.getElementById("response");
const animationDiv = document.getElementById("animation");
let isRunning = false;

// Dark mode toggle functionality
const modeToggle = document.getElementById('modeToggle');
const body = document.body;

modeToggle.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    modeToggle.textContent = body.classList.contains('dark-mode') 
        ? 'Switch to Light Mode' 
        : 'Switch to Dark Mode';
});

// Event listener for the toggle button to start/stop the assistant
toggleButton.addEventListener("click", async function () {
    toggleButton.disabled = true; // Disable button during processing
    if (isRunning) {
        await stopAssistant();
    } else {
        await startAssistant();
    }
    toggleButton.disabled = false; // Re-enable button after processing
});

async function startAssistant() {
    isRunning = true;
    toggleButton.classList.add("running");
    toggleButton.innerText = "Stop Voice Assistant";
    responseDisplay.innerText = "Status: Running...";
    animationDiv.classList.add("active"); // Start animation
    
    try {
        const response = await fetch("http://127.0.0.1:5000/start_voice_assistant");
        if (!response.ok) throw new Error("Running...");

        const data = await response.json();
        console.log("Backend response:", data);  // Log the response to check its structure

        if (data && data.message) {
            responseDisplay.innerText = "Response: " + data.message;
        } else {
            responseDisplay.innerText = "Unexpected response format";
        }
    } catch (error) {
        console.error("Running...:", error);
        responseDisplay.innerText = "Running...";
        animationDiv.classList.remove("active"); // Stop animation on error
    }
}

async function stopAssistant() {
    isRunning = false;
    toggleButton.classList.remove("running");
    toggleButton.innerText = "Start Voice Assistant";
    responseDisplay.innerText = "Status: Stopped";
    animationDiv.classList.remove("active"); // Stop animation
    
    try {
        const response = await fetch("http://127.0.0.1:5000/stop_voice_assistant");
        if (!response.ok) throw new Error("Not Running!!!");

        const data = await response.json();
        console.log("Backend response:", data);  // Log the response to check its structure

        if (data && data.message) {
            responseDisplay.innerText = "Response: " + data.message;
        } else {
            responseDisplay.innerText = "Unexpected response format";
        }
    } catch (error) {
        console.error("Not Running!!!:", error);
        responseDisplay.innerText = "Not Running!!!";
    }
}
