from langchain_core.prompts import ChatPromptTemplate

STYLE_PROMPTS = {
    "bullet": (
        "You are an expert document analyst. "
        "Summarize the following text into 3-5 concise bullet points, "
        "focusing on the key takeaways and most important information."
    ),
    "paragraph": (
        "You are an expert document analyst. "
        "Summarize the following text into a clear and concise paragraph "
        "of 4-6 sentences, covering the main ideas and key takeaways."
    ),
    "executive": (
        "You are a senior business analyst. "
        "Write a professional executive summary of the following text. "
        "Include: the main topic, key findings, and recommendations. "
        "Keep it under 150 words and use formal language."
    ),
    "eli5": (
        "You are a friendly teacher explaining things to a 5 year old. "
        "Summarize the following text in very simple language, "
        "using short sentences and easy words that anyone can understand. "
        "Make it fun and engaging!"
    ),
}


def get_summarize_prompt(language: str = "English", style: str = "bullet") -> ChatPromptTemplate:
    """Return a summarization prompt for the given language and style."""
    system = STYLE_PROMPTS.get(style, STYLE_PROMPTS["bullet"])
    system += f" Write your response in {language}."

    return ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", "{text}"),
    ])