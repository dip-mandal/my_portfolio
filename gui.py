import tkinter as tk
from main import start_listening
from voice_commands import speak  # To use the speak function

# Initialize Tkinter
window = tk.Tk()
window.title("Voice Assistant")
window.geometry("400x300")

# GUI Labels and Button setup
label = tk.Label(window, text="Click 'Start' to interact", font=("Arial", 14))
label.pack(pady=20)

def start_voice_assistant():
    """Start the voice assistant and display response in GUI."""
    response = start_listening()
    label.config(text=response)  # Display response in GUI
    speak(response)              # Speak the response

# Buttons for interactions
start_button = tk.Button(window, text="Start Voice Assistant", command=start_voice_assistant, font=("Arial", 12), bg="lightblue")
start_button.pack(pady=10)

# Main loop
window.mainloop()
