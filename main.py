from flask import Flask, jsonify
from voice_commands import listen_command, speak
from application_control import open_application, close_application

app = Flask(__name__)

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
        else:
            return "Sorry, I can't help with that."
    return "I didn't catch that."

@app.route('/start_voice_assistant', methods=['GET'])
def start_voice_assistant():
    """Listen for a command, process it, and return the response."""
    command = listen_command()
    response = process_command(command)
    speak(response)  # Speak the response
    return jsonify(response=response)

if __name__ == '__main__':
    app.run(debug=True)
