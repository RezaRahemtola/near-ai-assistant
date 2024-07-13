import json
import os
import sys

from logger import logger
from .functions import get_tools

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
import functions

def parse_json(message: str):
    message = message[next(i for i, char in enumerate(message) if char in "{["):]
    try:
        return json.loads(message)
    except json.JSONDecodeError as e:
        return json.loads(message[:e.pos])

class ToolsHandler:
    def __init__(self):
        self.tools = get_tools()
        self.line_separator = "\n"


    def extract_tool_calls(self, message: str) -> list[dict]:
        tool_calls = []

        try:
            json_data = parse_json(message)
            if 'arguments' in json_data and 'name' in json_data:
                tool_calls.append(json_data)
        except Exception:
            pass

        return tool_calls

    async def execute_tool_call(self, tool_call: dict) -> str:
        function_name = tool_call.get("name")
        # TODO: Not working without this _raw, try to fix it later
        function_to_call = getattr(functions, f"{function_name}_raw", None)
        function_args = tool_call.get("arguments", {})
        logger.debug(f"ToolsHandler::execute_tool_call: {function_name} with {function_args}")

        if not function_to_call:
            raise ValueError(f"Function {function_name} not found")

        function_response = await function_to_call(*function_args.values())
        results = f'{{"name": "{function_name}", "content": {function_response}}}'
        return results

    async def complete(self, tool_calls: list[dict], depth: int) -> str | None:
        tool_message = f"Current call depth: {depth}{self.line_separator}"
        if len(tool_calls) > 0:
            for tool_call in tool_calls:
                try:
                    function_response = await self.execute_tool_call(tool_call)
                    tool_message += f"<tool_response>{self.line_separator}{function_response}{self.line_separator}</tool_response>{self.line_separator}"
                except Exception as e:
                    tool_name = tool_call.get("name")
                    tool_message += f"<tool_response>{self.line_separator}There was an error when executing the function: {tool_name}{self.line_separator}Here's the error traceback: {e}{self.line_separator}Please call this function again with correct arguments within XML tags <tool_call></tool_call>{self.line_separator}</tool_response>{self.line_separator}"
            return tool_message
        return None
