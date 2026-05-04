from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

import os

# Configuration
CHROMA_PATH = os.getenv("CHROMA_PATH", "chroma_db")
CHROMA_HOST = os.getenv("CHROMA_HOST", None)
CHROMA_PORT = os.getenv("CHROMA_PORT", "8000")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:3b")
BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

class SearchInput(BaseModel):
    query: str = Field(description="The medical query to search for in the documents.")

@tool("medical_search", args_schema=SearchInput)
def medical_search(query: str) -> str:
    """Search for information in the medical document database with source filtering."""
    print(f"Medical Search invoked. Connecting to Ollama at: {BASE_URL}")
    embeddings = OllamaEmbeddings(model=MODEL_NAME, base_url=BASE_URL)
    
    if CHROMA_HOST:
        import chromadb
        print(f"Connecting to Remote Chroma: {CHROMA_HOST}:{CHROMA_PORT}")
        client = chromadb.HttpClient(host=CHROMA_HOST, port=int(CHROMA_PORT))
        vector_store = Chroma(
            client=client,
            embedding_function=embeddings,
            collection_name="medical_docs"
        )
    else:
        vector_store = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings,
            collection_name="medical_docs"
        )
    
    # Determine filtering logic based on keywords
    where_filter = None
    if "medical knowledge" in query.lower() or "base knowledge" in query.lower():
        where_filter = {"source_file": "medical_knowledge.txt"}
    elif "doc" in query.lower() or "uploaded" in query.lower():
        where_filter = {"source_file": {"$ne": "medical_knowledge.txt"}}

    # Search with optional metadata filter
    results = vector_store.similarity_search(query, k=10, filter=where_filter)
    
    context_parts = []
    for res in results:
        source = res.metadata.get('source_file', 'Base Knowledge')
        context_parts.append(f"Source: {source}\nContent: {res.page_content}")
    
    context = "\n\n---\n\n".join(context_parts)
    
    if not context:
        return "No relevant information found for the specified source. Please try asking without source keywords."
    
    return context

class ValidationInput(BaseModel):
    fact: str = Field(description="The fact to validate.")
    source_context: str = Field(description="The source context to validate against.")

@tool("validate_fact", args_schema=ValidationInput)
def validate_fact(fact: str, source_context: str) -> bool:
    """Validate if a specific fact is supported by the source context."""
    # This is a simplified logic. In a real scenario, this might involve another LLM call.
    return fact.lower() in source_context.lower()

tools = [medical_search, validate_fact]
