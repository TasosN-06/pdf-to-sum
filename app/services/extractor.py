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

def get_pdf_info(pdf_bytes: bytes, filename: str, is_scanned: bool) -> dict:
    """Extract basic info from the PDF."""
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        num_pages = len(doc)
    
    size_kb = round(len(pdf_bytes) / 1024, 1)
    size_str = f"{size_kb} KB" if size_kb < 1024 else f"{round(size_kb/1024, 1)} MB"
    
    return {
        "pages": num_pages,
        "size": size_str,
        "type": "Scanned PDF" if is_scanned else "Text PDF"
    }