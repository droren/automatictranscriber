import os
import wave
import pyaudio
from datetime import datetime

# Create the directories if they don't exist
if not os.path.exists('recordings'):
    os.makedirs('recordings')
if not os.path.exists('transcribed'):
    os.makedirs('transcribed')

# Set up the audio recording parameters
audio_format = 'mp3'
sample_rate = 44100
channels = 1
chunk_size = 1024
seconds = 20

# Function to record audio for a specified duration
def record_audio(timestamp):
    # Record the audio for a specified duration
    input("Press enter to start recordings")
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

    frames = []

    for i in range(0, int(sample_rate / chunk_size * seconds)):
        data = stream.read(chunk_size)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a file
    file_name = f'recordings/starship-log-{timestamp}.{audio_format}'

    wf = wave.open(file_name, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    return file_name

# Function to transcribe audio using OpenAI
def transcribe_audio(file_name):
    # Transcribe the recorded audio using OpenAI
    audio_file = open(file_name, "rb")
    transcription_result = Audio.transcribe("whisper-1", audio_file)
    transcription_string = json.dumps(transcription_result)

    print(transcription_result)

    # Save the transcription to a file
    log_file_name = f'transcribed/starship-log-{timestamp}.log'

    with open(log_file_name, 'w') as log_file:
        log_file.write(transcription_string)

    return log_file_name

# Function to retrieve and play back files either by date, time or containing string
def retrieve_and_playback(date, time, string):
    # Retrieve the files based on the given criteria
    recordings = os.listdir('recordings')
    transcriptions = os.listdir('transcribed')

    # Filter the files based on the given criteria
    filtered_recordings = [recording for recording in recordings if (date in recording or time in recording or string in recording)]
    filtered_transcriptions = [transcription for transcription in transcriptions if (date in transcription or time in transcription or string in transcription)]

    # Play back the retrieved files
    for recording in filtered_recordings:
        wf = wave.open(f'recordings/{recording}', 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(chunk_size)

        while data != '':
            stream.write(data)
            data = wf.readframes(chunk_size)

        stream.stop_stream()
        stream.close()
        p.terminate()

    for transcription in filtered_transcriptions:
        with open(f'transcribed/{transcription}', 'r') as log_file:
            transcription_string = log_file.read()
            print(transcription_string)

# Main function
if __name__ == '__main__':
    # Format the timestamp for the file names
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Record the audio
    file_name = record_audio(timestamp)

    # Transcribe the audio
    log_file_name = transcribe_audio(file_name)

    # Retrieve and playback the files
    retrieve_and_playback('2020-10-01', '12-00-00', 'starship')