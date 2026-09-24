from langchain_core.tools import tool

@tool
def search(keyword: str) -> str:
    """
    搜索本地知识库。
    当用户询问 Agent、Python 等知识时使用。
    """
    data = {
        "Python": "Python 是一种高级编程语言。",
        "Agent": "Agent 是能够根据任务自主决定并调用工具完成任务的 AI 应用。",
    }
    return data.get(
        keyword,
        "没有找到相关信息"
    )