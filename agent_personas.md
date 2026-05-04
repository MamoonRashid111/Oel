# Agent Personas: Medical Assistant Graph

The system employs a collaborative multi-agent architecture via LangGraph.

## 1. The Researcher
- **Goal**: Retrieve and summarize relevant medical information.
- **Tools**: `medical_search`
- **Behavior**: Focused on extracting facts from the provided context. It maintains a clinical and objective tone.
- **Constraint**: Must only use information found in the vector store.

## 2. The Validator
- **Goal**: Ensure the Researcher's output is safe and grounded.
- **Tools**: `validate_fact`
- **Behavior**: Acts as a critical reviewer. It checks for consistency between the Researcher's answer and the source context.
- **Safety Role**: Specifically looks for medical inaccuracies or hallucinations.

## 3. The Guardrail (Entry/Exit)
- **Goal**: Block harmful or out-of-scope requests.
- **Behavior**: Scans input for safety violations before processing. Ensures the system remains within its medical assistance boundaries.

## 4. Human Persona (HITL)
- **Goal**: Provide final approval for high-risk medical advice.
- **Role**: A healthcare professional who reviews the validated agent output before it is finalized.
