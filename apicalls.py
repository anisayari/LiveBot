from dotenv import load_dotenv
from pathlib import Path
import os
import openai
import json
import re
import logging
from elevenlabs import generate, play, set_api_key, save


logging.basicConfig(filename="simulation.log",
                    filemode='w')

# Let us Create an object
logger = logging.getLogger()

# Now we are going to Set the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

load_dotenv(Path('.env'))
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
set_api_key(os.getenv('ELEVENLAB_API_KEY'))

openai.organization = os.getenv('OPENAI_ORGA')
openai.api_key = OPENAI_API_KEY

#@TODO : add logger
def get_generate_audio(text, name_audio, voice="Adam"):
    audio = generate(
        text=text,
        voice=voice,
        model="eleven_multilingual_v1"
    )
    save(audio, name_audio)

class OpenAIBrain():
    def __init__(self, name):
        self.name = name
        self.systemData = dict(role="system", content="""Tu es une personne intelligente qui a un débat avec une autre personne""")
        self.messages = [self.systemData]

    def call_API(self, clock, text):
        # Append the user message to the conversation messages
        self.messages.append(dict(role="user", content=text))

        # Call the API with the updated conversation messages
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", max_tokens=100, temperature=1, messages=self.messages)

        # Get the model's response
        text = response['choices'][0]['message']['content']
        print(self.name, text)

        logger.info(f'CLOCK{clock}: clock | AGENT {self.name}')
        logger.info(text)

        return text

    def update_content_data(self, new_content):
        self.messages.append(dict(role="user", content=new_content))
        if len(self.messages) == 9:
            self.messages = self.messages[1:]










