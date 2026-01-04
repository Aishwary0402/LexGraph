from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.config import settings


emb = None
db = None


def get_vectorstore():
    global emb, db

    # Load embedding model once
    if emb is None:
        emb = HuggingFaceEmbeddings(
    model_name=settings.EMBEDDING_MODEL,
    model_kwargs={"local_files_only": True}
)

    # Load Chroma DB once
    if db is None:
        db = Chroma(
            persist_directory=settings.CHROMA_DB_DIR,
            embedding_function=emb
        )

    return db  # IMPORTANT: return only Chroma object
