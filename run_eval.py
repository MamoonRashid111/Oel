import json
import os
import sys
from multi_agent_graph import graph
from langchain_core.messages import HumanMessage

def run_evaluation():
    # Load threshold configuration
    config_path = os.getenv("EVAL_CONFIG_PATH", "eval_threshold_config.json")
    try:
        with open(config_path, "r") as f:
            thresholds = json.load(f)
    except FileNotFoundError:
        thresholds = {"min_avg_score": 0.8}

    # Load dataset
    dataset_path = os.getenv("TEST_DATASET_PATH", "test_dataset.json")
    with open(dataset_path, "r") as f:
        dataset = json.load(f)
    
    results = []
    print(f"Starting evaluation of {len(dataset)} pairs...")
    
    for item in dataset:
        print(f"Testing: {item['question']}")
        config = {"configurable": {"thread_id": "eval_thread"}}
        
        try:
            print(f"  [Step 1/2] Invoking Agent...")
            response = graph.invoke({"messages": [HumanMessage(content=item["question"])]}, config)
            actual_answer = response["messages"][-1].content
            
            print(f"  [Step 2/2] Calculating Score...")
            # Simple keyword matching for score (can be replaced with Ragas/Judge LLM)
            score = 1.0 if any(keyword in actual_answer.lower() for keyword in item["answer"].lower().split() if len(keyword) > 3) else 0.0
            
            results.append({
                "question": item["question"],
                "expected": item["answer"],
                "actual": actual_answer,
                "score": score
            })
        except Exception as e:
            print(f"Error evaluating '{item['question']}': {e}")
            results.append({
                "question": item["question"],
                "expected": item["answer"],
                "actual": f"ERROR: {str(e)}",
                "score": 0.0
            })
    
    avg_score = sum(r["score"] for r in results) / len(results)
    print(f"\nEvaluation Complete. Average Score: {avg_score:.2f}")
    
    # Save results
    with open("eval_results.json", "w") as f:
        json.dump(results, f, indent=4)
    
    # CI/CD Gate
    min_score = thresholds.get("min_avg_score", 0.8)
    if avg_score >= min_score:
        print(f"SUCCESS: Average score {avg_score:.2f} meets threshold {min_score}")
        sys.exit(0)
    else:
        print(f"FAILURE: Average score {avg_score:.2f} is below threshold {min_score}")
        sys.exit(1)

if __name__ == "__main__":
    run_evaluation()
