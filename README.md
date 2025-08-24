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

## ⚡ Quick Start

Get up and running in minutes 🚀

```bash
# 1️⃣ Clone the repo
git clone https://github.com/aden-ai/rag-ollama-chat.git
cd rag-ollama-chat

# 2️⃣ Create & activate virtual environment
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3️⃣ Install dependencies
pip install streamlit langchain langchain-community langchain-huggingface langchain-ollama faiss-cpu sentence-transformers pypdf python-docx requests

# 4️⃣ Run Ollama (make sure it's installed)
ollama run llama3

# 5️⃣ Launch the app 🎉
streamlit run app.py
