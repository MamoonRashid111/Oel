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

def ingest_base_knowledge():
    """Ingests the default medical knowledge file."""
    base_file = "medical_knowledge.txt"
    if os.path.exists(base_file):
        ingest_document(base_file)
    else:
        print(f"Base knowledge file {base_file} not found.")

def ingest_document(file_path: str):
    """Ingests a document, chunks it, and adds it to the vector store."""
    from langchain_community.document_loaders import CSVLoader
    
    # Load document
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.txt'):
        loader = TextLoader(file_path)
    elif file_path.endswith('.docx'):
        loader = Docx2txtLoader(file_path)
    elif file_path.endswith('.csv'):
        loader = CSVLoader(file_path)
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

def ingest_directory(directory_path: str):
    """Ingests all supported files in a directory."""
    if not os.path.exists(directory_path):
        print(f"Directory {directory_path} not found.")
        return

    print(f"Ingesting files from {directory_path}...")
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(('.pdf', '.txt', '.docx', '.csv')):
                file_path = os.path.join(root, file)
                try:
                    ingest_document(file_path)
                except Exception as e:
                    print(f"Error ingesting {file_path}: {e}")

def reset_and_ingest_all():
    """Clears the collection and ingests everything."""
    print("Clearing vector database...")
    embeddings = get_embeddings()
    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
        collection_name="medical_docs"
    )
    
    # Try to delete the collection data
    try:
        vector_store.delete_collection()
        print("Collection cleared.")
    except Exception as e:
        print(f"Note: Could not clear collection (it might be empty or locked): {e}")

    # Re-initialize
    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
        collection_name="medical_docs"
    )

    # Ingest base knowledge
    ingest_base_knowledge()
    
    # Ingest project-specific initial data
    ingest_directory("Initial_Data")

if __name__ == "__main__":
    # Fully reset and ingest everything to ensure clean state
    reset_and_ingest_all()
