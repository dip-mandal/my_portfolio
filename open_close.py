from voice_commands import speak
from application_control import open_application, close_application
import settings

def open_close_application(command):
    while settings.mode == "listening":
        user_input = input("Enter a command: ")
    if "open" in user_input:
        app_name = open_application(user_input)
        if app_name:
            speak(f"{app_name} is now open.")
    elif "close" in user_input:
        if close_application(user_input):
            speak("Application closed.")
        else:
            speak("I couldn't find the application to close.")
    else:
        speak("Sorry, I can't help with that.")