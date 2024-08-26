import modules.llm as llm
import modules.texttospeech as tts
import modules.speechtotext as stt

print("Ready!")
while True:    
    wakeword = stt.recognize().lower()
    if "hey cortex" in wakeword:
        while True:
            print("Recognizing!")
            question = stt.recognize()
            if len(question) == 0:
                continue
            print("You:", question)
            response = llm.generate(question)
            print("Bot:", response["message"]["content"])
            tts.say(response["message"]["content"])
            if "goodbye" in question or "good bye" in question:
                print("Ready!")
                break