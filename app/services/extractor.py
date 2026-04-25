import os
import base64
import fitz  # PyMuPDF
from mistralai import Mistral


def extract_text_pymupdf(pdf_bytes: bytes) -> str:
    """Extract text from a text-based PDF using PyMuPDF."""
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        return "\n".join(page.get_text() for page in doc)


def extract_text_mistral_ocr(pdf_bytes: bytes, filename: str) -> str:
    """Fallback OCR for scanned/image-based PDFs using Mistral."""
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": f"data:application/pdf;base64,{pdf_base64}"
        },
    )
    return "\n\n".join(page.markdown for page in ocr_response.pages)