from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from app.services.extractor import extract_text_pymupdf, extract_text_mistral_ocr, get_pdf_info
from app.services.summarizer import summarize_text_stream
import json

router = APIRouter()


@router.post("/summarize")
async def summarize(file: UploadFile = File(...), language: str = Form(default="English")):
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
            raise HTTPException(status_code=422, detail=f"OCR failed: {e}")

    # Step 3: If still no text, return an error
    if not text.strip():
        raise HTTPException(status_code=422, detail="Could not extract any text from the PDF.")

    # Step 4: Get PDF info
    pdf_info = get_pdf_info(pdf_bytes, file.filename, is_scanned)

    # Step 5: Stream the summary
    async def generate():
        # First send the PDF info
        yield f"data: {json.dumps({'type': 'info', 'data': pdf_info, 'filename': file.filename})}\n\n"

        # Then stream the summary tokens
        async for token in summarize_text_stream(text, language):
            yield f"data: {json.dumps({'type': 'token', 'data': token})}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")