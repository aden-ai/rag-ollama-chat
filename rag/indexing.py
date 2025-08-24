import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from rag.config import settings


def get_embeddings():
    return HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)


def clean_documents(docs):
    """Remove empty or invalid documents before indexing."""
    valid_docs = []
    for d in docs:
        if d.page_content and d.page_content.strip():
            valid_docs.append(d)
    return valid_docs


def build_or_update_index(docs, index_path=settings.VECTOR_STORE_PATH, progress_cb=None):
    os.makedirs(index_path, exist_ok=True)
    embeddings = get_embeddings()

    
    docs = clean_documents(docs)
    if not docs:
        raise ValueError("No valid documents to index. All docs were empty.")

    if os.path.exists(os.path.join(index_path, "index.faiss")):
        
        if progress_cb:
            progress_cb("Loading existing FAISS index...", 20)
        vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

        if progress_cb:
            progress_cb("Adding documents to existing index...", 50)
        vector_store.add_documents(docs)
    else:
        
        if progress_cb:
            progress_cb("Creating new FAISS index...", 30)
        vector_store = FAISS.from_documents(docs, embeddings)

    
    if progress_cb:
        progress_cb("Saving index...", 90)
    vector_store.save_local(index_path)

    if progress_cb:
        progress_cb("Index build complete ✅", 100)

    return vector_store


def load_existing_index(index_path=settings.VECTOR_STORE_PATH):
    if os.path.exists(os.path.join(index_path, "index.faiss")):
        embeddings = get_embeddings()
        return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    return None
