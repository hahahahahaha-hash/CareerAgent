from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """
    查询指定城市的天气。
    当用户询问某个城市的天气时使用。
    """
    weather_data = {
        "北京": "晴天，25℃",
        "上海": "多云，27℃",
        "广州": "小雨，30℃",
        "深圳": "晴天，29℃",
    }
    return weather_data.get(
        city,
        f"{city}暂无天气数据"
    )