from langchain_groq import ChatGroq

from app.core.config import get_settings

settings = get_settings()


def get_chat_model(temperature: float = 0.3) -> ChatGroq:
    """
    Returns an instance of ChatGroq configured with the Groq API key.
    We default to a low temperature for factual, grounded responses (e.g., 0.3).
    """
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model="llama-3.1-8b-instant",  # Defaulting to an open-weight Llama 3.1 model on Groq
        temperature=temperature,
        max_tokens=1024,
    )
