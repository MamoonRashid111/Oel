import streamlit as st
import requests
import os
import time
from ingest_data import ingest_document
from db_utils import init_db, log_feedback

# Initialize Feedback DB
init_db()

# Page Config
st.set_page_config(
    page_title="MedAssist Pro | Healthcare Intelligence",
    layout="wide",
    page_icon="🩺",
    initial_sidebar_state="expanded"
)

# Sophisticated Dark Theme (CSS)
st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background-color: #0f172a !important; /* Deep Navy/Charcoal */
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide white elements */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important; /* Lighter Navy */
        border-right: 1px solid #334155;
    }
    
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #cbd5e1 !important;
    }

    /* Main Header Styling */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(to right, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        padding-top: 2rem;
    }
    
    .sub-header {
        color: #94a3b8;
        text-align: center;
        margin-bottom: 3rem;
        font-size: 1.1rem;
        font-weight: 300;
    }

    /* Chat Bubble Customization */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
    }
    
    /* User Message Bubble */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) .stChatMessageContent {
        background: rgba(59, 130, 246, 0.15) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        color: #e2e8f0 !important;
        border-radius: 16px 16px 0px 16px !important;
        padding: 1.25rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
    }
    
    /* Assistant Message Bubble */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) .stChatMessageContent {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        color: #f1f5f9 !important;
        border-radius: 16px 16px 16px 0px !important;
        padding: 1.25rem !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }

    /* Input Field Styling */
    .stChatInputContainer {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
    }
    
    .stChatInputContainer textarea {
        color: #f8fafc !important;
    }

    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: #1e293b !important;
        color: #94a3b8 !important;
        border-radius: 8px !important;
        border: 1px solid #334155 !important;
    }
    
    .streamlit-expanderContent {
        background-color: #0f172a !important;
        color: #cbd5e1 !important;
    }

    /* Status Bar */
    div[data-testid="stStatus"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        color: #60a5fa !important;
    }

    /* Disclaimer Section */
    .disclaimer-box {
        background-color: #1e293b;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        margin-top: 3rem;
        border-radius: 0 8px 8px 0;
    }
    
    .disclaimer-text {
        font-size: 0.85rem;
        color: #94a3b8;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

# Application Header
st.markdown('<h1 class="main-header">🩺 MedAssist Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced Multi-Agent Clinical Intelligence System</p>', unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("### 🧬 Knowledge Matrix")
    st.markdown("---")
    
    st.markdown("**Local Document Ingestion**")
    uploaded_file = st.file_uploader("Upload Clinical Data (PDF/TXT)", type=["pdf", "txt", "docx"], label_visibility="collapsed")
    
    if uploaded_file:
        if "processed_files" not in st.session_state:
            st.session_state.processed_files = set()
            
        if uploaded_file.name not in st.session_state.processed_files:
            with st.spinner("Decrypting & Indexing..."):
                temp_path = os.path.join("temp", uploaded_file.name)
                os.makedirs("temp", exist_ok=True)
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                try:
                    ingest_document(temp_path)
                    st.session_state.processed_files.add(uploaded_file.name)
                    st.success(f"✓ {uploaded_file.name} Verified")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Ingestion Failure: {e}")
        else:
            st.info(f"ℹ️ {uploaded_file.name} is already indexed.")

    st.markdown("---")
    st.markdown("**Operational Controls**")
    thread_id = st.text_input("Active Thread ID", value="clinic_delta_9")
    show_sources = st.toggle("Evidence-Based Reporting", value=True)
    
    if st.button("Reset Matrix History"):
        st.session_state.messages = []
        st.rerun()

# Message State Management
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_approval" not in st.session_state:
    st.session_state.pending_approval = False
if "current_thread" not in st.session_state:
    st.session_state.current_thread = "clinic_delta_9"

# HITL Approval Banner (Moved to top for visibility)
if st.session_state.pending_approval:
    st.warning("⚠️ **CLINICAL VERIFICATION REQUIRED**: This response contains high-risk medical information (dosage, surgery, or critical diagnosis) and requires human professional approval before being finalized.")
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("✅ Approve & Release", use_container_width=True):
            with st.spinner("Finalizing Clinical Protocol..."):
                try:
                    API_URL = os.getenv("API_URL", "http://localhost:8000")
                    resp = requests.post(
                        f"{API_URL}/approve",
                        json={"thread_id": st.session_state.current_thread},
                        timeout=30
                    )
                    if resp.status_code == 200:
                        st.session_state.pending_approval = False
                        st.success("Protocol Approved.")
                        time.sleep(1)
                        st.rerun()
                except Exception as e:
                    st.error(f"Approval Error: {e}")
    with col2:
        st.info("As a Healthcare Professional, your approval confirms this information is grounded in the provided clinical evidence.")

# Rendering Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if show_sources and "context" in message and message["role"] == "assistant":
            with st.expander("🔍 Clinical Traceability & Context"):
                st.code(message["context"], language="markdown")
        
        # Feedback Widget for Assistant Messages
        if message["role"] == "assistant":
            feedback_key = f"feedback_{st.session_state.messages.index(message)}"
            feedback = st.feedback("thumbs", key=feedback_key)
            if feedback is not None:
                # Streamlit "thumbs": 0 is Down, 1 is Up
                final_score = 1 if feedback == 1 else -1
                
                if "logged_feedback" not in st.session_state:
                    st.session_state.logged_feedback = set()
                
                if feedback_key not in st.session_state.logged_feedback:
                    log_feedback(
                        thread_id=thread_id,
                        user_input=message.get("user_input", "Unknown"),
                        agent_response=message["content"],
                        feedback_score=final_score
                    )
                    st.session_state.logged_feedback.add(feedback_key)
                    st.toast("Feedback recorded. Thank you!", icon="🩺")

# Conversation Input
if prompt := st.chat_input("Initiate clinical query (e.g., 'From Doc, summarize findings')"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("📡 Orchestrating Agent Reasoning...", expanded=True) as status:
            try:
                API_URL = os.getenv("API_URL", "http://localhost:8000")
                response = requests.post(
                    f"{API_URL}/chat",
                    json={"message": prompt, "thread_id": thread_id},
                    timeout=90
                )
                if response.status_code == 200:
                    data = response.json()
                    ans = data["response"]
                    ctx = data.get("context", "Base Medical Protocol Applied")
                    is_pending = data.get("requires_approval", False)
                    
                    status.update(label="✓ Clinical Logic Processed", state="complete", expanded=False)
                    
                    if is_pending:
                        st.session_state.pending_approval = True
                        st.info("System is waiting for your professional approval...")
                    
                    st.markdown(ans)
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": ans,
                        "context": ctx,
                        "user_input": prompt 
                    })
                    st.rerun() 
                else:
                    status.update(label="✘ Backend Logic Error", state="error")
                    st.error("Protocol Error: The medical reasoning engine failed to initialize.")
            except Exception as e:
                status.update(label="✘ Connection Interrupted", state="error")
                st.error(f"Neural Link Error: {e}")

# Footer Safety Protocol
st.markdown("""
    <div class="disclaimer-box">
        <p class="disclaimer-text">
            <b>CRITICAL SAFETY PROTOCOL:</b> MedAssist Pro outputs are generated by AI. 
            This system does not provide medical diagnosis. All outputs MUST be verified by a licensed medical professional. 
            For life-threatening situations, seek immediate professional help.
        </p>
    </div>
    """, unsafe_allow_html=True)
