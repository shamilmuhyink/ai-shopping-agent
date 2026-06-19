import json
from typing import AsyncGenerator

async def format_sse(generator: AsyncGenerator[str, None]) -> AsyncGenerator[str, None]:
    """
    Formats tokens yielded by the LangGraph/LLM stream into Server-Sent Events (SSE) format.
    """
    async for chunk in generator:
        yield f"data: {json.dumps({'token': chunk})}\n\n"
    yield "data: [DONE]\n\n"
