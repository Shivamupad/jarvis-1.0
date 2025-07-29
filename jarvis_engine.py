import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        return query
    except sr.UnknownValueError:
        return "Sorry, I didn’t catch that."
    except sr.RequestError:
        return "Internet error. Try again."
