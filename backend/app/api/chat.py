from fastapi import APIRouter
from app.graph.workflow import app_graph

router = APIRouter()


@router.get("/chat")
def chat(message: str):
    result = app_graph.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": "demo_user_001"
            }
        }
    )

    return {
        "answer": result["messages"][-1].content
    }