import tiktoken

def count_tokens(text: str, model_name: str = "gpt-3.5-turbo") -> int:
    """
    Estimates the number of tokens in a text string.
    Note: For Groq Llama 3 models, a specific llama tokenizer should be used,
    but tiktoken is a widely accepted proxy for general token estimation if standard.
    """
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))
