class ToolsHandler:
    def __init__(self):
        # TODO: fetch tools with a function
        self.tools = []
        self.line_separator = "\n"

    def complete(self, _message: str, depth: int) -> str | None:
        tool_calls = []
        tool_message = f"Current call depth: {depth}{self.line_separator}"
        if len(tool_calls) > 0:
            # TODO: execute tool and handle response
            _tmp = 42
        # TODO: handle errors in this elif
        elif False:
            tool_message += f"<tool_response>{self.line_separator}There was an error parsing function calls{self.line_separator}Here's the error stack trace: {error_message}{self.line_separator}Please call the function again with correct syntax within XML tags <tool_call></tool_call>{self.line_separator}</tool_response>{self.line_separator}"
            return tool_message
        return None
