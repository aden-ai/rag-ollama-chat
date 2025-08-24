# 📚 Document Query with Ollama + LangChain + Streamlit  

This project is a simple **RAG (Retrieval-Augmented Generation) app** that lets you upload documents and chat with them using **Ollama** as the LLM. It uses **LangChain**, **FAISS**, and **Streamlit** to build an interactive interface.  

---

## 🚀 Features  
- Upload `.pdf`, `.txt`, or `.docx` documents  
- Build or load a **FAISS vector index** for fast retrieval  
- Query documents with **Ollama models** (e.g., `llama3:latest`)  
- Maintain **chat history** with memory  
- Display **sources/snippets** for transparency  

---

## 🛠️ Tech Stack  
- **LangChain** → Conversational Retrieval Chain, memory, prompts  
- **Ollama** → Local LLM backend  
- **FAISS** → Vector store for document embeddings  
- **Streamlit** → UI for uploads, chat, and settings  
- **HuggingFace Embeddings** → For text vectorization  

---

## 📦 Installation  

# Clone repo
git clone https://github.com/aden-ai/rag-ollama-chat.git
cd document-query

# Create venv (optional but recommended)
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

# Install dependencies
pip install streamlit langchain langchain-community langchain-huggingface langchain-ollama faiss-cpu sentence-transformers pypdf python-docx requests

# Make sure Ollama is installed & running
ollama run llama3

# Start the app
streamlit run app.py
