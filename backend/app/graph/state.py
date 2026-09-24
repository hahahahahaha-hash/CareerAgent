from typing import TypedDict, Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

from app.models.jd import JobAnalysis
from app.tools.skill_matcher import SkillMatchResult


class AgentState(TypedDict, total=False):
    messages: Annotated[
        list[AnyMessage],
        add_messages
    ]

    # 求职 Agent 工作流状态
    jd_text: str
    job_analysis: JobAnalysis
    skill_match: SkillMatchResult
    final_report: str