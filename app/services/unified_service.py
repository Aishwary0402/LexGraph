# app/services/unified_service.py

from app.services.rag_service import RAGPipeline
from app.services.shap_service import SHAPExplainer
from app.services.graph_service import GraphBuilder
from app.utils.text_utils import markdown_to_html   # ✅ already imported

class UnifiedPipeline:

    def __init__(self):
        self.rag = RAGPipeline()
        self.shap = SHAPExplainer()
        self.graph = GraphBuilder()
        self.cache = {}

    def process(self, query: str, k: int = 5):

        if query in self.cache:
            return self.cache[query]

        answer, docs = self.rag.get_answer(query, k)

        shap_output = self.shap.explain_answer(
            query=query,
            answer=answer,
            docs=docs
        )

        try:
            graph_output = self.graph.build_graph(answer)
        except Exception:
            graph_output = {"nodes": [], "edges": []}

        # ✅ ADD THESE TWO LINES ONLY
        answer = markdown_to_html(answer)
        shap_output["summary"] = markdown_to_html(shap_output["summary"])

        result = {
            "answer": answer,
            "shap_explanation": shap_output,
            "graph": graph_output
        }

        self.cache[query] = result
        return result
