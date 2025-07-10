from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import os


response = client.images.generate(prompt="a dear granny watching over her grandkids while they are climbing trees",
n=1,
size="1024x1024")
image_url = response.data[0].url

print(image_url)