from langgraph.graph import StateGraph
from services.rag_service import RAGPipeline
from backend.app.services.graph_service import Neo4jService
from llm.loader import load_llm
import json, re

rag = RAGPipeline()
neo = Neo4jService()
llm = load_llm()

def rag_node(state):
    question = state["question"]
    answer, docs = rag.get_answer(question, k=state.get("top_k", 5))
    return {"docs": docs, "rag_answer": answer}

def suggest_node(state):
    question = state["question"]
    docs = state["docs"]

    prompt = f"Suggest next legal steps in JSON for:\n{question}"
    resp = llm.chat(prompt)

    try:
        m = re.search(r'\[(.*?)\]', str(resp), re.S)
        actions = json.loads(f"[{m.group(1)}]")
    except:
        actions = ["Consult lawyer"]

    case_id = f"case_{abs(hash(question))}"
    neo.create_case_graph(case_id, question, docs, actions)

    return {"actions": actions, "case_id": case_id}

workflow = StateGraph()
workflow.add_node("rag", rag_node)
workflow.add_node("suggest", suggest_node)

workflow.add_edge("rag", "suggest")
workflow.set_entry_point("rag")

agent = workflow.compile()
