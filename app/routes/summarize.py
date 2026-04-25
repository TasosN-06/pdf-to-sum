from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.extractor import extract_text_pymupdf, extract_text_mistral_ocr, get_pdf_info
from app.services.summarizer import summarize_text

router = APIRouter()


@router.post("/summarize")
async def summarize(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    # Read the uploaded file
    pdf_bytes = await file.read()

    # Step 1: Try to extract text with PyMuPDF (fast, no API call)
    text = extract_text_pymupdf(pdf_bytes)
    is_scanned = False

    # Step 2: If text is too short, fall back to Mistral OCR (for scanned PDFs)
    if len(text.strip()) < 100:
        is_scanned = True
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

    # Step 4: Get PDF info
    pdf_info = get_pdf_info(pdf_bytes, file.filename, is_scanned)

    # Step 5: Summarize the extracted text using Groq
    summary = summarize_text(text)
    
    return {
        "filename": file.filename,
        "summary": summary,
        "info": pdf_info
    }