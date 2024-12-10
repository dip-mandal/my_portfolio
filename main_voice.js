const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let pythonProcess;

// Function to create the main Electron window
function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'), // Optional, if you use preload scripts
            nodeIntegration: true, // Allows integration with Node.js
            contextIsolation: false, // To use Electron with Node modules
        },
    });

    // Load your app's main HTML file
    mainWindow.loadFile('index_ai.html'); // Update with your file path

    // Handle window close event to terminate Python process
    mainWindow.on('closed', () => {
        mainWindow = null;
        if (pythonProcess) pythonProcess.kill(); // Terminate the Python backend
    });
}

// Start the Python backend when Electron starts
app.whenReady().then(() => {
    pythonProcess = spawn('python', ['main.py']); // Update with your main.py path

    pythonProcess.stdout.on('data', (data) => {
        console.log(`Python stdout: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python process exited with code ${code}`);
    });

    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

// Quit Electron when all windows are closed
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
