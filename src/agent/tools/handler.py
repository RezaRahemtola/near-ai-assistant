import json
import re

from logger import logger

def parse_json(message: str):
    message = message[next(i for i, char in enumerate(message) if char in "{["):]
    try:
        return json.loads(message)
    except json.JSONDecodeError as e:
        return json.loads(message[:e.pos])

class ToolsHandler:
    def __init__(self):
        # TODO: fetch tools with a function
        self.tools = []
        self.line_separator = "\n"


    def extract_tool_calls(self, message: str) -> list:
        tool_calls = []

        try:
            json_data = parse_json(message)
            if 'arguments' in json_data and 'name' in json_data:
                tool_calls.append(json_data)
        except Exception:
            pass

        return tool_calls

    def complete(self, message: str, depth: int) -> str | None:
        tool_calls = self.extract_tool_calls(message)
        tool_message = f"Current call depth: {depth}{self.line_separator}"
        if len(tool_calls) > 0:
            tool_message += f"<tool_response>{self.line_separator}{"NearBot is a French AI agent to help with user queries"}{self.line_separator}</tool_response>{self.line_separator}"
            return tool_message
        # TODO: handle errors in this elif
        elif False:
            tool_message += f"<tool_response>{self.line_separator}There was an error parsing function calls{self.line_separator}Here's the error stack trace: {error_message}{self.line_separator}Please call the function again with correct syntax within XML tags <tool_call></tool_call>{self.line_separator}</tool_response>{self.line_separator}"
            return tool_message
        return None
