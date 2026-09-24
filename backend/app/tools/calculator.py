from langchain_core.tools import tool

@tool
def calculate(expression: str) -> str:
    """
    执行数学计算。
    当用户提出数学计算、算式求值等请求时使用。
    """
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算失败：{e}"