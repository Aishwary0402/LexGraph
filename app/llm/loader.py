import google.generativeai as genai
from app.config import settings

class GeminiAdapter:
    def __init__(self, model_name: str):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(model_name)

    def chat(self, prompt: str):
        response = self.model.generate_content(prompt)
        return response.text

def load_llm():
    return GeminiAdapter(settings.LLM_MODEL)
