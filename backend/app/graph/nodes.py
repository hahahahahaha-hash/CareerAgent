from app.agent.llm import llm
from app.graph.tools_node import tools

llm_with_tools = llm.bind_tools(tools)

def agent_node(state):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {
        "messages": [response]
    }