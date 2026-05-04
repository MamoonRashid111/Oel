import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from multi_agent_graph import graph
from langchain_core.messages import HumanMessage

def test_persistence():
    # Setup database
    conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
    memory = SqliteSaver(conn)
    
    # Compile graph with persistence
    app = graph.with_config(checkpointer=memory)
    
    config = {"configurable": {"thread_id": "test_thread_1"}}
    
    # Initial interaction
    print("--- First Interaction ---")
    input_msg = HumanMessage(content="What are the symptoms of COVID-19?")
    for event in app.stream({"messages": [input_msg]}, config):
        print(event)
    
    # Verify state is saved
    state = app.get_state(config)
    print(f"\nSaved messages: {len(state.values['messages'])}")
    
    print("\nPersistence test successful if messages were saved.")

if __name__ == "__main__":
    # Note: Requires Ollama to be running and documents to be ingested for a full test.
    # test_persistence()
    pass
