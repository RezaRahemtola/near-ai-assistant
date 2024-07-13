from langchain.tools import tool
from langchain_core.utils.function_calling import convert_to_openai_tool

@tool()
def search_google(message: str) -> str:
    """Search on Google"""
    print("here")
    return "fake"

def get_tools() -> list:
    tools = [search_google]
    return [convert_to_openai_tool(t) for t in tools]
