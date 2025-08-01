import speech_recognition as sr
import threading

def listen_background(callback):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    def listen_loop():
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            while True:
                print("🎙️ Listening...")
                try:
                    audio = recognizer.listen(source)
                    text = recognizer.recognize_google(audio)
                    callback(text)
                except Exception as e:
                    pass

    threading.Thread(target=listen_loop, daemon=True).start()
