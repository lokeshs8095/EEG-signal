import pyttsx3
import threading
import speech_recognition as sr

def speak_text(text):
    """Speak the given text using pyttsx3 in a separate thread."""
    def run_speech():
        engine = pyttsx3.init()
        engine.say(str(text))
        engine.runAndWait()
    threading.Thread(target=run_speech).start()

def recognize_speech():
    """Capture speech input and return it as text."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"🗣️ Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return "Unrecognized Speech"
    except sr.RequestError:
        print("⚠️ Could not request results")
        return "API Error"
