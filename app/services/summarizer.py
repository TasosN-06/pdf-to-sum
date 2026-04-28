import os
import asyncio
from langchain_groq import ChatGroq
from app.prompts.templates import get_summarize_prompt

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
)

CHUNK_SIZE = 4_000


def chunk_text(text: str) -> list[str]:
    words = text.split()
    return [
        " ".join(words[i:i + CHUNK_SIZE])
        for i in range(0, len(words), CHUNK_SIZE)
    ]


async def summarize_text_stream(text: str, language: str = "English", style: str = "bullet"):
    words = text.split()

    if len(words) <= CHUNK_SIZE:
        prompt = get_summarize_prompt(language, style)
        chain = prompt | llm
        async for chunk in chain.astream({"text": text}):
            if chunk.content:
                yield chunk.content
        return

    # ✅ TASK 1: Parallel chunk processing με asyncio.gather()
    chunks = chunk_text(text)
    prompt = get_summarize_prompt(language, style)
    chain = prompt | llm

    tasks = [chain.ainvoke({"text": chunk}) for chunk in chunks]
    results = await asyncio.gather(*tasks)

    chunk_summaries = [
        f"Part {i+1}:\n{result.content}"
        for i, result in enumerate(results)
    ]

    combined = "\n\n".join(chunk_summaries)
    final_prompt = get_summarize_prompt(language, style)
    final_chain = final_prompt | llm
    async for chunk in final_chain.astream({"text": combined}):
        if chunk.content:
            yield chunk.content 
