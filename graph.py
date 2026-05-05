from typing import Annotated, List, TypedDict
import operator
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from multi_agent_graph import researcher, validator, should_continue, AgentState
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

def guardrail(state: AgentState):
    """Enhanced safety guardrail node."""
    last_msg = state["messages"][-1].content
    
    # Category 1: Harmful & Adversarial Content
    harmful_keywords = [
        "poison", "kill", "suicide", "illegal", "bomb", "weapon",
        "hack", "bypass", "delete", "override", "exploit", "jailbreak"
    ]
    if any(word in last_msg.lower() for word in harmful_keywords):
        return {
            "messages": [AIMessage(content="🚨 SECURITY ALERT: This request contains prohibited or adversarial keywords. The operation has been blocked by the clinical safety protocol.")],
            "validated": True
        }
    
    # Category 2: Non-Medical Scope
    non_medical_keywords = ["weather", "stock market", "crypto", "joke", "movie"]
    if any(word in last_msg.lower() for word in non_medical_keywords):
        return {
            "messages": [AIMessage(content="ℹ️ SCOPE NOTICE: I am a specialized Medical Assistant. Please restrict your queries to clinical and health-related topics.")],
            "validated": True
        }
        
    return {}

def risk_classifier(state: AgentState):
    """Classifies if the query/response is high-risk and needs human approval."""
    last_msg = state["messages"][-1].content
    
    risk_keywords = ["dose", "dosage", "surgery", "operation", "cancer", "emergency", "prescription", "medication", "treatment", "drug", "relief"]
    is_high_risk = any(word in last_msg.lower() for word in risk_keywords)
    
    return {"is_high_risk": is_high_risk}

def human_reviewer(state: AgentState):
    """Node that triggers the interrupt for human approval."""
    # This node is a placeholder that we interrupt before.
    # When resumed, it just passes through.
    return {}

def route_after_validator(state: AgentState):
    """Routes to human review if high risk, otherwise ends."""
    if state.get("is_high_risk"):
        return "human_reviewer"
    return END

# Build Secured Graph
workflow = StateGraph(AgentState)

workflow.add_node("guardrail", guardrail)
workflow.add_node("researcher", researcher)
workflow.add_node("validator", validator)
workflow.add_node("risk_classifier", risk_classifier)
workflow.add_node("human_reviewer", human_reviewer)

workflow.set_entry_point("guardrail")
workflow.add_edge("guardrail", "researcher")
workflow.add_edge("researcher", "validator")
workflow.add_edge("validator", "risk_classifier")

workflow.add_conditional_edges(
    "risk_classifier",
    route_after_validator,
    {
        "human_reviewer": "human_reviewer",
        END: END
    }
)

workflow.add_edge("human_reviewer", END)

# Use SQLite for persistence and support interrupts
conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
memory = SqliteSaver(conn)

# We define points where the execution should stop for human review
secured_graph = workflow.compile(
    checkpointer=memory,
    interrupt_before=["human_reviewer"] 
)
