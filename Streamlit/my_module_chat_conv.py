from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()  # Load variables from .env file
api_key = os.getenv("OPENAI_API_KEY")

# Create an OpenAI client instance
client = OpenAI(api_key=api_key)



# Create a ChatGPT
def ChatGPT_Conversation(messages):
        
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
        
    return completion.choices[0].message.content
