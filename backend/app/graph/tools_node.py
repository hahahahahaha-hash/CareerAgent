from langgraph.prebuilt import ToolNode

from app.tools import jd_analyzer
from app.tools.weather import get_weather
from app.tools.calculator import calculate
from app.tools.search import search
from app.tools.jd_analyzer import analyze_jd
from app.tools.resume_search import search_resume_tool
from app.tools.skill_matcher import match_resume_with_jd

tools = [
    get_weather,
    calculate,
    search,
    analyze_jd,
    search_resume_tool,
    match_resume_with_jd
]

tool_node = ToolNode(tools)