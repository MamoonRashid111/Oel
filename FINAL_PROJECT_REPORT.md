# Project Report: MedAssist Pro — Advanced Multi-Agent Clinical Intelligence System

## 1. Executive Summary
**MedAssist Pro** is an industrial-grade AI clinical assistant designed to support healthcare professionals by providing accurate, grounded, and safe medical information. The system is built on a state-of-the-art **Multi-Agent LangGraph** architecture, integrating **Retrieval-Augmented Generation (RAG)** with strict **Human-In-The-Loop (HITL)** safety protocols. Unlike generic LLM interfaces, MedAssist Pro ensures that every response is cited, validated for clinical accuracy, and reviewed by a professional for high-risk scenarios.

---

## 2. System Architecture

The architecture follows a modular design focused on safety and transparency.

### 2.1 Multi-Agent Orchestration (LangGraph)
The core logic is managed by a directed graph where specialized agents collaborate in a sequence:

1.  **Input Guardrail**: Analyzes user intent to block adversarial attacks (jailbreaks) or out-of-scope queries (e.g., finance, politics).
2.  **Researcher Agent**: Performs semantic retrieval from the vector database and synthesizes a response grounded in clinical evidence.
3.  **Clinical Validator**: Cross-references the researcher's output against the source context to detect hallucinations or ungrounded claims.
4.  **Risk Classifier**: Automatically identifies "High-Risk" content (e.g., dosage recommendations, surgical procedures).
5.  **Human-In-The-Loop (HITL)**: If a query is high-risk, the system pauses execution using a SQLite checkpointer, requiring professional approval before the answer is released.

### 2.2 Knowledge Management (RAG Pipeline)
- **Vector Database**: **ChromaDB** is used to store high-dimensional embeddings of medical documents.
- **Ingestion Engine**: `ingest_data.py` processes PDF, TXT, and DOCX files, applying semantic chunking and metadata enrichment.
- **Grounding Justification**: Every response includes a "Clinical Traceability" section showing the exact source text used.

---

## 3. Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Orchestration** | LangGraph | State management and agentic workflow |
| **Large Language Model** | Qwen 2.5 (3B) / Ollama | Local, privacy-preserving reasoning engine |
| **Vector Store** | ChromaDB | High-performance semantic document retrieval |
| **Persistence** | SQLite | Conversation checkpointers and HITL state |
| **API Layer** | FastAPI | RESTful backend with streaming support |
| **User Interface** | Streamlit | Premium clinical dashboard with custom dark-navy aesthetics |
| **Infrastructure** | Docker & Compose | Containerized, reproducible environment |

---

## 4. Key Features & Implementation

### 4.1 Professional Clinical UI
The frontend (`app.py`) is designed for healthcare settings:
- **Dark Mode Aesthetic**: Uses a custom CSS-in-JS implementation for a premium, non-distracting look.
- **Evidence Reporting**: Collapsible sections for source context.
- **Feedback Loop**: Integrated "thumbs up/down" to log performance for drift analysis.
- **Security Banners**: Real-time warnings when human approval is pending.

### 4.2 Drift Monitoring & Observability
- **`analyze_feedback.py`**: A diagnostic tool that parses user feedback to identify common failure points.
- **`drift_report.md`**: Tracks model performance shifts over time, identifying "concept drift" in clinical accuracy.
- **`checkpoints.sqlite`**: Stores the entire state of every conversation, allowing for seamless session recovery.

### 4.3 Quality Assurance Suite
- **`run_eval.py`**: Automated benchmarking against a clinical test dataset (`test_dataset.json`).
- **`breaking_change_test.py`**: Regression testing to ensure updates don't compromise safety guardrails.

---

## 5. File Manifest & Structure

- `app.py`: Main Streamlit application (UI).
- `main.py`: FastAPI backend entry point.
- `secured_graph.py`: Implementation of the safety-first LangGraph.
- `multi_agent_graph.py`: Core agent logic (Researcher/Validator).
- `tools.py`: Search and retrieval tools.
- `ingest_data.py`: Data processing pipeline.
- `db_utils.py`: Database operations for feedback and logging.
- `Dockerfile` / `docker-compose.yaml`: Deployment configurations.
- `requirements.txt`: Python dependency list.

---

## 6. Setup & Deployment

### Prerequisites
- Python 3.10+
- Ollama (running `qwen2.5:3b`)
- Docker (optional for containerized setup)

### Local Installation
1.  **Clone the Repository**.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Start the Backend**:
    ```bash
    python main.py
    ```
4.  **Start the Frontend**:
    ```bash
    streamlit run app.py
    ```

---

## 7. Future Enhancements
- **Multi-Modal Support**: Analyzing X-ray/MRI metadata.
- **Real-time API Integration**: Connecting to PubMed or clinical trial registries.
- **Granular Permissions**: Role-based access control for different tiers of medical professionals.

---

## 8. Compliance & Disclaimer
MedAssist Pro is a **Decision Support System**, not a diagnostic tool. All clinical decisions must be made by licensed medical professionals. The system logs all interactions for auditing and quality improvement purposes.
