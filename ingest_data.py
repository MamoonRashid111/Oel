import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import chromadb

# Configuration
CHROMA_PATH = "chroma_db"
MODEL_NAME = "qwen2.5:3b"
BASE_URL = "http://localhost:11434"

def get_embeddings():
    return OllamaEmbeddings(model=MODEL_NAME, base_url=BASE_URL)

def ingest_document(file_path: str):
    """Ingests a document, chunks it, and adds it to the vector store."""
    
    # Load document
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.txt'):
        loader = TextLoader(file_path)
    elif file_path.endswith('.docx'):
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError("Unsupported file format")

    documents = loader.load()
    
    # Metadata Enrichment
    for doc in documents:
        doc.metadata["source_file"] = os.path.basename(file_path)
        doc.metadata["file_type"] = file_path.split('.')[-1]

    # Semantic Chunking (using RecursiveCharacterTextSplitter as a proxy for better control)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(documents)

    # Initialize ChromaDB
    embeddings = get_embeddings()
    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
        collection_name="medical_docs"
    )

    # Add chunks to vector store
    vector_store.add_documents(chunks)
    print(f"Successfully ingested {len(chunks)} chunks from {file_path}")

def ingest_base_knowledge():
    """Ingests the default medical knowledge file after clearing the existing base data."""
    base_file = "medical_knowledge.txt"
    if os.path.exists(base_file):
        print(f"Initializing vector store with base knowledge: {base_file}")
        embeddings = get_embeddings()
        vector_store = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings,
            collection_name="medical_docs"
        )
        
        # Clear base knowledge entries to prevent duplicates (by filtering on the source name)
        # Note: In a simple setup, we can also just delete the collection or the specific source.
        # Here we'll delete any documents where source_file is medical_knowledge.txt
        vector_store.delete(where={"source_file": base_file})
        
        ingest_document(base_file)
    else:
        print(f"Base knowledge file {base_file} not found. Skipping initialization.")

if __name__ == "__main__":
    # Initialize with base knowledge if the script is run directly
    ingest_base_knowledge()
