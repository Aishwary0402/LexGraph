import os
import fitz
from tqdm import tqdm
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.config import settings

# ----------------------------------------------------
# 🔥 FIXED: Compute backend root from THIS file's path
# ----------------------------------------------------
BACKEND_ROOT = Path(__file__).resolve().parent
DATA_DIR = BACKEND_ROOT / "data"
DOC_DIR = DATA_DIR / "documents"
DB_DIR = DATA_DIR / "vector_db"

def create_db():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
    return Chroma(
        embedding_function=embeddings,
        persist_directory=str(DB_DIR)
    )

def ingest_pdf(filepath, db):
    pdf = fitz.open(str(filepath))
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

    for page in pdf:
        text = page.get_text("text")
        if not text.strip():
            continue

        chunks = splitter.split_text(text)
        db.add_texts(
            texts=chunks,
            metadatas=[{"source": filepath.name}] * len(chunks)
        )

    pdf.close()

def main():
    print("BACKEND ROOT:", BACKEND_ROOT)
    print("DOC_DIR:", DOC_DIR)

    if not DOC_DIR.exists():
        raise FileNotFoundError(f"Documents folder not found: {DOC_DIR}")

    db = create_db()
    pdf_files = sorted([p for p in DOC_DIR.iterdir() if p.suffix.lower() == ".pdf"])

    print(f"\n📄 Found {len(pdf_files)} PDF files\n")

    for p in tqdm(pdf_files, desc="Ingesting PDFs"):
        ingest_pdf(p, db)

    db.persist()
    print("\n✅ Vector DB stored at:", DB_DIR)

if __name__ == "__main__":
    main()
