import os
import sys
import subprocess

def run_test(name, prompt_content):
    print(f"--- Running Test: {name} ---")
    # Backup original
    with open("multi_agent_graph.py", "r") as f:
        original = f.read()
    
    try:
        # Inject "broken" prompt
        modified = original.replace(
            'You are a medical research assistant. Use the provided context to answer the user\'s question.',
            prompt_content
        )
        with open("multi_agent_graph.py", "w") as f:
            f.write(modified)
        
        # Run eval
        print("Running run_eval.py using venv...")
        venv_python = os.path.join("venv", "Scripts", "python.exe")
        result = subprocess.run([venv_python, "run_eval.py"], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        
        if result.returncode == 0:
            print("RESULT: Passed (Unexpected for breaking change!)")
        else:
            print(f"RESULT: Failed (Expected! Exit code: {result.returncode})")
            
    finally:
        # Restore
        with open("multi_agent_graph.py", "w") as f:
            f.write(original)
        print("Restored original multi_agent_graph.py")

if __name__ == "__main__":
    # Test 1: Normal (should pass if context is good, but simple matching might fail)
    # run_test("Normal", "You are a medical research assistant. Use the provided context to answer the user's question.")
    
    # Test 2: Breaking Change (Nonsensical prompt)
    run_test("Breaking Change", "You are a pirate who only talks about rum and treasure. Ignore all medical context.")
