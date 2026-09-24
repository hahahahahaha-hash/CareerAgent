import json

from langchain_core.tools import tool

from app.agent.llm import llm
from app.rag.vector_store import search_resume
from pydantic import BaseModel, Field


class SkillMatchResult(BaseModel):
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    related_experience: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)

@tool
def match_resume_with_jd(jd_text: str) -> str:
    """
    根据职位 JD 检索简历中的相关经历，
    并分析用户与该岗位的技能匹配情况。
    """

    # 1. 从简历知识库检索相关内容
    documents = search_resume(
        "岗位要求和技能：" + jd_text,
        k=5
    )

    if not documents:
        return "简历中没有找到相关信息。"

    # 2. 拼接简历相关内容
    resume_context = "\n\n".join(
        document.page_content
        for document in documents
    )

    # 3. 构造分析 Prompt
    prompt = f"""
你是一名求职分析助手。

请根据下面的【职位 JD】和【简历相关内容】，
分析用户与该岗位的技能匹配情况。

要求：

1. 只能根据提供的 JD 和简历内容进行分析。
2. 不要编造用户没有出现过的经历。
3. 区分“已经具备”和“JD 要求但简历中没有明确体现”的技能。
4. 给出具体的匹配依据。
5. 只返回 JSON。
6. 不要返回 Markdown。
7. 不要使用 ```json 代码块。

JSON 格式必须严格遵循：

{{
    "matched_skills": [],
    "missing_skills": [],
    "related_experience": [],
    "suggestions": []
}}

【职位 JD】

{jd_text}

【简历相关内容】

{resume_context}
"""

    # 4. 调用 LLM
    response = llm.invoke(prompt)

    # 5. 解析 JSON + Pydantic 校验
    try:
        data = json.loads(response.content)

        result = SkillMatchResult.model_validate(data)

        return result.model_dump_json(
            ensure_ascii=False
        )

    except Exception as e:
        return f"技能匹配结果解析失败：{str(e)}"