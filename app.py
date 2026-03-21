"""
AI Research Assistant Agent - Day 2
Supports file upload and reading (TXT + PDF)
"""

import streamlit as st
from PyPDF2 import PdfReader


def read_txt(file) -> str:
    """Read text from TXT file."""
    return file.read().decode("utf-8")

def split_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """
    Split text into chunks for processing.

    Args:
        text: Full document text
        chunk_size: size of each chunk
        overlap: overlapping text between chunks

    Returns:
        List of text chunks
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

def read_pdf(file) -> str:
    """Extract text from PDF file."""
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def main() -> None:
    """Run Streamlit app."""

    st.set_page_config(
        page_title="AI Research Assistant",
        page_icon="📚",
        layout="wide"
    )

    st.title("📚 AI Research Assistant Agent")
    st.write("Upload documents and ask questions based on them.")

    st.divider()

    # File Upload
    uploaded_file = st.file_uploader(
        "Upload document (PDF or TXT)",
        type=["pdf", "txt"]
    )

    # Question Input
    query = st.text_input("Ask a question about the document:")

    # Buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔍 Get Answer"):
            st.info("AI answering will be added soon...")

    with col2:
        if st.button("🗑 Clear"):
            st.rerun()

    # Process uploaded file
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

        # Read file based on type
        if uploaded_file.type == "text/plain":
            document_text = read_txt(uploaded_file)

        elif uploaded_file.type == "application/pdf":
            document_text = read_pdf(uploaded_file)

        else:
            st.error("Unsupported file type")
            return

        # Display extracted content
        st.subheader("📄 Extracted Document Content")
        st.text_area("Content", document_text[:2000], height=200)

        # Split into chunks
        chunks = split_text(document_text)

        st.subheader("🧩 Text Chunks")

        for i, chunk in enumerate(chunks[:5]):  # show only first 5
            st.write(f"Chunk {i+1}:")
            st.code(chunk)


if __name__ == "__main__":
    main()
