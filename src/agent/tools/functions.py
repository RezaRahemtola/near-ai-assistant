from langchain.tools import tool
from langchain_core.utils.function_calling import convert_to_openai_tool

@tool()
def search_google(_query: str):
    """Search google results.
    Args:
        query (str): The query to search for.
    Returns:
        A string with the result"""

def search_google_raw(_query: str) -> str:
    return "NearBot is an AI to help you discovering the Near Protocol"


TOOLS = [search_google]

def get_tools() -> list:
    return [convert_to_openai_tool(t) for t in TOOLS]
