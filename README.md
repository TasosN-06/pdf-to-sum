# 📄 AI PDF Summarizer API

A production-ready microservice that accepts a PDF file and returns a concise AI-generated summary. Built with FastAPI, LangChain, Groq, and Mistral OCR.

---

## ✨ Features

- 📄 **Text-based PDF extraction** via PyMuPDF (fast, no API call)
- 🔍 **OCR fallback** via Mistral for scanned/image-based PDFs
- 🤖 **AI summarization** via Groq (LLaMA 3.3 70B) + LangChain
- 📦 **Chunking** for large PDFs that exceed the model's context window
- ⚡ **Streaming** response — summary appears word by word
- 🌍 **Language selection** — summarize in English, Greek, Spanish, French, German, Italian
- 📊 **PDF Info** — pages, file size, and PDF type displayed
- 📋 **Copy button** — copy the summary with one click
- 🎨 **Custom dark mode UI**
- 🐳 **Dockerized** for easy deployment

---

## 🧠 How it works

1. User uploads a PDF via the web UI or the `/summarize` endpoint
2. **PyMuPDF** tries to extract text directly (fast, no API call)
3. If the PDF is scanned/image-based, **Mistral OCR** is used as fallback
4. If the text is too large, it is split into **chunks** and each chunk is summarized separately
5. The extracted text is sent to **Groq** (LLaMA 3.3 70B) via **LangChain**
6. A concise bullet-point summary is **streamed** back word by word

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

## 📁 Project Structure
pdf-to-sum/
├── app/
│   ├── prompts/
│   │   └── templates.py    # Prompt templates
│   ├── routes/
│   │   └── summarize.py    # API endpoint
│   ├── services/
│   │   ├── extractor.py    # PyMuPDF + Mistral OCR
│   │   └── summarizer.py   # Groq + LangChain + Chunking + Streaming
│   └── init.py
├── static/
│   └── index.html          # Dark mode web UI
├── main.py                 # App initialization
├── Dockerfile
├── requirements.txt
└── README.md

## 🚀 Live Demo

**https://pdf-to-sum-production.up.railway.app**