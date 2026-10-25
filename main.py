import os
import json
import pymupdf

from dotenv import load_dotenv
from groq import Groq
from pydantic import ValidationError

from schemas import ResumeInfo

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from your .env file.")

client = Groq(api_key=api_key)

pdf_path = "sample_resume.pdf"

try:
    with pymupdf.open(pdf_path) as pdf:
        resume_text = "\n".join(
            page.get_text() for page in pdf
        ).strip()

    if not resume_text:
        raise ValueError("No readable text found in the PDF.")

    print("PDF text extracted successfully!")

except (FileNotFoundError, RuntimeError, ValueError) as error:
    print(f"Error reading PDF: {error}")
    raise SystemExit(1)

schema = ResumeInfo.model_json_schema()

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": f"""
You are a resume information extraction assistant.

Extract information only from the supplied resume.

Rules:
1. Never invent missing information.
2. Use null for missing text fields.
3. Use empty lists when no items are found for skills,
   education, or work_experience.
4. Include every education qualification and work experience.
5. Do not infer total years of experience unless the resume
   explicitly provides enough information to determine it.
6. Return a JSON object matching this schema:

{json.dumps(schema)}
"""
        },
        {
            "role": "user",
            "content": resume_text
        }
    ],
    response_format={"type": "json_object"},
    temperature=0
)

raw_output = response.choices[0].message.content

try:
    data = json.loads(raw_output)
    resume = ResumeInfo.model_validate(data)

    print("\nExtracted Resume Information:\n")
    print(resume.model_dump_json(indent=2))

except (json.JSONDecodeError, ValidationError) as error:
    print("Could not validate the extracted resume information.")
    print(error)