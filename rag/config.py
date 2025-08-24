import os

class Settings:
    
    MODEL_NAME = os.getenv("MODEL_NAME", "llama3:latest")
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "vectorstore")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CHROMA_DIR = os.path.join(BASE_DIR, "chroma")
    UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
    DATA_DIR = os.path.join(BASE_DIR, "data")


os.makedirs(Settings.CHROMA_DIR, exist_ok=True)
os.makedirs(Settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(Settings.DATA_DIR, exist_ok=True)

settings = Settings()
