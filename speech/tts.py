# speech/tts.py

from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import sounddevice as sd
import soundfile as sf
import uuid
import os
from dotenv import load_dotenv
load_dotenv() 
client = ElevenLabs(
    api_key=os.getenv("ELEVEN_LABS_API_KEY"),
    timeout=60
)
OUTPUT_DIR = "audio_out"

def text_to_speech(text: str):
    file_path = os.path.join(
        OUTPUT_DIR,
        f"response_{uuid.uuid4().hex}.mp3"
    )

    audio_stream = client.text_to_speech.convert(
        voice_id="Xb7hH8MSUJpSbSDYk0k2",
        model_id="eleven_multilingual_v2",
        text=text
    )

    play(audio_stream)
