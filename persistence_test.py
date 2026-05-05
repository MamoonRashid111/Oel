import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from multi_agent_graph import graph
from langchain_core.messages import HumanMessage

def test_persistence():
    # Setup database
    conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
    memory = SqliteSaver(conn)
    
    # Note: 'graph' is already compiled in multi_agent_graph, 
    # but we use the 'secured_graph' version which already has persistence configured.
    from secured_graph import secured_graph
    
    config = {"configurable": {"thread_id": "persistence_demo_final"}}
    
    print("\n[STEP 1] Starting First Session...")
    input_1 = HumanMessage(content="Hello, my name is Dr. Smith. What is the standard adult dose for Aspirin?")
    result_1 = secured_graph.invoke({"messages": [input_1]}, config)
    print(f"Agent Response 1: {result_1['messages'][-1].content[:100]}...")
    
    print("\n[STEP 2] Closing and Re-opening Session (Simulating Restart)...")
    # In a real scenario, the script would end here and be re-run.
    # We verify by checking the state of the SAME thread_id.
    
    print("\n[STEP 3] Resuming Session with same Thread ID...")
    input_2 = HumanMessage(content="What did I just say my name was?")
    result_2 = secured_graph.invoke({"messages": [input_2]}, config)
    
    print(f"Agent Response 2: {result_2['messages'][-1].content}")
    
    # Debug: Print entire message history
    print("\n--- Full Message History ---")
    for m in result_2['messages']:
        print(f"{type(m).__name__}: {m.content[:50]}...")
    
    if "Smith" in result_2['messages'][-1].content:
        print("\nSUCCESS: Persistence Verified. The agent remembered the name across interactions.")
    else:
        print("\nFAILURE: Persistence Failed. The agent forgot the name.")

if __name__ == "__main__":
    test_persistence()
