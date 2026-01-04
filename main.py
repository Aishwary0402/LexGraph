# 🔥 MUST BE FIRST — BEFORE ANY OTHER IMPORT
# app/main.py
import os

# 🔥 MUST BE FIRST LINES
os.environ["HF_HUB_DISABLE_SSL_VERIFICATION"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["REQUESTS_CA_BUNDLE"] = ""
os.environ["CURL_CA_BUNDLE"] = ""
os.environ["SSL_CERT_FILE"] = ""



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.qa_router import router as qa_router

app = FastAPI(
    title="LexGraph Backend",
    version="2.0",
    description="Unified Legal Reasoning System using RAG + SHAP + Neo4j + Gemini"
)

# -------------------------------
# CORS (important for frontend later)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # change to frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Include Unified Route
# -------------------------------
app.include_router(qa_router, prefix="/api", tags=["Unified Pipeline"])

# -------------------------------
# Root endpoint
# -------------------------------
@app.get("/")
def home():
    return {"message": "LexGraph backend is running successfully 🚀"}
