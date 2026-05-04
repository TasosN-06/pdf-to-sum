---
title: Pdf To Sum
emoji: 📄
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# 📄 AI PDF Summarizer

A production-ready AI-powered PDF summarizer with user authentication. Built with FastAPI, LangChain, Groq, Mistral OCR, and Supabase.

---

## ✨ Features

- 🔐 **Authentication** — Sign Up / Sign In / Sign Out with email confirmation via Supabase
- 📄 **Text-based PDF extraction** via PyMuPDF (fast, no API call)
- 🔍 **OCR fallback** via Mistral for scanned/image-based PDFs
- 🤖 **AI summarization** via Groq (LLaMA 3.3 70B) + LangChain
- 📦 **Chunking** for large PDFs that exceed the model's context window
- ⚡ **Parallel chunk processing** via `asyncio.gather()` for faster summarization
- 🌊 **Streaming** response — summary appears word by word
- 📋 **Structured summary** — strictly typed JSON with title, summary, category, keywords and length
- 🌍 **Language selection** — English, Greek, Spanish, French, German, Italian
- 💬 **Summary style** — Bullet Points, Paragraph, Executive Summary, ELI5
- 📊 **PDF Info** — pages, file size, and PDF type
- 🕘 **Session History** — browse and restore previous summaries
- 📋 **Copy** & 💾 **Download** summary as `.txt`