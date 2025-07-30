import os
import webbrowser
import datetime

def handle_command(command):
    command = command.lower()

    if "hello" in command:
        return "Hello! How can I assist you?"

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube"

    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google"

    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}"

    elif "date" in command:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        return f"Today is {today}"

    elif "open notepad" in command:
        os.system("notepad")
        return "Opening Notepad"

    elif "exit" in command or "stop" in command:
        return "exit"

    else:
        return "Sorry, I didn't understand that."
