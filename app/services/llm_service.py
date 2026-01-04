# app/services/llm_service.py

from app.llm.loader import load_llm
from google.api_core.exceptions import ResourceExhausted


class LLMService:

    def __init__(self):
        self.llm = load_llm()

    def generate(self, prompt: str):
        try:
            return self.llm.chat(prompt)
        except ResourceExhausted:
            return "⚠️ AI service temporarily unavailable. Please retry."
