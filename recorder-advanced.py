import os
import wave
import pyaudio
import json
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Initialize OpenAI client
api_key = os.environ["OPENAI_API_KEY"]

# Create the directories if they don't exist
if not os.path.exists('recordings'):
    os.makedirs('recordings')
if not os.path.exists('transcribed'):
    os.makedirs('transcribed')

# Format the timestamp for the file names
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Set up the audio recording parameters
sample_rate = 44100
channels = 1
chunk_size = 2048
buffer_duration = 0.5

# Initialize PyAudio
audio = pyaudio.PyAudio()

def start_recording():
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)
    frames = []
    buffer_frames = int(sample_rate / chunk_size * buffer_duration)

    print("Recording... Speak 'stop recording' to end.")

    while True:
        buffer = []
        for _ in range(buffer_frames):
            data = stream.read(chunk_size)
            buffer.append(data)
            frames.append(data)

        # Check for "stop recording" using OpenAI
        audio_data = wave.open('temp.wav', 'wb')
        audio_data.setnchannels(channels)
        audio_data.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        audio_data.setframerate(sample_rate)
        audio_data.writeframes(b''.join(buffer))
        audio_data.close()

        with open('temp.wav', 'rb') as audio_file:
            try:
                response = client.audio.translations.create(model="whisper-1", file=audio_file)
                if "stop recording" in response.text.lower():
                    print("Stop command received. Ending recording.")
                    os.remove('temp.wav')  # Clean up the temporary file
                    break
            except Exception as e:
                print(f"Error during transcription: {e}")

    stream.stop_stream()
    stream.close()
    return frames

# Record the audio
frames = start_recording()
audio.terminate()

# Save the recorded audio to a WAV file
file_name = f'recordings/starship-log-{timestamp}.wav'

wf = wave.open(file_name, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
wf.setframerate(sample_rate)
wf.writeframes(b''.join(frames))
wf.close()

# Transcribe the recorded audio using OpenAI
with open(file_name, "rb") as audio_file:
    transcription_result = client.audio.transcribe(model="whisper-1", file=audio_file)

transcription_string = json.dumps(transcription_result, indent=2)

print(transcription_result)

# Save the transcription to a file
log_file_name = f'transcribed/starship-log-{timestamp}.log'

with open(log_file_name, 'w') as log_file:
    log_file.write(transcription_string)
