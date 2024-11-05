import os
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound  import playsound # Corrected import
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import pvporcupine
from urllib.parse import quote
import hugchat

from engine.helper import extract_yt_term, remove_words

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# Function to play the assistant's sound
def playAssistantSound():
    music_dir = os.path.join("www", "assets", "audio", "start_sound.mp3")
    try:
        playsound(music_dir)
    except Exception as e:
        speak(f"Unable to play sound. Error: {str(e)}")

# Function to open applications or websites
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "").replace("open", "").lower().strip()
    try:
        cursor.execute('SELECT path FROM sys_command WHERE name=?', (query,))
        results = cursor.fetchall()
        if results:
            speak(f"Opening {query}")
            os.startfile(results[0][0])
        else:
            cursor.execute('SELECT url FROM web_command WHERE name=?', (query,))
            results = cursor.fetchall()
            if results:
                speak(f"Opening {query}")
                webbrowser.open(results[0][0])
            else:
                speak(f"Opening {query}")
                os.system(f'start {query}')
    except Exception as e:
        speak(f"Something went wrong. Error: {str(e)}")

# Function to play YouTube videos
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak(f"Playing {search_term} on YouTube")
    kit.playonyt(search_term)

# Function to detect hotwords
def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(keywords=["jarvis", "alexa"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)
        
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)
            if keyword_index >= 0:
                print("Hotword detected")
                pyautogui.hotkey('win', 'j')  # Adjust for Windows 11 Taskbar
                time.sleep(2)
    except Exception as e:
        speak(f"Error detecting hotword: {str(e)}")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# Function to find contacts
def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove).strip().lower()
    try:
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        if results:
            mobile_number_str = str(results[0][0])
            if not mobile_number_str.startswith('+91'):
                mobile_number_str = '+91' + mobile_number_str
            return mobile_number_str, query
        else:
            speak('Contact not found')
            return None, None
    except Exception as e:
        speak(f"Error finding contact: {str(e)}")
        return None, None

# Function to send WhatsApp messages or make calls
def whatsApp(mobile_no, message, flag, name):
    try:
        if flag == 'message':
            target_tab = 12
            jarvis_message = f"Message sent successfully to {name}"
        elif flag == 'call':
            target_tab = 7
            jarvis_message = f"Calling {name}"
        else:
            target_tab = 6
            jarvis_message = f"Starting video call with {name}"

        encoded_message = quote(message)
        whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
        full_command = f'start "" "{whatsapp_url}"'

        subprocess.run(full_command, shell=True)
        time.sleep(5)
        subprocess.run(full_command, shell=True)
        pyautogui.hotkey('ctrl', 'f')

        for _ in range(1, target_tab):
            pyautogui.hotkey('tab')
        pyautogui.hotkey('enter')
        speak(jarvis_message)
    except Exception as e:
        speak(f"Error with WhatsApp operation: {str(e)}")

# Function to interact with the chatbot
def chatBot(query):
    try:
        user_input = query.lower()
        chatbot = hugchat.ChatBot(cookie_path=os.path.join("engine", "cookies.json"))
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        response = chatbot.chat(user_input)
        print(response)
        speak(response)
        return response
    except Exception as e:
        speak(f"Error interacting with chatbot: {str(e)}")

# Function to make a phone call via Android automation
def makeCall(name, mobileNo):
    mobileNo = mobileNo.replace(" ", "")
    speak(f"Calling {name}")
    command = f'adb shell am start -a android.intent.action.CALL -d tel:{mobileNo}'
    os.system(command)

# Function to send a message via Android automation
def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    try:
        message = replace_spaces_with_percent_s(message)
        mobileNo = replace_spaces_with_percent_s(mobileNo)
        speak("Sending message")
        goback(4)
        time.sleep(1)
        keyEvent(3)
        tapEvents(136, 2220)  # Open SMS app (Coordinates may need adjustment)
        tapEvents(819, 2192)  # Start chat (Coordinates may need adjustment)
        adbInput(mobileNo)     # Search mobile no
        tapEvents(601, 574)    # Tap on name (Coordinates may need adjustment)
        tapEvents(390, 2270)   # Tap on input field (Coordinates may need adjustment)
        adbInput(message)      # Input message
        tapEvents(957, 1397)   # Send message (Coordinates may need adjustment)
        speak(f"Message sent successfully to {name}")
    except Exception as e:
        speak(f"Error sending message: {str(e)}")
