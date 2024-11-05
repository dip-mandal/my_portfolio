import os
import eel
import subprocess
from engine.features import playAssistantSound, speak
from engine.command import *
from engine.auth import recoganize

def start():
    # Initialize the Eel library with the folder containing the web files
    eel.init("www")

    # Play an assistant sound
    playAssistantSound()

    # Expose the init function to JavaScript
    @eel.expose
    def init():
        # Execute a batch file to start device-related processes
        subprocess.call([r'device.bat'])
        
        # Hide the loader on the web interface
        eel.hideLoader()
        
        # Notify the user that face authentication is starting
        speak("Ready for Face Authentication")
        
        # Perform face authentication
        flag = recoganize.AuthenticateFace()
        
        # Check the result of face authentication
        if flag == 1:
            # If successful, update the web interface and greet the user
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()
            speak("Hello, Welcome Sir, How can I help you?")
            eel.hideStart()
            playAssistantSound()
        else:
            # If authentication fails, notify the user
            speak("Face Authentication Failed")

    # Open the web interface in Microsoft Edge as an app
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    # Start the Eel application
    eel.start('index.html', mode=None, host='localhost', block=True)

if __name__ == "__main__":
    start()
