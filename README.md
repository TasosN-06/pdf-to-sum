# 📄 AI PDF Summarizer API

A production-ready microservice that accepts a PDF file and returns a concise AI-generated summary. Built with FastAPI, LangChain, Groq, and Mistral OCR.

---

## 🧠 How it works

1. The user uploads a PDF via the web UI or the `/summarize` endpoint
2. **PyMuPDF** tries to extract text directly from the PDF (fast, no API call)
3. If the PDF is scanned/image-based, **Mistral OCR** is used as a fallback
4. The extracted text is sent to **Groq** (LLaMA 3.3 70B) via **LangChain**
5. A concise bullet-point summary is returned as JSON

---

## 🛠️ Tech Stack

| Tool | Role |
|---|---|
| FastAPI | REST API framework |
| PyMuPDF | Text extraction from PDFs |
| Mistral OCR | OCR fallback for scanned PDFs |
| LangChain + Groq | LLM orchestration & inference |
| Docker | Containerization |

---

## ⚙️ Setup & Run

### Prerequisites
- Docker
- Groq API Key → https://console.groq.com
- Mistral API Key → https://console.mistral.ai
