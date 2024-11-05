import pyttsx3
import speech_recognition as sr
import eel
import time
from engine.features import openCommand, PlayYoutube, findContact, whatsApp, makeCall, sendMessage, chatBot

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10, phrase_time_limit=6)
    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not catch that. Could you please repeat?")
        return ""
    except sr.RequestError:
        speak("Sorry, I am having trouble connecting to the recognition service.")
        return ""
    except Exception as e:
        speak("Sorry, something went wrong.")
        return ""

@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
    else:
        query = message

    query = str(query).lower()  # Ensure query is a string and in lowercase
    eel.senderText(query)
    
    try:
        if "open" in query:
            openCommand(query)
        elif "on youtube" in query:
            PlayYoutube(query)
        elif "send message" in query or "phone call" in query or "video call" in query:
            contact_no, name = findContact(query)
            if contact_no != 0:
                speak("Which mode would you like to use: WhatsApp or mobile?")
                preference = takecommand()

                if "mobile" in preference:
                    if "send message" in query or "send sms" in query: 
                        speak("What message would you like to send?")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("Please try again.")
                elif "whatsapp" in preference:
                    if "send message" in query:
                        speak("What message would you like to send?")
                        query = takecommand()
                        message = 'message'
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                    whatsApp(contact_no, query, message, name)
        else:
            chatBot(query)
    except Exception as e:
        print(f"Error occurred: {e}")
    
    eel.ShowHood()
