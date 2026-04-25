from langchain_core.prompts import ChatPromptTemplate

summarize_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert document analyst. "
        "Summarize the following text into 3-5 concise bullet points, "
        "focusing on the key takeaways and most important information.",
    ),
    ("human", "{text}"),
])