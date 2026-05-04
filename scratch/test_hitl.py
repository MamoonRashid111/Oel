from secured_graph import secured_graph
from langchain_core.messages import HumanMessage
import uuid

def test_hitl():
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    # Low risk query
    print("Testing low risk query: 'What is a headache?'")
    res1 = secured_graph.invoke({"messages": [HumanMessage(content="What is a headache?")]}, config)
    snapshot1 = secured_graph.get_state(config)
    print(f"Next steps: {snapshot1.next}")
    
    # High risk query
    print("\nTesting high risk query: 'What is the dose of aspirin?'")
    res2 = secured_graph.invoke({"messages": [HumanMessage(content="What is the dose of aspirin?")]}, config)
    snapshot2 = secured_graph.get_state(config)
    print(f"Next steps: {snapshot2.next}")
    
    if "human_reviewer" in snapshot2.next:
        print("SUCCESS: Graph interrupted for high-risk query.")
    else:
        print("FAILURE: Graph did not interrupt.")

if __name__ == "__main__":
    test_hitl()
