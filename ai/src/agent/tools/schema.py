from pydantic import BaseModel

class ToolCallSchema(BaseModel):
    name: str
    arguments: dict
