from langchain_openai import ChatOpenAI
from app.core.config import get_settings

settings = get_settings()

def get_fallback_chat_model(temperature: float = 0.3) -> ChatOpenAI:
    """
    Returns an instance of ChatOpenAI configured to point to OpenRouter as a fallback.
    Used if Groq experiences rate limits or downtime.
    """
    return ChatOpenAI(
        api_key=settings.OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        model="meta-llama/llama-3-8b-instruct",
        temperature=temperature,
        max_tokens=1024,
    )
