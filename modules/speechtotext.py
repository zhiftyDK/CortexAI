import whisper
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
model = whisper.load_model("base", device="cuda")

def speechtotext(filepath):
    result = model.transcribe(filepath, language="en")
    return result