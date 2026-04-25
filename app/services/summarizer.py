import os
from langchain_groq import ChatGroq
from app.prompts.templates import get_summarize_prompt

# Initialize the Groq LLM with LLaMA 3.3 70B
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
)

CHUNK_SIZE = 4_000  # words per chunk


def chunk_text(text: str) -> list[str]:
    """Split text into chunks of CHUNK_SIZE words."""
    words = text.split()
    return [
        " ".join(words[i:i + CHUNK_SIZE])
        for i in range(0, len(words), CHUNK_SIZE)
    ]


def summarize_text(text: str, language: str = "English") -> str:
    """Summarize text using chunking for large documents."""
    words = text.split()

    # If text is small enough, summarize directly
    if len(words) <= CHUNK_SIZE:
        prompt = get_summarize_prompt(language)
        chain = prompt | llm
        response = chain.invoke({"text": text})
        return response.content

    # For large texts: chunk -> summarize each -> final summary
    chunks = chunk_text(text)
    chunk_summaries = []

    for i, chunk in enumerate(chunks):
        prompt = get_summarize_prompt(language)
        chain = prompt | llm
        response = chain.invoke({"text": chunk})
        chunk_summaries.append(f"Part {i+1}:\n{response.content}")

    # Final summary from all chunk summaries
    combined = "\n\n".join(chunk_summaries)
    final_prompt = get_summarize_prompt(language)
    final_chain = final_prompt | llm
    final_response = final_chain.invoke({"text": combined})
    return final_response.content