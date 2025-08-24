import os
import streamlit as st

from rag.config import settings
from rag.loaders import save_uploaded_to_temp, load_many, SUPPORTED_EXTS
from rag.indexing import build_or_update_index, load_existing_index
from rag.llm import check_ollama_health, get_llm
from rag.chain import build_chat_chain
from rag.ui import sidebar_controls, render_chat, add_message, progress_bar

st.set_page_config(page_title="Document Query", layout="wide")
st.title("📚 Document Query")

# Session state init
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Ollama health check ---
ok, msg, models = check_ollama_health()
if not ok:
    st.error(msg)
    st.stop()
st.success("✅ " + msg)

# Sidebar controls (model / temp / top-k)
model_name, temperature, top_k = sidebar_controls(models)

# Upload zone
st.subheader("📤 Upload documents")
uploaded_files = st.file_uploader(
    f"Drop your files here ({', '.join(SUPPORTED_EXTS)})",
    type=[e.strip(".") for e in SUPPORTED_EXTS],
    accept_multiple_files=True
)

# Build / load index buttons
col1, col2 = st.columns([1, 1], vertical_alignment="center")
with col1:
    build_btn = st.button("⚡ Build/Update Index", use_container_width=True)
with col2:
    load_btn = st.button("📦 Load Existing Index", use_container_width=True)

vectordb = None

# Handle build/update
if build_btn:
    if not uploaded_files:
        st.warning("Please upload at least one file to build the index.")
        st.stop()

    # Save uploads to temp and load
    tmp_paths = [save_uploaded_to_temp(f) for f in uploaded_files]
    docs = load_many(tmp_paths)

    progress = progress_bar()
    vectordb = build_or_update_index(docs, progress_cb=progress)
    st.success("Index built & persisted to disk ✅")

# Handle load existing
if load_btn:
    vectordb = load_existing_index()
    if vectordb:
        st.success("Loaded existing index from disk ✅")
    else:
        st.warning("No existing index found. Please build it first.")

# If neither button clicked yet, try to auto-load if the store exists
if not vectordb and os.path.isdir(settings.VECTOR_STORE_PATH):
    try:
        vectordb = load_existing_index()
        if vectordb:
            st.info("Auto-loaded existing index.")
    except Exception:
        pass

st.divider()

# Chat UI
st.subheader("💬 Chat with your documents")
render_chat(st.session_state.messages)

if prompt := st.chat_input("Ask something about your documents..."):
    add_message("user", prompt)

    if vectordb is None:
        st.warning("Please build or load an index first.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                llm = get_llm(model_name=model_name, temperature=temperature)
                chain = build_chat_chain(llm, vectordb, top_k=top_k)

                # ✅ use invoke() (new API)
                result = chain.invoke({"question": prompt})
                answer = result["answer"]

                if not answer:
                    st.warning("⚠️ No answer generated. Enable sources below to inspect context.")
                else:
                    st.markdown(answer)

                # Show sources (if any)
                sources = result.get("source_documents", [])
                if sources:
                    with st.expander("🔎 Sources"):
                        for i, doc in enumerate(sources, start=1):
                            st.markdown(f"**Source {i}:**")
                            st.write(doc.metadata.get("source", "uploaded file"))
                            snippet = doc.page_content[:1000]
                            st.code(snippet)

        add_message("assistant", answer or "⚠️ No answer generated.")
