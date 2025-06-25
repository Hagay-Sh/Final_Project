from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()  # Load variables from .env file
api_key = os.getenv("OPENAI_API_KEY")

# Create an OpenAI client instance
client = OpenAI(api_key=api_key)



# Create a ChatGPT
def ChatGPT_Prompt_Parameter_Tuner(prompt, temperature, top_p, max_tokens):
        
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{'role':'user', 'content':prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )
        
    return completion.choices[0].message.content
