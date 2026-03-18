"""
AI Research Assistant Agent - Day 1 UI
"""

import streamlit as st


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

    # Show file info
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")


if __name__ == "__main__":
    main()