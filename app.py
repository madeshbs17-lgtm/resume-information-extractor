import json
import os

import pymupdf
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from pydantic import ValidationError

from schemas import ResumeInfo

load_dotenv()

st.set_page_config(
    page_title="Resume Information Extractor",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Resume Information Extractor")
st.write("Upload a resume PDF to extract structured information using AI.")

api_key = os.getenv("GROQ_API_KEY")

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"]
)

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("Extract Information"):
        if not api_key:
            st.error("GROQ_API_KEY is missing from your .env file.")
            st.stop()

        try:
            # Step 1: Extract text from the uploaded PDF
            with pymupdf.open(
                stream=uploaded_file.getvalue(),
                filetype="pdf"
            ) as pdf:
                resume_text = "\n".join(
                    page.get_text() for page in pdf
                ).strip()

            if not resume_text:
                st.error(
                    "No readable text found in this PDF. "
                    "Scanned resumes may require OCR."
                )
                st.stop()

            # Step 2: Prepare the LLM client
            client = Groq(api_key=api_key)
            schema = ResumeInfo.model_json_schema()

            # Step 3: Ask the LLM to extract the information
            with st.spinner("Extracting resume information..."):
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
3. Use empty lists when no items are found.
4. Include every education qualification and work experience.
5. Return a JSON object matching this schema:

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

            # Step 4: Parse and validate the response
            raw_output = response.choices[0].message.content
            data = json.loads(raw_output)
            resume = ResumeInfo.model_validate(data)

            # Step 5: Display the extracted information
            st.subheader("Extracted Resume Information")

            st.write("**Candidate Name**")
            st.write(resume.name or "Not provided")

            st.write("**Email**")
            st.write(resume.email or "Not provided")

            st.write("**Skills**")
            if resume.skills:
                st.write(", ".join(resume.skills))
            else:
                st.write("No skills found")

            st.write("**Education**")
            if resume.education:
                for item in resume.education:
                    st.markdown(
                        f"- **Degree:** {item.degree or 'Not provided'}  \n"
                        f"  **Field:** {item.field or 'Not provided'}  \n"
                        f"  **Institution:** {item.institution or 'Not provided'}"
                    )
            else:
                st.write("No education information found")

            st.write("**Work Experience**")
            if resume.work_experience:
                for item in resume.work_experience:
                    st.markdown(
                        f"- **Job Title:** {item.job_title or 'Not provided'}  \n"
                        f"  **Company:** {item.company or 'Not provided'}  \n"
                        f"  **Description:** {item.description or 'Not provided'}"
                    )
            else:
                st.write("No work experience found")

            with st.expander("View raw JSON"):
                st.json(resume.model_dump(mode="json"))

            st.success("Resume extraction completed!")

        except (json.JSONDecodeError, ValidationError) as error:
            st.error("The AI response could not be parsed or validated.")
            st.code(str(error))

        except Exception as error:
            st.error("Something went wrong while processing the resume.")
            st.code(str(error))