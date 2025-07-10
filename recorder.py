import pyaudio
import wave

CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_DURATION = 15
OUTPUT_FILE = "recorded_audio.wav"

p = pyaudio.PyAudio()

# Get the default input device index
input_device_index = p.get_default_input_device_info()["index"]

print("Using input device:", p.get_device_info_by_index(
    input_device_index)["name"])

# Open the input stream
input_stream = p.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      input_device_index=input_device_index,
                      frames_per_buffer=CHUNK_SIZE)

# Record for RECORD_DURATION seconds
print("Recording started...")
frames = []
for i in range(0, int(RATE / CHUNK_SIZE * RECORD_DURATION)):
    data = input_stream.read(CHUNK_SIZE)
    frames.append(data)
print("Recording stopped...")

# Stop and close the input stream
input_stream.stop_stream()
input_stream.close()

# Write the recorded audio to a file
with wave.open(OUTPUT_FILE, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

# Terminate PyAudio
p.terminate()
