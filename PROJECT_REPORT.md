# Project Report: Industrial-Grade Medical Assistant Chatbot

## 1. Executive Summary
The **Industrial Medical Assistant** is a production-ready AI system designed to assist healthcare professionals by providing accurate, grounded clinical information. Built with a focus on safety, reliability, and transparency, the system leverages a multi-agent **LangGraph** architecture combined with a **Retrieval-Augmented Generation (RAG)** pipeline. Key differentiators include mandatory human-in-the-loop (HITL) triggers for high-risk advice, robust security guardrails, and automated evaluation metrics.

---

## 2. System Architecture

The project follows a modular, containerized architecture consisting of a backend processing engine, a vector database, and a professional user interface.

### 2.1 Multi-Agent Reasoning (LangGraph)
The core logic is orchestrated using LangGraph, which allows for complex, stateful workflows. The graph consists of several specialized nodes:
- **Guardrail Node**: Intercepts requests to block harmful, adversarial, or out-of-scope (non-medical) queries.
- **Researcher Agent**: Queries the knowledge base using ChromaDB to extract relevant medical facts.
- **Validator Agent**: Reviews the researcher's output for clinical accuracy and ensures it aligns with the provided documents.
- **Risk Classifier**: Analyzes the generated response for "high-risk" keywords (e.g., dosage, surgery, medication).
- **Human-In-The-Loop (HITL)**: If a response is deemed high-risk, the system interrupts execution and requires professional approval before sending the response to the user.

### 2.2 RAG Pipeline
- **Vector Database**: Uses **ChromaDB** for persistent storage of document embeddings.
- **Data Ingestion**: A dedicated pipeline (`ingest_data.py`) handles chunking and metadata enrichment for PDF, DOCX, and TXT files.
- **Grounding**: Every response is strictly tied to the ingested medical knowledge, with a "Grounding Justification" provided for transparency.

---

## 3. Technology Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **LLM** | Qwen 2.5 (3B) | Core reasoning and language generation |
| **Framework** | LangGraph | Multi-agent orchestration and state management |
| **Interface** | FastAPI | RESTful API for integration and HITL |
| **Frontend** | Streamlit | Professional medical professional dashboard |
| **Vector DB** | ChromaDB | Semantic retrieval of medical documents |
| **State DB** | SQLite | Persistent conversation checkpointers |
| **DevOps** | Docker | Containerization and service orchestration |

---

## 4. Detailed Component Breakdown

### 4.1 Multi-Agent Collaboration
The system uses a **Synchronous Multi-Agent Graph** where agents act in a sequence to ensure quality:
1.  **Researcher**: Specializes in fact-extraction. It uses semantic search to find clinical evidence in the knowledge base.
2.  **Validator**: A "Clinical Auditor" persona that cross-references the Researcher's draft against the source text to prevent hallucinations.
3.  **Risk Classifier**: A logic gate that determines if the content requires a human "Senior Physician" (HITL) review.

### 4.2 Security & Guardrails
- **Input Guardrail**: Prevents "Jailbreaking" and ensures the chatbot is only used for medical queries.
- **Output Guardrail**: Ensures responses are professional and include necessary medical disclaimers.

### 4.3 Evaluation & Quality Assurance
The project includes a robust testing suite:
- **`run_eval.py`**: Runs a series of clinical questions against the system and calculates an accuracy score.
- **`breaking_change_test.py`**: Ensures that code changes do not degrade the agent's performance.
- **`drift_report.md`**: Tracks performance shifts over time based on user feedback and automated logs.

---

## 5. Deployment & Infrastructure
The project is fully containerized to ensure reproducibility:
- **`Dockerfile`**: Builds the core application environment.
- **`docker-compose.yaml`**: Orchestrates the API, Streamlit UI, and Ollama services.
- **Volume Mapping**: Ensures database persistence (`chroma_db`, `checkpoints.sqlite`) across container restarts.

---

## 6. Compliance & Professionalism
- **Medical Disclaimer**: Every user interaction starts with a mandatory clinical disclaimer.
- **Source Tracking**: The UI highlights which documents were used to generate a specific response.
- **Audit Logs**: Conversation history and feedback are logged for continuous improvement.

---

## 7. Future Roadmap
- **Feedback Analysis**: Implementing automated drift reports based on user feedback.
- **Expanded Knowledge**: Support for real-time medical API integrations (e.g., PubMed).
- **Enhanced Personas**: specialized agents for different medical fields (Oncology, Pediatrics, etc.).
