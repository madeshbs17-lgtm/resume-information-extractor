# 📄 Resume Information Extractor

An AI-powered application that extracts structured information from PDF resumes using a Large Language Model (LLM). Built with Python, Groq, Pydantic, PyMuPDF, and Streamlit.

## 🚀 Features

- **PDF Upload:** Upload resumes in PDF format.
- **AI-Powered Extraction:** Uses an LLM through the Groq API to extract resume information.
- **Candidate Information:** Extracts the candidate's name and email.
- **Skills Extraction:** Identifies technical and professional skills.
- **Education Extraction:** Extracts degrees, fields of study, and institutions.
- **Work Experience Extraction:** Identifies job titles, companies, and experience descriptions.
- **Structured Output:** Uses Pydantic to validate extracted information.
- **Interactive Interface:** Displays results through a Streamlit web application.
- **JSON Output:** View the extracted information in JSON format.
- **Missing Information Handling:** Displays missing fields as "Not provided" in the interface.

## 🛠️ Tech Stack

- Python
- Groq API
- OpenAI GPT-OSS 20B model, accessed through Groq
- Pydantic
- PyMuPDF
- Streamlit
- python-dotenv

## 📂 Project Structure

```text
resume-information-extractor/
├── app.py
├── main.py
├── schemas.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd resume-information-extractor
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your own API key. Never commit your API key to GitHub.

### 5. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, upload a PDF resume, and click **Extract Information**.

## 🧠 How It Works

1. The user uploads a PDF resume.
2. PyMuPDF extracts text from the PDF.
3. The extracted text is sent to the LLM through the Groq API.
4. The model returns the information in JSON format.
5. Python parses the JSON response.
6. Pydantic validates the extracted data against the defined schema.
7. Streamlit displays the extracted information.

## 📋 Extracted Information

The application extracts:

- Candidate name
- Email address
- Skills
- Education qualifications
  - Degree
  - Field of study
  - Institution
- Work experience
  - Job title
  - Company
  - Description

## 🔒 Security and Limitations

- Store API keys in `.env` and exclude that file from version control.
- The application requires a working Groq API connection.
- Scanned PDFs may not work without OCR.
- Extraction accuracy depends on the quality and structure of the resume and the model's response.
- Extracted information should be reviewed for accuracy.

## 🔮 Future Improvements

- Add support for DOCX