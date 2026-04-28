import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
)

# ✅ Pydantic model - ορίζει την ακριβή δομή του JSON
class DocumentSummary(BaseModel):
    title: str = Field(description="A generated title for the document")
    summary: str = Field(description="The actual summarization of the document")
    summary_length: int = Field(description="The length of the generated summary in words")
    category: str = Field(description="The document category (e.g. Legal, Technical, Academic)")
    keywords: list[str] = Field(description="A list of relevant keywords from the document")

# ✅ LLM με forced structured output
structured_llm = llm.with_structured_output(DocumentSummary)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert document analyst. Analyze the following document and extract structured information."),
    ("human", "{text}")
])

chain = prompt | structured_llm


async def get_structured_summary(text: str) -> DocumentSummary:
    result = await chain.ainvoke({"text": text})
    return result