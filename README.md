# Chat with Multiple PDFs

A powerful Streamlit application that enables natural language conversations with multiple PDF documents. Built with LangChain and powered by DeepSeek AI through OpenRouter, this tool allows you to upload various PDFs and get intelligent responses to your questions about their content. Perfect for researchers, students, and professionals who need to extract information from multiple documents quickly.

![Application Architecture](PDF-LangChain.jpg)

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

The application follows a sophisticated architecture as shown in the diagram above. Here's a detailed breakdown of the process:

1. **PDF Processing Pipeline**:
   - Users upload multiple PDF files through the Streamlit interface
   - The application uses PyPDFLoader to extract text from each PDF
   - Text is split into manageable chunks using RecursiveCharacterTextSplitter
   - Each chunk is converted into embeddings using HuggingFace's sentence transformers
   - These embeddings are stored in a FAISS vector store for efficient similarity search

2. **Query Processing**:
   - When a user asks a question, the system:
     - Converts the query into embeddings
     - Performs similarity search in the FAISS vector store
     - Retrieves the most relevant chunks of text from the PDFs

3. **Response Generation**:
   - The retrieved context and user's question are sent to the DeepSeek API through OpenRouter
   - The API processes the context and question to generate a relevant response
   - The response is displayed to the user in the chat interface

4. **Key Components**:
   - **Streamlit**: Provides the user interface for file upload and chat
   - **LangChain**: Handles document loading, text splitting, and vector storage
   - **FAISS**: Enables efficient similarity search in the vector space
   - **HuggingFace**: Provides the embedding model for text-to-vector conversion
   - **DeepSeek API**: Generates intelligent responses based on the context

This architecture ensures that the application can handle multiple PDFs efficiently and provide accurate, context-aware responses to user queries.

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
