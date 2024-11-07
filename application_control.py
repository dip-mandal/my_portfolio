import subprocess
import os
import psutil
from voice_commands import speak

def open_application(command):
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    }

    for app_name, app_path in apps.items():
        if app_name in command:
            speak(f"Opening {app_name}.")
            subprocess.Popen(app_path)
            return app_name
    return None

def close_application(command):
    apps_to_check = {
        "notepad": "notepad.exe",
        "calculator": ["calc.exe", "calculator.exe", "Calculator.exe"],
        "chrome": "chrome.exe",
        "word": "WINWORD.EXE"
    }

    for app_name, process_names in apps_to_check.items():
        if app_name in command:
            speak(f"Closing {app_name}.")
            
            if app_name == "calculator":
                # Use PowerShell to close the Calculator UWP app
                subprocess.run([
                    "powershell", "-Command",
                    "Get-Process | Where-Object { $_.Path -like '*WindowsCalculator*' } | Stop-Process -Force"
                ], shell=True)
                return True

            # For other apps, use psutil to close based on process name
            closed = False
            if not isinstance(process_names, list):
                process_names = [process_names]
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].lower() in [name.lower() for name in process_names]:
                        os.kill(proc.info['pid'], 9)
                        closed = True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return closed
    return False
