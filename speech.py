import os
from gtts import gTTS
from io import BytesIO
import pygame

# Get the OpenAI API key from environment variables
# (not used here but kept for consistency with your initial approach)
openai_api_key = os.getenv("OPENAI_API_KEY")

# Text you want to convert to speech
text = "Today is a wonderful day to build something people love!"

# Convert text to speech using gTTS
tts = gTTS(text, lang='en')

# Save the speech to a BytesIO object
speech_data = BytesIO()
tts.write_to_fp(speech_data)
speech_data.seek(0)

# Initialize pygame mixer
pygame.mixer.init()
pygame.mixer.music.load(speech_data)
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    continue
