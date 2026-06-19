import re

def redact_pii(text: str) -> str:
    """
    Redacts Personally Identifiable Information (PII) like phone numbers and emails
    from conversation logs before storing them in the database.
    """
    # Redact Emails
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    text = re.sub(email_pattern, '[EMAIL REDACTED]', text)
    
    # Redact Phone Numbers (Basic 10-digit formats)
    phone_pattern = r'\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\b'
    text = re.sub(phone_pattern, '[PHONE REDACTED]', text)
    
    # Redact Credit Cards (Basic 16 digit formats)
    cc_pattern = r'\b(?:\d[ -]*?){13,16}\b'
    text = re.sub(cc_pattern, '[CARD REDACTED]', text)
    
    return text
