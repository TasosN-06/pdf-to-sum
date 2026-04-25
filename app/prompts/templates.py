from langchain_core.prompts import ChatPromptTemplate


def get_summarize_prompt(language: str = "English") -> ChatPromptTemplate:
    """Return a summarization prompt for the given language."""
    return ChatPromptTemplate.from_messages([
        (
            "system",
            f"You are an expert document analyst. "
            f"Summarize the following text into 3-5 concise bullet points, "
            f"focusing on the key takeaways and most important information. "
            f"Write your response in {language}.",
        ),
        ("human", "{text}"),
    ])