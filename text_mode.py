from voice_commands import speak
from application_control import open_application, close_application
import settings
from keypress_listener import listen_for_keypress

def text_input_mode():
    speak("Text input mode is activated. Type 'start' to return to listening mode.")
    while settings.mode == "text_input":
        listen_for_keypress()  # Check if "d" key is pressed to switch back
        user_input = input("Enter command (type 'start' to return to listening mode): ").lower()
        if user_input == "start":
            return "listening"
        # elif "open" in user_input:
        #     app_name = open_application(user_input)
        #     if app_name:
        #         speak(f"{app_name} is now open.")
        # elif "close" in user_input:
        #     if close_application(user_input):
        #         speak("Application closed.")
        #     else:
        #         speak("I couldn't find the application to close.")
        # else:
        #     speak("Sorry, I can't help with that.")
