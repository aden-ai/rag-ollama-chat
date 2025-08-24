import os
import tempfile
from typing import List
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader

SUPPORTED_EXTS = (".pdf", ".txt", ".docx")

def save_uploaded_to_temp(uploaded_file) -> str:
    suffix = os.path.splitext(uploaded_file.name)[1]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded_file.read())
    tmp.flush()
    tmp.close()
    return tmp.name

def load_file(path: str) -> List[Document]:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(path)
    elif ext == ".txt":
        loader = TextLoader(path, encoding="utf-8")
    elif ext == ".docx":
        loader = Docx2txtLoader(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    return loader.load()

def load_many(paths: List[str]) -> List[Document]:
    all_docs: List[Document] = []
    for p in paths:
        docs = load_file(p)
        all_docs.extend(docs)
    return all_docs
