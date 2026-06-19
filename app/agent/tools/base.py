from typing import Any, Callable, Dict, Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class ECommerceTool(BaseTool):
    """
    Base class for tools in the AI Assistant.
    Provides standard error handling and uniform interface for LangGraph nodes.
    """
    name: str
    description: str
    args_schema: Type[BaseModel]

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("ECommerceTool only supports async execution.")

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        try:
            return await self.execute(*args, **kwargs)
        except Exception as e:
            return f"Error executing tool {self.name}: {str(e)}"
            
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Override this method to implement the tool logic."""
        raise NotImplementedError("Tool execution logic not implemented.")
