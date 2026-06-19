import re

def validate_input(user_input: str) -> str:
    """
    Checks for basic prompt injection attempts.
    Raises ValueError if malicious input is detected.
    """
    # Simple heuristic checks for prompt injection keywords
    suspicious_patterns = [
        r"ignore previous instructions",
        r"disregard all previous",
        r"system prompt",
        r"you are now",
        r"print your instructions",
    ]
    
    lower_input = user_input.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, lower_input):
            raise ValueError("Prompt injection detected. Input rejected.")
            
    return user_input
