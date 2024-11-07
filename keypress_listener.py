import keyboard  # Import the keyboard module
from voice_commands import speak
import settings
import time  # To add a small delay

def listen_for_keypress():
        if keyboard.is_pressed("s"):
            settings.mode = "text_input"
            speak("Text input mode activated.")
            time.sleep(0.2)  # Prevent repeated activation on one press
        elif keyboard.is_pressed("d"):
            settings.mode = "listening"
            speak("Listening mode activated.")
            time.sleep(0.2)  # Prevent repeated activation on one press

# Call the function to start listening
listen_for_keypress()
