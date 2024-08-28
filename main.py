import os
import base64
import uuid
import logging
from flask import Flask, send_file, request
from flask_cors import CORS
import modules.llm as llm
from modules.texttospeech import texttospeech
from modules.speechtotext import speechtotext

app = Flask(__name__)
CORS(app)

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
    return response

app.run()