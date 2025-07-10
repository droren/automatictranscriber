import unittest
import subprocess
import pyaudio
import os
from datetime import datetime
from openai import OpenAI

client = OpenAI()
import json

class TestAudioTranscription(unittest.TestCase):
    def setUp(self):
        self.api_key = os.environ["OPENAI_API_KEY"]
        self.timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.audio_format = 'mp3'
        self.sample_rate = 44100
        self.channels = 1
        self.chunk_size = 1024
        self.seconds = 20
        self.file_name = f'recordings/starship-log-{self.timestamp}.{self.audio_format}'
        self.log_file_name = f'transcribed/starship-log-{self.timestamp}.log'

    def test_record_audio(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,
                            channels=self.channels,
                            rate=self.sample_rate,
                            input=True,
                            frames_per_buffer=self.chunk_size)

        frames = []

        for i in range(0, int(self.sample_rate / self.chunk_size * self.seconds)):
            data = stream.read(self.chunk_size)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save the recorded audio to a file
        import wave

        wf = wave.open(self.file_name, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        self.assertTrue(os.path.exists(self.file_name))

    def test_transcribe_audio(self):
        audio_file = open(self.file_name, "rb")
        transcription_result = client.audio.transcribe("whisper-1", audio_file)
        transcription_string = json.dumps(transcription_result)

        self.assertIsNotNone(transcription_result)

    def test_save_transcription(self):
        with open(self.log_file_name, 'w') as log_file:
            log_file.write(transcription_string)

        self.assertTrue(os.path.exists(self.log_file_name))

if __name__ == '__main__':
    unittest.main()