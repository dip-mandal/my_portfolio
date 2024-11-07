import speech_recognition as sr
import pyttsx3

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        command = ""
        try:
            command = recognizer.recognize_google(audio)
            print("You said:", command)
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
        except sr.RequestError:
            print("Network error.")
        return command.lower() if command else ""

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
