import os
from langchain_groq import ChatGroq
from app.prompts.templates import summarize_prompt


# Initialize the Groq LLM with LLaMA 3.3 70B
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
)

# Chain: prompt -> LLM
chain = summarize_prompt | llm


def summarize_text(text: str) -> str:
    """Truncate text if needed and send it to Groq for summarization."""
    # Truncate to 12,000 words to stay within the model's context window
    words = text.split()
    if len(words) > 12_000:
        text = " ".join(words[:12_000])

    response = chain.invoke({"text": text})
    return response.content