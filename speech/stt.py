# speech/stt.py
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import whisper

SAMPLE_RATE = 16000
RECORD_SECONDS = 6
AUDIO_FILE = "input.wav"

model = whisper.load_model("base")

def listen_text():
    print("🎙️ Listening...")

    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype=np.int16
    )
    sd.wait()

    wav.write(AUDIO_FILE, SAMPLE_RATE, audio)

    result = model.transcribe(AUDIO_FILE)
    text = result["text"].strip()

    return text
