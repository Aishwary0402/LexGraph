# app/services/shap_service.py

import shap
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from langchain_huggingface import HuggingFaceEmbeddings
from app.services.llm_service import LLMService
from app.config import settings
import json, re


class SHAPExplainer:

    def __init__(self):
        self.emb = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )
        self.llm = LLMService()

    # --------------------------------------------------
    # LLM-based relevance scoring (INTERNAL ONLY)
    # --------------------------------------------------
    def score_docs(self, query, docs):

        prompt = f"""
You are ranking retrieved legal documents.

Query:
{query}

Score each document from 0 to 1 based on relevance.
Return ONLY a JSON list of numbers.

Documents:
"""

        for i, d in enumerate(docs):
            prompt += f"\nDOCUMENT {i}:\n{d.page_content}\n"

        raw = self.llm.generate(prompt)

        match = re.search(r"\[(.*?)\]", str(raw), re.S)
        if not match:
            return [1.0] * len(docs)

        try:
            scores = json.loads(f"[{match.group(1)}]")
            return scores if len(scores) == len(docs) else [1.0] * len(docs)
        except Exception:
            return [1.0] * len(docs)

    # --------------------------------------------------
    # SHAP explanation
    # --------------------------------------------------
    def explain_answer(self, query, answer, docs):

        if not docs:
            return {
                "summary": "No documents were retrieved to justify the answer.",
                "explanation_ranked": []
            }

        # 1️⃣ Embed documents
        X = np.array([
            self.emb.embed_query(d.page_content)
            for d in docs
        ])

        # 2️⃣ LLM-based relevance labels
        scores = self.score_docs(query, docs)
        y = np.array(scores, dtype=float)

        # 3️⃣ Train surrogate model
        model = RandomForestRegressor(
            n_estimators=40,
            random_state=42
        )
        model.fit(X, y)

        # 4️⃣ SHAP values
        background = X[:2] if len(X) > 1 else X
        explainer = shap.KernelExplainer(model.predict, background)

        shap_values = explainer.shap_values(X, nsamples=10)
        if isinstance(shap_values, list):
            shap_values = shap_values[0]

        importance = np.abs(shap_values).sum(axis=1)

        # 5️⃣ Build INTERNAL explanation objects
        explanation_ranked = []
        for i, d in enumerate(docs):
            explanation_ranked.append({
                "doc_label": f"Doc {i+1}", 
                "snippet": d.page_content[:300],
                "shap_importance": float(importance[i]),
                "llm_score": float(y[i])
            })

        explanation_ranked.sort(
            key=lambda x: x["shap_importance"],
            reverse=True
        )

        # 6️⃣ USER-FACING reasoning (NO DOC IDS)
        top_snippets = [
            f"Doc {i+1}: {e['snippet']}"
            for i, e in enumerate(explanation_ranked[:3])
        ]

        reason_prompt = f"""
You are a legal reasoning assistant.

Final Answer:
{answer}

Key legal principles derived from authoritative sources:
{top_snippets}

Explain in ONE clear paragraph why these legal principles
together justify the final answer.

Rules:
- Do NOT mention documents, indices, or sources
- Do NOT say "provided context"
- Write as a legal expert explaining reasoning
"""

        summary = self.llm.generate(reason_prompt)

        return {
            "summary": summary,
            "explanation_ranked": explanation_ranked
        }
