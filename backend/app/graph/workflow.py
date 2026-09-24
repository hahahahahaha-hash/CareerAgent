from langgraph.graph import StateGraph, END

from app.graph.state import AgentState
from app.graph.nodes import agent_node
from app.graph.tools_node import tool_node
from app.graph.router import should_continue
from langgraph.checkpoint.memory import InMemorySaver

graph = StateGraph(AgentState)

graph.add_node(
    "agent",
    agent_node
)

graph.add_node(
    "tools",
    tool_node
)

graph.set_entry_point("agent")

graph.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "end": END,
    }
)

graph.add_edge(
    "tools",
    "agent"
)

app_graph = graph.compile()
checkpointer = InMemorySaver()
app_graph = graph.compile(
    checkpointer=checkpointer
)

print(
    app_graph.get_graph().draw_mermaid()
)