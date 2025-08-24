import streamlit as st
from typing import List, Dict

def sidebar_controls(available_models: List[str]):
    st.sidebar.header("⚙️ Settings")
    model = st.sidebar.selectbox(
        "Model",
        options=available_models,
        index=available_models.index("llama3:latest") if "llama3:latest" in available_models else 0
    )
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.2, 0.05)
    top_k = st.sidebar.slider("Top-K Chunks", 2, 10, 4, 1)
    if st.sidebar.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    return model, temperature, top_k

def render_chat(messages: List[Dict[str, str]]):
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

def add_message(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})

def progress_bar():
    bar = st.progress(0.0, text="Preparing...")
    def update(text: str, percent: float):
        fraction = min(max(percent / 100, 0.0), 1.0)
        bar.progress(fraction, text=text)
    return update


