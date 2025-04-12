# Chat with Multiple PDFs

A powerful Streamlit application that enables natural language conversations with multiple PDF documents. Built with LangChain and powered by DeepSeek AI through OpenRouter, this tool allows you to upload multiple PDFs and get intelligent responses to your questions about their content. Perfect for researchers, students, and professionals who need to quickly extract information from multiple documents.

## Features

- Upload multiple PDF files
- Process PDFs using LangChain
- Chat with the content using DeepSeek API
- Real-time responses based on PDF content
- Beautiful and intuitive Streamlit interface

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Open the `app.py` file
2. Locate the following section:
```python
# OpenRouter API configuration
OPENROUTER_API_KEY = "your-api-key"
```
3. Replace the API key with your own OpenRouter API key
4. Save the file

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to `http://localhost:8501`

3. Upload one or more PDF files using the file uploader

4. Once the PDFs are processed, you can start asking questions about their content

## How it Works

1. The application uses LangChain to:
   - Load and process PDF files
   - Split the content into manageable chunks
   - Create embeddings using HuggingFace
   - Store the embeddings in a FAISS vector store

2. When you ask a question:
   - The system finds relevant content from the PDFs
   - Sends the context and your question to the DeepSeek API
   - Returns a response based on the PDF content

## Requirements

- Python 3.8+
- Streamlit
- LangChain
- PyPDF
- Requests
- FAISS
- HuggingFace Embeddings
- Sentence Transformers

## Note

The application uses the DeepSeek API through OpenRouter. Make sure you have a valid API key and sufficient credits to use the service. You can get an API key from [OpenRouter](https://openrouter.ai/). 