from app.report.word_generator import create_word_report


if __name__ == "__main__":
    create_word_report(
        title="AI 岗位匹配分析报告",
        content="""
岗位名称：AI Agent 开发工程师

已掌握技能：
Python
FastAPI
LangChain
LangGraph
RAG

技能缺口：
Redis
Kubernetes
""",
        output_path="test_report.docx"
    )

    print("Word 报告生成成功")