import os
import wave
import pyaudio

# Create the directories if they don't exist
if not os.path.exists('recordings'):
    os.makedirs('recordings')
if not os.path.exists('transcribed'):
    os.makedirs('transcribed')

# Set up the audio playback parameters
audio_format = 'mp3'  # Note: `pyaudio` handles WAV, not MP3 directly
sample_rate = 44100
channels = 1
chunk_size = 1024

# Function to retrieve and playback files by date, time, or containing string
def retrieve_and_playback(search_parameter):
    # Get list of files in transcribed directory
    recordings_list = os.listdir('transcribed')
    
    # Iterate through list of files
    for file in recordings_list:
        # Check if search parameter is in file name and file is a .wav file
        if search_parameter in file and file.endswith('.wav'):
            file_path = os.path.join('transcribed', file)
            try:
                # Open the file
                wf = wave.open(file_path, 'rb')
                # Set up the audio playback parameters
                p = pyaudio.PyAudio()
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                channels=wf.getnchannels(),
                                rate=wf.getframerate(),
                                output=True)
                # Read data
                data = wf.readframes(chunk_size)
                # Playback the audio
                while len(data) > 0:
                    stream.write(data)
                    data = wf.readframes(chunk_size)
                # Close the stream
                stream.stop_stream()
                stream.close()
                p.terminate()
            except Exception as e:
                print(f"Error playing file {file}: {e}")
            finally:
                wf.close()

# Prompt user to enter search parameter
search_parameter = input("Enter search parameter (date, time, or containing string): ")

# Call function to retrieve and playback files
retrieve_and_playback(search_parameter)
