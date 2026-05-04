# Product Requirement Document: Medical Assistant Chatbot

## 1. Overview
The Medical Assistant Chatbot is an AI-powered system designed to assist healthcare professionals by providing accurate, grounded information from medical documents. It utilizes RAG (Retrieval-Augmented Generation) and a multi-agent LangGraph architecture to ensure safety and precision.

## 2. Core Features
- **Document Ingestion**: Support for PDF, DOCX, and TXT files.
- **RAG Pipeline**: Semantic chunking and metadata-rich vector storage.
- **Multi-Agent Reasoning**:
    - **Researcher**: Extracts facts from documents.
    - **Validator**: Cross-references facts and ensures medical safety.
- **Human-In-The-Loop (HITL)**: Mandatory approval for critical medical advice.
- **Persistence**: SQLite-based state management for conversation history.
- **API Interface**: FastAPI with streaming support.
- **Professional UI**: Streamlit-based dashboard with source tracking.

## 3. Technical Stack
- **LLM**: qwen2.5:3b via Ollama.
- **Frameworks**: LangChain, LangGraph, FastAPI, Streamlit.
- **Database**: ChromaDB (Vector Store), SQLite (State Store).

## 4. Safety & Compliance
- **Guardrails**: Implementation of safety checks for non-medical or harmful queries.
- **Grounding**: Strict adherence to provided document context.
- **Disclaimer**: Mandatory display of medical disclaimer in the UI.

## 5. Success Metrics
- Retrieval accuracy > 85%.
- Response latency < 5s (first token).
- Successful state persistence across sessions.
