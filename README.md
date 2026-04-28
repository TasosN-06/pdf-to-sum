# 📄 AI PDF Summarizer API

A production-ready microservice that accepts a PDF file and returns a concise AI-generated summary. Built with FastAPI, LangChain, Groq, and Mistral OCR.

🚀 **Live Demo:** https://pdf-to-sum-production.up.railway.app

---

## ✨ Features

- 📄 **Text-based PDF extraction** via PyMuPDF (fast, no API call)
- 🔍 **OCR fallback** via Mistral for scanned/image-based PDFs
- 🤖 **AI summarization** via Groq (LLaMA 3.3 70B) + LangChain
- 📦 **Chunking** for large PDFs that exceed the model's context window
- ⚡ **Parallel chunk processing** via `asyncio.gather()` for faster summarization
- 🌊 **Streaming** response — summary appears word by word
- 🗂️ **Structured summary** — strictly typed JSON with title, summary, category, keywords and length
- 🌍 **Language selection** — English, Greek, Spanish, French, German, Italian
- 🎨 **Summary style** — Bullet Points, Paragraph, Executive Summary, ELI5
- 📊 **PDF Info** — pages, file size, and PDF type
- 🕓 **Session History** — browse and restore previous summaries
- 📋 **Copy** & 💾 **Download** summary as `.txt`
- ⌨️ **Keyboard shortcut** — press Enter to summarize
- 📱 **Mobile responsive** UI
- 🎨 **Custom dark mode UI**
- 🐳 **Dockerized** for easy deployment
- 🚂 **Deployed on Railway**

---

## 🧠 How it works

1. User uploads a PDF via the web UI or the `/summarize` endpoint
2. **PyMuPDF** tries to extract text directly (fast, no API call)
3. If the PDF is scanned/image-based, **Mistral OCR** is used as fallback
4. If the text is too large, it is split into **chunks** processed **in parallel** via `asyncio.gather()`
5. The extracted text is sent to **Groq** (LLaMA 3.3 70B) via **LangChain**
6. The summary is **streamed** back word by word in the selected language and style
7. Optionally, **structured summary** can be requested via `/structured-summary`, returning a strictly typed JSON enforced by a Pydantic model and LangChain's `with_structured_output()`

---

## 🛠️ Tech Stack

| Tool | Role |
|---|---|
| FastAPI | REST API framework |
| PyMuPDF | Text extraction from PDFs |
| Mistral OCR | OCR fallback for scanned PDFs |
| LangChain + Groq | LLM orchestration & inference |
| Pydantic | Structured output validation |
| asyncio | Parallel chunk processing |
| Docker | Containerization |
| Railway | Cloud deployment |

---

## 📁 Project Structure

```
pdf-to-sum/
├── app/
│   ├── prompts/
│   │   └── templates.py      # Prompt templates per style
│   ├── routes/
│   │   └── summarize.py      # API endpoints (/summarize, /structured-summary)
│   ├── services/
│   │   ├── extractor.py      # PyMuPDF + Mistral OCR
│   │   ├── summarizer.py     # Groq + LangChain + Parallel Chunking + Streaming
│   │   └── structured.py     # Structured output via Pydantic + with_structured_output()
│   └── __init__.py
├── static/
│   └── index.html            # Dark mode web UI
├── main.py                   # App initialization
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🗂️ Structured Summary

The `/structured-summary` endpoint returns a strictly typed JSON enforced by LangChain's `with_structured_output()` and a Pydantic model:

```json
{
  "filename": "document.pdf",
  "title": "Generated document title",
  "summary": "The actual summarization...",
  "summary_length": 42,
  "category": "Technical",
  "keywords": ["AI", "FastAPI", "LangChain"]
}
```

Visit **http://localhost:8000**
