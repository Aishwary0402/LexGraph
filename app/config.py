# app/config.py
import os
from pathlib import Path

import ssl

# 🔴 NUCLEAR SSL BYPASS (UNSAFE)
ssl._create_default_https_context = ssl._create_unverified_context

os.environ["HF_HUB_DISABLE_SSL_VERIFICATION"] = "1"
os.environ["REQUESTS_CA_BUNDLE"] = ""
os.environ["CURL_CA_BUNDLE"] = ""
os.environ["SSL_CERT_FILE"] = "" 

# --------------------------------------------------
# NORMAL CONFIG
# --------------------------------------------------

from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):

    GOOGLE_API_KEY: str = "AIzaSyBE7j8iFTlod3sOwyHDaautdN8OeBx6Xcw"
    LLM_MODEL: str = "gemini-2.5-flash"

    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "Aishwary-04"

    VECTOR_DB_PATH: str = str(PROJECT_ROOT / "data" / "vector_db")
    CHROMA_DB_DIR: str = VECTOR_DB_PATH

    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-MiniLM-L6-v2"

    class Config:
        env_file = ".env"


settings = Settings()
