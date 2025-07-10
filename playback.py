from pydub import AudioSegment
from pydub.playback import play

INPUT_FILE = "recorded_audio.wav"

# Read the audio file
audio = AudioSegment.from_wav(INPUT_FILE)

# Play back the audio
print("Playing back recorded audio...")
play(audio)
