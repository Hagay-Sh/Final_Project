from openai import OpenAI
from dotenv import load_dotenv
import os
import base64


load_dotenv()  # Loads variables from .env

openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

file = client.files.create(
    file=open("Basic_Woodworking_Course_Syllabus.pdf", "rb"),  # "rb" means read binary mode. Used to read files like PDFs or images
   # file=open("Python Developer job Description.pdf", "rb"),  # "rb" means read binary mode. Used to read files like PDFs or images
    purpose="user_data"
)

response = client.responses.create(
    model="gpt-4.1",
    input=[
        {"role": "user",
        "content":
                [{"type": "input_file","file_id": file.id},
                {"type": "input_text", "text": "What is the instructor name?"}]
        }
    ]
)

print(response.output_text)

files = client.files.list()

for f in files.data:
    print(f.id)
    print(f.filename)
    print()

client.files.delete(file.id)  

with open("Basic_Woodworking_Course_Syllabus.pdf", "rb") as f:  # "rb" means read binary mode. Used to read files like PDFs or images
    data = f.read()

base64_string = base64.b64encode(data).decode("utf-8")

response = client.responses.create(
    model="gpt-4.1",
    input=[
        {"role": "user",
        "content":
                [{"type": "input_file", "filename": "Basic_Woodworking_Course_Syllabus.pdf", "file_data": f"data:application/pdf;base64,{base64_string}"},
                {"type": "input_text", "text": "What is opening date?"}]
        }
    ]
)

print(response.output_text)


