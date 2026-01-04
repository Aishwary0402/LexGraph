# app/services/rag_service.py

from app.utils.vectorstore import get_vectorstore
from app.services.llm_service import LLMService


class RAGPipeline:

    def __init__(self):
        self.db = get_vectorstore()
        self.llm = LLMService()

    def retrieve(self, query: str, k: int = 5):
        retriever = self.db.as_retriever(search_kwargs={"k": k})
        return retriever.invoke(query)

    def get_answer(self, query: str, k: int = 5):
        docs = self.retrieve(query, k)

        context = "\n\n".join(
            [f"LEGAL SOURCE:\n{d.page_content}" for d in docs]
        )

        prompt = f"""
You are an Indian legal expert.

Answer the question STRICTLY using the legal sources below.
These sources are authoritative.

{context}

Question:
{query}

Rules:
- Do NOT mention documents, snippets, or sources
- Do NOT say "provided context"
- Produce a clear, complete legal answer
"""

        answer = self.llm.generate(prompt)
        return answer, docs
