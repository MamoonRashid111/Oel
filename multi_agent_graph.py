import operator
from typing import Annotated, List, TypedDict, Union
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from tools import medical_search

import os

# Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:3b")
BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    context: str
    validated: bool
    retry_count: int
    is_high_risk: bool

llm = ChatOllama(model=MODEL_NAME, base_url=BASE_URL)

def researcher(state: AgentState):
    """The Researcher persona: Finds information."""
    print(f"Researcher node: Connecting to Ollama at {BASE_URL}")
    
    # Extract the last user message for the search query
    query = state["messages"][-1].content
    context = medical_search.invoke(query)
    
    # System instructions for the researcher
    system_instructions = f"""
    You are a Senior Clinical Intelligence Agent.
    Your primary directive is GROUNDING. 

    1. NEVER suggest dosages unless explicitly stated in the provided context. If asked for a dose not in the context, respond: "I do not have specific dosage information for this medication in my current clinical matrix. Please consult a licensed pharmacist or physician."
    2. ALWAYS cite the source of your information (e.g., "According to the provided context..." or "Based on base medical protocols...").
    3. If retrieval results are empty or irrelevant, acknowledge it: "The current clinical trace does not contain information on this topic. I will provide general medical guidelines instead, but please verify with a professional."
    4. Maintain a professional, clinical tone at all times.
    
    Current Medical Context:
    {context}
    """
    
    # Construct message list: System Instructions + Full History
    messages = [HumanMessage(content=system_instructions)] + state["messages"]
    
    response = llm.invoke(messages)
    
    return {
        "messages": [AIMessage(content=response.content)],
        "context": context,
        "retry_count": state.get("retry_count", 0) + 1
    }

def validator(state: AgentState):
    """The Validator persona: Checks for safety and grounding."""
    # Logic to validate the researcher's output
    last_message = state["messages"][-1].content
    context = state["context"]
    
    system_instructions = f"""
    Evaluate the following clinical answer based on the provided source context.
    
    CRITERIA:
    1. Does the answer accurately reflect medical information in the source?
    2. Is the answer free from irrelevant content?
    3. Is the tone professional and clinical?
    
    Source Context: {context}
    
    Respond with 'YES' if it meets all criteria, or 'NO' if it contains irrelevant or ungrounded info.
    """
    
    # We pass the history but emphasize the last answer check
    messages = [HumanMessage(content=system_instructions)] + state["messages"]
    check = llm.invoke(messages)
    
    is_valid = "YES" in check.content.upper()
    
    return {"validated": is_valid}

def should_continue(state: AgentState):
    if state["validated"] or state.get("retry_count", 0) >= 2:
        return END
    else:
        return "researcher"

# Build Graph
workflow = StateGraph(AgentState)

workflow.add_node("researcher", researcher)
workflow.add_node("validator", validator)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "validator")
workflow.add_conditional_edges("validator", should_continue)

graph = workflow.compile()
