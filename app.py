import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import requests
import json
from typing import List
import tempfile

# Set page configuration
st.set_page_config(
    page_title="Chat with Multiple PDFs",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processed_docs" not in st.session_state:
    st.session_state.processed_docs = False
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# OpenRouter API configuration
OPENROUTER_API_KEY = "your-api-key"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def process_pdfs(pdf_files: List[st.runtime.uploaded_file_manager.UploadedFile]) -> None:
    """Process uploaded PDF files and create vector store."""
    all_docs = []
    
    for pdf_file in pdf_files:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Load PDF
        loader = PyPDFLoader(tmp_file_path)
        pages = loader.load()
        all_docs.extend(pages)
        
        # Clean up
        os.unlink(tmp_file_path)
    
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(all_docs)
    
    # Create embeddings and vector store
    embeddings = HuggingFaceEmbeddings()
    st.session_state.vector_store = FAISS.from_documents(splits, embeddings)
    st.session_state.processed_docs = True

def get_relevant_docs(query: str) -> str:
    """Get relevant documents for the query."""
    if st.session_state.vector_store:
        docs = st.session_state.vector_store.similarity_search(query, k=3)
        return "\n\n".join([doc.page_content for doc in docs])
    return ""

def get_chat_response(query: str, context: str) -> str:
    """Get response from DeepSeek API."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "Chat with PDFs"
    }
    
    prompt = f"""Context from PDFs:
{context}

User Question: {query}

Please provide a detailed answer based on the context provided. If the answer cannot be found in the context, say so."""
    
    data = {
        "model": "deepseek/deepseek-r1-distill-qwen-32b:free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    response = requests.post(OPENROUTER_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return "Error getting response from the API."

# Streamlit UI
st.title("📚 Chat with Multiple PDFs")

# File uploader
uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files and not st.session_state.processed_docs:
    with st.spinner("Processing PDFs..."):
        process_pdfs(uploaded_files)
        st.success("PDFs processed successfully!")

# Chat interface
if st.session_state.processed_docs:
    st.subheader("Chat with your PDFs")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your PDFs"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get relevant context
        context = get_relevant_docs(prompt)
        
        # Get response from API
        with st.spinner("Thinking..."):
            response = get_chat_response(prompt, context)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display the new messages
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            st.write(response)
else:
    st.info("Please upload PDF files to start chatting.") 
