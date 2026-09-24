from langchain_core.tools import tool
from app.rag.vector_store import search_resume

@tool
def search_resume_tool(query: str) -> str:
    """
    搜索用户简历中的相关信息。

    当用户询问自己的项目经历、技术栈、Agent 开发经验、
    工作经历、教育背景、技能等信息时，可以使用该工具。
    """

    documents = search_resume(query, k=3)

    if not documents:
        return "简历中没有找到相关信息。"

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    return context