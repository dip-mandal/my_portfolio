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


# import speech_recognition as sr
# import pyttsx3
# import sounddevice as sd
# import numpy as np
# import wavio  # Optional, helps in saving audio as .wav format in memory

# def listen_command():
#     # Define audio settings
#     recognizer = sr.Recognizer()
#     sample_rate = 16000  # Set sample rate
#     duration = 5  # Duration of recording in seconds

#     print("Listening...")
#     # Record audio with sounddevice
#     audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
#     sd.wait()  # Wait until the recording is finished

#     # Save recorded audio as .wav format in memory
#     wavio.write("temp_audio.wav", audio_data, sample_rate, sampwidth=2)

#     # Now use speech_recognition to recognize from this audio file
#     with sr.AudioFile("temp_audio.wav") as source:
#         audio = recognizer.record(source)  # Load the audio to speech_recognition
#         command = ""
#         try:
#             command = recognizer.recognize_google(audio)
#             print("You said:", command)
#         except sr.UnknownValueError:
#             print("Sorry, I didn't understand that.")
#         except sr.RequestError:
#             print("Network error.")
#         return command.lower() if command else ""

# def speak(text):
#     engine = pyttsx3.init()
#     engine.say(text)
#     engine.runAndWait()

