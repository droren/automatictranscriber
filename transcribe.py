from openai import OpenAI

client = OpenAI()
import os

api_key = os.environ["OPENAI_API_KEY"]

audio_file = open("recorded_audio.wav", "rb")
transcript = client.audio.transcribe("whisper-1", audio_file)

print(transcript)