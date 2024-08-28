import wave
import sys
import json
import numpy as np
from scipy.io import wavfile
from vosk import Model, KaldiRecognizer, SetLogLevel

SetLogLevel(-1)
model = Model("./models/vosk-model-small-en-us-0.15")

def speechtotext(filepath):
    samplerate, data = wavfile.read(filepath)
    new_data = data * 32767
    wavfile.write(filepath, samplerate, new_data.astype(np.int16))
    wf = wave.open(filepath, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit(1)
    
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    rec.SetPartialWords(True)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        rec.AcceptWaveform(data)

    return json.loads(rec.FinalResult())