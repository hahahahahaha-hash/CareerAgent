from app.rag.vector_store import search_resume
from app.agent.llm import llm

def ask_resume(question: str) -> str:
    documents = search_resume(question, k=3)
    context = "\n\n".join(
        document.page_content
        for document in documents
    )
    prompt = f"""
你是一个求职助手。
请严格根据下面提供的简历内容回答用户问题。
不要编造简历中没有出现的信息。
如果简历中没有相关信息，请明确告诉用户：
“简历中没有找到相关信息。”
【简历相关内容】
{context}
【用户问题】
{question}
"""
    response = llm.invoke(prompt)
    return response.content