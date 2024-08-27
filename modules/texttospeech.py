import pyttsx3
import uuid
import threading
import os
import time

def deleteFile(filepath):
    time.sleep(1)
    os.remove(filepath)

def texttospeech(input):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate", 150)
    filepath = f"./{uuid.uuid4()}.wav"
    engine.save_to_file(input, filepath)
    engine.runAndWait()
    threading.Thread(target=deleteFile, args=(filepath,)).start()
    return filepath