# app/services/graph_service.py

from neo4j import GraphDatabase
from app.services.llm_service import LLMService
from app.config import settings
import json
import re
import uuid


class GraphBuilder:

    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
        self.llm = LLMService()

    def build_graph(self, answer: str):
        """
        Build a structured legal reasoning graph from the final answer.
        """

        # -------------------------------
        # STEP 1: Ask LLM for structured reasoning
        # -------------------------------
        prompt = f"""
You are a legal knowledge graph extractor.

Given the legal answer below, extract a reasoning graph.

Answer:
{answer}

Return STRICT JSON only with this schema:
{{
  "answer_node": {{
    "label": "Short title of the final answer"
  }},
  "evidence": [
    {{ "label": "Short evidence phrase" }}
  ],
  "laws": [
    {{ "label": "Law or Act name" }}
  ],
  "sections": [
    {{ "label": "Section reference" }}
  ],
  "remedies": [
    {{ "label": "Legal remedy or action" }}
  ]
}}
"""

        raw = self.llm.generate(prompt) 

        # -------------------------------
        # STEP 2: Extract JSON safely
        # -------------------------------
        match = re.search(r"\{.*\}", raw, re.S)
        if not match:
            return {"nodes": [], "edges": []}

        try:
            structured = json.loads(match.group())
        except Exception:
            return {"nodes": [], "edges": []}

        # -------------------------------
        # STEP 3: Build nodes & edges
        # -------------------------------
        nodes = []
        edges = []

        def nid():
            return str(uuid.uuid4())

        # ---- Answer node (CENTER)
        answer_id = nid()
        nodes.append({
            "id": answer_id,
            "label": structured.get("answer_node", {}).get(
                "label", "Final Legal Answer"
            )[:60],
            "full_text": answer,
            "type": "ANSWER",
            "level": 0
        })

        # ---- Evidence nodes
        for ev in structured.get("evidence", []):
            ev_id = nid()
            nodes.append({
                "id": ev_id,
                "label": ev["label"][:60],
                "full_text": ev["label"],
                "type": "EVIDENCE",
                "level": 1
            })
            edges.append({
                "source": ev_id,
                "target": answer_id,
                "relation": "SUPPORTS"
            })

        # ---- Law nodes
        for law in structured.get("laws", []):
            law_id = nid()
            nodes.append({
                "id": law_id,
                "label": law["label"][:60],
                "full_text": law["label"],
                "type": "LAW",
                "level": 2
            })
            edges.append({
                "source": law_id,
                "target": answer_id,
                "relation": "GOVERNS"
            })

        # ---- Section nodes
        for sec in structured.get("sections", []):
            sec_id = nid()
            nodes.append({
                "id": sec_id,
                "label": sec["label"][:60],
                "full_text": sec["label"],
                "type": "SECTION",
                "level": 3
            })
            edges.append({
                "source": sec_id,
                "target": answer_id,
                "relation": "DERIVED_FROM"
            })

        # ---- Remedy nodes
        for rem in structured.get("remedies", []):
            rem_id = nid()
            nodes.append({
                "id": rem_id,
                "label": rem["label"][:60],
                "full_text": rem["label"],
                "type": "REMEDY",
                "level": 4
            })
            edges.append({
                "source": answer_id,
                "target": rem_id,
                "relation": "LEADS_TO"
            })

        # -------------------------------
        # STEP 4: Store in Neo4j
        # -------------------------------
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

            for node in nodes:
                session.run(
                    """
                    CREATE (n:Entity {
                        id: $id,
                        label: $label,
                        full_text: $full_text,
                        type: $type,
                        level: $level
                    })
                    """,
                    **node
                )

            for edge in edges:
                session.run(
                    """
                    MATCH (a:Entity {id: $source})
                    MATCH (b:Entity {id: $target})
                    CREATE (a)-[:RELATION {type: $relation}]->(b)
                    """,
                    **edge
                )

        # -------------------------------
        # STEP 5: Return to frontend
        # -------------------------------
        return {
            "nodes": nodes,
            "edges": edges
        }
