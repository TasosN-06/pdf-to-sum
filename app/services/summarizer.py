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


async def summarize_text_stream(text: str, language: str = "English", style: str = "bullet"):
    """Stream summary tokens, with chunking for large texts."""
    words = text.split()

    # If text is small enough, stream directly
    if len(words) <= CHUNK_SIZE:
        prompt = get_summarize_prompt(language, style)
        chain = prompt | llm
        async for chunk in chain.astream({"text": text}):
            if chunk.content:
                yield chunk.content
        return

    # For large texts: chunk -> summarize each -> stream final summary
    chunks = chunk_text(text)
    chunk_summaries = []

    for i, chunk in enumerate(chunks):
        prompt = get_summarize_prompt(language, style)
        chain = prompt | llm
        response = chain.invoke({"text": chunk})
        chunk_summaries.append(f"Part {i+1}:\n{response.content}")

    # Stream the final summary
    combined = "\n\n".join(chunk_summaries)
    final_prompt = get_summarize_prompt(language, style)
    final_chain = final_prompt | llm
    async for chunk in final_chain.astream({"text": combined}):
        if chunk.content:
            yield chunk.content