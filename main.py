import os
import base64
import uuid
import sys
from flask import Flask, send_file, request
from flask_cors import CORS
from intentclassification import IntentClassifier, handleTriggers
import modules.llm as llm
from modules.texttospeech import texttospeech
from modules.speechtotext import speechtotext
from modules.trigger import trigger_functions

app = Flask(__name__)
CORS(app)

IC = IntentClassifier(intents_path="./models/intentclassifier/intents.json", output_path="./models/intentclassifier/")

if "--fitmodel" in sys.argv:
    IC.fit_model(epochs=50)
    IC.save_model()
    sys.exit()

IC.load_model()

test_question = "What is your name?"
llm.ask_question_memory(test_question)
IC.predict(test_question)

@app.route("/texttospeech", methods=["POST"])
def tts():
    data = request.get_json()
    filepath = texttospeech(data["text"])

    return send_file(filepath, mimetype="audio/wav")

@app.route("/speechtotext", methods=["POST"])
def stt():
    data = request.get_json()
    decoded = base64.b64decode(data["audio_data"])

    filepath = f"./{uuid.uuid4()}.wav"

    with open(filepath, "wb") as f:
        f.write(decoded)
        f.close()
    
    result = speechtotext(filepath)
    os.remove(filepath)

    return result

@app.route("/wakeword", methods=["POST"])
def wakeword():
    data = request.get_json()
    decoded = base64.b64decode(data["audio_data"])
    wakeword = data["wakeword"]

    filepath = f"./{uuid.uuid4()}.wav"

    with open(filepath, "wb") as f:
        f.write(decoded)
        f.close()
    
    result = speechtotext(filepath)
    os.remove(filepath)

    detected = True if wakeword.lower() in result["text"].lower() else False
    
    return {
        "wakeword": wakeword,
        "detected": detected
    }

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prediction = IC.predict(data["question"])

    if prediction["intent"] == "search_google" and float(prediction["probability"]) > 0.90:
        returns = None
        response = llm.ask_question_google(data["question"])
    else:
        returns = handleTriggers(prediction, 0.90, trigger_functions, ())
        if returns:
            prompt = f"Using this information: {returns}. Respond to the prompt: {data['question']}"
            print(prompt)
            response = llm.ask_question_memory(prompt)
        else:
            response = llm.ask_question_memory(data["question"])

    return {
        "response": response,
        "triggers": {
            "prediction": prediction,
            "returns": returns
        }
    }

app.run()