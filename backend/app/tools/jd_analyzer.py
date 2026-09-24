import json
from langchain_core.tools import tool
from app.agent.llm import llm
from app.models.jd import JobAnalysis

@tool
def analyze_jd(jd_text: str) -> str:
    """
    分析职位 JD，提取岗位名称、技术技能、
    工作职责、学历要求、经验要求和加分技能。
    """

    prompt = f"""
请分析下面的职位 JD。

请严格根据 JD 中出现的信息进行分析，不要凭空编造。

请只返回 JSON，不要返回 Markdown，
不要使用 ```json 代码块。

JSON 格式必须严格遵循：

{{
    "job_title": "岗位名称",
    "technical_skills": [],
    "responsibilities": [],
    "education": "未提及",
    "experience": "未提及",
    "bonus_skills": []
}}

职位 JD：

{jd_text}
"""
    response = llm.invoke(prompt)
    try:
        data = json.loads(response.content)
        result = JobAnalysis.model_validate(data)
        return result.model_dump_json(
            ensure_ascii=False
        )
    except Exception as e:
        return f"JD 分析结果解析失败：{str(e)}"