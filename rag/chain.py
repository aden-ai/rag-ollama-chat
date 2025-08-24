from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate

SYSTEM_PROMPT = """You are a helpful assistant answering questions strictly using the provided context.
If the answer is not contained in the context, say you don't know.
Respond concisely and cite brief quotes from the context when useful."""

QA_TEMPLATE = """{system}

Chat History:
{chat_history}

Context:
{context}

User Question:
{question}

Answer:"""

prompt = PromptTemplate(
    template=QA_TEMPLATE,
    input_variables=["system", "chat_history", "context", "question"],
    partial_variables={"system": SYSTEM_PROMPT},
)

def build_chat_chain(llm, vectordb: Chroma, top_k: int = 4):
    retriever = vectordb.as_retriever(search_kwargs={"k": top_k})
    memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer" 
    )
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt},
        return_source_documents=True,
        output_key="answer"  # ✅ explicitly set the output key
    )
    return chain
