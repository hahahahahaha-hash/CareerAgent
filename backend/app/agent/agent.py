import json
from app.agent.llm import chat
from app.tools.weather import (
    weather_tool,
    get_weather
)
from app.tools.calculator import (
    calculate,
    calculator_tool
)
from app.tools.search import (
    search,
    search_tool
)

#工具列表
available_tools = [
    weather_tool,
    calculator_tool,
    search_tool
]

class Agent:
    def run(self,message):
        messages=[
            {
                "role":"user",
                "content":message
            }
        ]

        # 第一次请求LLM
        response = chat(
            messages,
            tools=available_tools
        )


        # 判断LLM是否调用工具
        if response.tool_calls:
            tool_call=response.tool_calls[0]
            args=json.loads(
                tool_call.function.arguments
            )

            # 执行工具
            tool_map = {
                "get_weather": get_weather,
                "calculate": calculate,
                "search": search
            }
            function_name=tool_call.function.name
            function = tool_map[function_name]
            args = json.loads(
                tool_call.function.arguments
            )
            print("工具名称:", function_name)
            print("工具参数:", args)
            result = function(**args)

            # 把工具结果告诉LLM
            messages.append(response)
            messages.append({
                "role":"tool",
                "tool_call_id":
                tool_call.id,
                "content":
                result
            })
            final=chat(messages)
            return final.content
        return response.content