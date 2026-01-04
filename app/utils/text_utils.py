import re

def markdown_to_html(text: str) -> str:
    if not text:
        return text
    # Convert **bold** to <strong>bold</strong>
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    return text
