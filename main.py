import os
import base64
import uuid
from flask import Flask, send_file, request
from flask_cors import CORS
import modules.llm as llm
from modules.texttospeech import texttospeech
from modules.speechtotext import speechtotext
from modules.intentclassifier import IntentClassifier
from modules.trigger import handleTrigger

app = Flask(__name__)
CORS(app)

model_dir_path = "./models/intentclassifier/"
IC = IntentClassifier(model_dir_path)
IC.load_model()

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

    handleTrigger(prediction, 0.75)

    return {
        "response": response,
        "triggers": prediction
    }

@app.route("/fit_model", methods=["GET"])
def fit_model():
    try:
        IC.fit_model()
        IC.load_model()
        return {
            "error": False,
            "message": "Model has been fit!"
        }
    except:
        return {
            "error": True,
            "message": "An unknown error has occured while fitting the model!"
        }

app.run()