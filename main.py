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
    IC.fit_model()
    IC.save_model()
    sys.exit()

IC.load_model()

test_question = "What is your name?"
llm.generate(test_question)
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

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    response = llm.generate(data["question"])
    prediction = IC.predict(data["question"])

    returns = handleTriggers(prediction, 0.75, trigger_functions)

    return {
        "response": response,
        "triggers": {
            "prediction": prediction,
            "returns": returns
        }
    }

app.run()