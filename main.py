import os
import fitz  # PyMuPDF
from fastapi import FastAPI, UploadFile, File, HTTPException
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from mistralai import Mistral
from dotenv import load_dotenv
import tempfile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="AI PDF Summarizer API")

# Serve static files and the main UI
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

# Initialize the Groq LLM with LLaMA 3.3 70B
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
)

# Prompt template for summarization
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert document analyst. "
        "Summarize the following text into 3-5 concise bullet points, "
        "focusing on the key takeaways and most important information.",
    ),
    ("human", "{text}"),
])

# Chain: prompt -> LLM
chain = prompt | llm


def extract_text_pymupdf(pdf_bytes: bytes) -> str:
    """Extract text from a text-based PDF using PyMuPDF."""
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        return "\n".join(page.get_text() for page in doc)


def extract_text_mistral_ocr(pdf_bytes: bytes, filename: str) -> str:
    """Fallback OCR for scanned/image-based PDFs using Mistral."""
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

    import base64
    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": f"data:application/pdf;base64,{pdf_base64}"
        },
    )
    return "\n\n".join(page.markdown for page in ocr_response.pages)


def summarize_text(text: str) -> str:
    """Truncate text if needed and send it to Groq for summarization."""
    # Truncate to 12,000 words to stay within the model's context window
    words = text.split()
    if len(words) > 12_000:
        text = " ".join(words[:12_000])

    response = chain.invoke({"text": text})
    return response.content


@app.post("/summarize")
async def summarize(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    # Read the uploaded file
    pdf_bytes = await file.read()

    # Step 1: Try to extract text with PyMuPDF (fast, no API call)
    text = extract_text_pymupdf(pdf_bytes)

    # Step 2: If text is too short, fall back to Mistral OCR (for scanned PDFs)
    if len(text.strip()) < 100:
        try:
            text = extract_text_mistral_ocr(pdf_bytes, file.filename)
        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail=f"OCR failed: {e}",
            )

    # Step 3: If still no text, return an error
    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="Could not extract any text from the PDF.",
        )

    # Step 4: Summarize the extracted text using Groq
    summary = summarize_text(text)
    return {"filename": file.filename, "summary": summary}