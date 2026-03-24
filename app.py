"""
AI Research Assistant Agent (RAG - Complete)
"""

import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import FAISS

load_dotenv()


# -------- FILE READERS --------

def read_txt(file) -> str:
    return file.read().decode("utf-8")


def read_pdf(file) -> str:
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


# -------- TEXT CHUNKING --------

def split_text(text: str, chunk_size: int = 500, overlap: int = 100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


# -------- EMBEDDINGS + VECTOR DB --------

def create_vector_store(chunks):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store


# -------- QA FUNCTION --------

def get_answer(vector_store, query):
    docs = vector_store.similarity_search(query, k=3)

    context = "\n".join([doc.page_content for doc in docs])

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = f"""
    Answer the question based on the context below.

    Context:
    {context}

    Question:
    {query}
    """

    response = llm.invoke(prompt)

    return response.content


# -------- MAIN APP --------

def main():
    st.set_page_config(page_title="AI Research Agent", layout="wide")

    st.title("📚 AI Research Assistant Agent")
    st.write("Upload documents and ask questions based on them.")

    st.divider()

    uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
    query = st.text_input("Ask a question about the document")

    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None

    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

        if uploaded_file.type == "text/plain":
            document_text = read_txt(uploaded_file)
        elif uploaded_file.type == "application/pdf":
            document_text = read_pdf(uploaded_file)
        else:
            st.error("Unsupported file type")
            return

        st.subheader("📄 Document Preview")
        st.text_area("Content", document_text[:2000], height=200)

        # Chunking
        chunks = split_text(document_text)

        st.info(f"Created {len(chunks)} text chunks")

        # Create vector store
        st.session_state.vector_store = create_vector_store(chunks)

        st.success("Embeddings + Vector DB Ready")

    # QA Section
    if st.session_state.vector_store and query:
        if st.button("🔍 Get Answer"):
            with st.spinner("Thinking..."):
                answer = get_answer(st.session_state.vector_store, query)

            st.subheader("💡 Answer")
            st.write(answer)


if __name__ == "__main__":
    main()
