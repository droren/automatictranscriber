from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
import os

api_key = os.environ["OPENAI_API_KEY"]

def get_openai_response(prompt):
    # Set up the OpenAI API client

    if "generate image:" in prompt:
        newprompt = prompt.replace("generate image:","")
        response = client.images.generate(prompt = newprompt,
        n=2,
        size="1024x1024")
        message = response.data[0].url
    else:     
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages = [
            {"role":"system","content":"You are a well-behaved, english butler like sarcastic assistant."},
            {"role":"user","content":prompt}
        ])
        message = response.choices[0].message.content.strip()

#    print(response)
    # Extract the response text from the API response

    return message

while True:
    # Prompt the user for input
    user_input = input("You: ")

    # Check if the user wants to exit
    if user_input.lower() == "exit":
        break

    # Generate a response from OpenAI GPT
    response = get_openai_response(user_input)

    # Print the response
    print("Tau:", response)
