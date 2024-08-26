import pyttsx3
def say(input):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate", 150)
    engine.say(input)
    engine.runAndWait()