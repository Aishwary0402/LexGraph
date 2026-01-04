from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text: str, chunk_size=1000, overlap=150):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )
    return splitter.split_text(text)
