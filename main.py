from flask import Flask, jsonify
from voice_commands import listen_command, speak
from application_control import open_application, close_application
import threading
import time
import webbrowser

app = Flask(__name__)
assistant_running = False  # Global variable to track the assistant's state
assistant_thread = None  # To store the thread

def process_command(command):
    """Process a voice command and return the response."""
    if command:
        if "hello" in command:
            return "Hello! How can I help you?"
        elif "your name" in command:
            return "I'm your personal assistant!"
        elif "open" in command:
            app_name = open_application(command)
            return f"{app_name} is now open." if app_name else "I couldn't open that application."
        elif "close" in command:
            closed = close_application(command)
            return "Application closed." if closed else "I couldn't find the application to close."
        elif "search" in command:
            query = command.replace("search", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return "I found that."
        else:
            return "Sorry, I can't help with that."
    return "I didn't catch that."

def run_assistant():
    """Continuously listens and processes commands while assistant is running."""
    global assistant_running
    while assistant_running:
        command = listen_command()
        response = process_command(command)
        speak(response)
        time.sleep(1)  # Small delay to prevent excessive looping

@app.route('/start_voice_assistant', methods=['GET'])
def start_voice_assistant():
    """Start the voice assistant in a separate thread to listen for commands continuously."""
    global assistant_running, assistant_thread
    if not assistant_running:
        assistant_running = True
        assistant_thread = threading.Thread(target=run_assistant)
        assistant_thread.start()
        return jsonify(message="Voice assistant started.")
    else:
        return jsonify(message="The assistant is already running.")

@app.route('/stop_voice_assistant', methods=['GET'])
def stop_voice_assistant():
    """Stop the voice assistant and return a response indicating it's stopped."""
    global assistant_running
    if assistant_running:
        assistant_running = False
        return jsonify(message="The assistant has been stopped.")
    else:
        return jsonify(message="The assistant is not running.")

if __name__ == '__main__':
    app.run(debug=True)
