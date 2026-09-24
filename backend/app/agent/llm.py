from langchain_openai import ChatOpenAI

from app.core.config import settings


llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=settings.openai_api_key,
    base_url="https://api.deepseek.com",
    temperature=0.7
)